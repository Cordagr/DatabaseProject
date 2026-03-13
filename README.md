# appender.py

`appender.py` is a simple file-backed key-value store.

## Utility 

- Accepts commands from standard input: `SET <key> <value>`, `GET <key>`, `EXIT`
- Stores updates in `data.db` as append-only lines: `SET key value`
- Rebuilds in-memory state from `data.db` on startup (persistence)
- Returns the latest value for a key on `GET`

## Run

```bash
python appender.py
```

## Example

```text
SET name Jack
GET name
Jack
EXIT
```

