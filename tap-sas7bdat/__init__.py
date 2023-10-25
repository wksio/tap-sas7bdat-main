import os
import json
import singer
from singer import utils
from singer.catalog import Catalog, CatalogEntry
from singer.schema import Schema
import pandas as pd

REQUIRED_CONFIG_KEYS = ["file_path", "table_name"]
LOGGER = singer.get_logger()


def get_abs_path(path):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), path)


def load_schemas(df):
    schema = {"type": "object", "properties": {}}

    for column in df.columns:
        if df[column].dtype == "float64":
            column_type = ["number","null"]
            out={"type": column_type}
        elif df[column].dtype == "Int64":
            column_type = ["integer","null"]
            out={"type": column_type}
        elif df[column].dtype == "bool":
            column_type = ["boolean","null"]
            out={"type": column_type}
        elif df[column].dtype == "datetime64[ns]":
            column_type = ["string","null"]
            format1="date-time"
            out={"type": column_type,"format": format1}
        else:
            column_type = "string"
            out={"type": column_type}
        schema["properties"][column] = out

    return schema

def read_sas7bdat_file(file_path):
    try:
        df = pd.read_sas(file_path, format='sas7bdat',encoding='utf-8')
        df['index_id'] = df.index
        
        return df
    except Exception as e:
        LOGGER.error(f"Error reading SAS file: {e}")
        return None

def discover(config):
    file_path = config['file_path']

    df = read_sas7bdat_file(file_path)
    table_name = config['table_name']
    raw_schemas = load_schemas(df)
    
    streams = []
    stream_id = table_name
    stream_metadata = []
    key_properties = ["index_id"]
    streams.append(
        CatalogEntry(
            tap_stream_id=stream_id,
            stream=stream_id,
            schema=Schema.from_dict(raw_schemas),
            key_properties=key_properties,
            metadata=stream_metadata,
            replication_key=None,
            is_view=None,
            database=None,
            table=None,
            row_count=None,
            stream_alias=None,
            replication_method=None,
        )
    )  
    return Catalog(streams)

def sync(config, catalog):
    """Sync data from tap source"""
    # Loop over selected streams in catalog
    for stream in catalog.streams:
        LOGGER.info("Syncing stream:" + stream.tap_stream_id)

        singer.write_schema(
            stream_name=stream.tap_stream_id,
            schema=stream.schema.to_dict(),
            key_properties=stream.key_properties
        )
        # data retrieval process:
        file_path = config['file_path']
        table_name = config['table_name']
        df = read_sas7bdat_file(file_path)
        date_columns = df.select_dtypes(include=['datetime64']).columns.tolist()
        df[date_columns] = df[date_columns].astype(str)
        if df is not None:
            for row in df.itertuples(index=False):
                record = {k: v for k, v in zip(df.columns, row)}
                record = {k: None if pd.isna(v) else v for k, v in record.items() }
                singer.write_record(stream_name=stream.tap_stream_id, record=record)

        # singer.write_state(state)
        
    return

@singer.utils.handle_top_exception(LOGGER)
def main():
    # Parse command line arguments
    args = singer.utils.parse_args(REQUIRED_CONFIG_KEYS)

    # If discover flag was passed, run discovery mode and dump output to stdout
    if args.discover:
        catalog = discover(args.config)
        catalog.dump()
    # Otherwise run in sync mode
    else:
        if args.catalog:
            catalog = args.catalog
        else:
            catalog = discover(args.config)
        sync(args.config, catalog)


if __name__ == "__main__":
    main()