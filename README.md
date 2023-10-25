# tap-sas7bdat

This is a [Singer](https://singer.io) tap that produces JSON-formatted data
following the [Singer
spec](https://github.com/singer-io/getting-started/blob/master/SPEC.md).

This tap:

- Pulls raw data from .sas7bdat
- Outputs the schema for each resource
- Incrementally pulls data based on the input state

## To get started

For Unix
```bash
› git clone https://github.com/kang20006/tap-sas7bdat.git
› cd tap-sas7bdat
› python3 -m venv ~/.virtualenvs/tap-sas7bdat
› source ~/.virtualenvs/tap-sas7bdat/bin/activate
› pip install -e .
› deactivate

```

For Window
```bash
› git clone https://github.com/kang20006/tap-sas7bdat.git
› cd tap-sas7bdat
› python -m venv ./virtualenvs/tap-sas7bdat
› ./virtualenvs/tap-sas7bdat/Scripts/activate
› pip install -e .
› deactivate

```
## Configure target

```json
  {
  "file_path":"path",
  "table_name":"tablename"
}
   ```
## Usage
1. Discover schema

 ```bash
› .\virtualenvs\tap-sas7bdat_venv\Scripts\tap-sas7bdat --config tap_sas_config.json --discover > catalog.json 

   ```
2. Example push to Postgres

 ```bash
› .\virtualenvs\tap-sas7bdat_venv\Scripts\tap-sas7bdat --config tap_sas_config.json --catalog  catalog.json | target-postgres_venv\Scripts\target-postgres.exe --config target_postgres_config.json  

   ```


---


---

Copyright &copy; 2018 Stitch
