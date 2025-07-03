# SQL Query Runner (Python)
pyinstaller --onefile --noconsole --exclude-module PyQt6 sqlquery.py
A command-line tool to execute MySQL queries or SQL files and return the results as formatted JSON. Supports single queries, multi-statement queries, and reading queries from files. Handles date, datetime, and decimal types in output.

## Requirements
- Python 3.x
- `mysql-connector-python` package

## Installation
1. Install Python 3 if not already installed.
2. Install the required package:
   ```sh
   pip install mysql-connector-python
   ```

## Usage
Run the script from the command line with the required arguments:

```
python sqlquery.py --host <HOST> --user <USER> --password <PASSWORD> --database <DB> [--query <SQL>] [--sqlfile <FILE>]
```

- `--host`      : MySQL server host (required)
- `--user`      : MySQL username (required)
- `--password`  : MySQL password (required)
- `--database`  : Database name (required)
- `--query`     : SQL query to execute (optional)
- `--sqlfile`   : Path to SQL file to execute (optional)

You must provide either `--query` or `--sqlfile`.

### Examples

#### 1. Run a single SELECT query
```
python sqlquery.py --host localhost --user root --password mypass --database testdb --query "SELECT * FROM users;"
```

#### 2. Run a DML query (INSERT/UPDATE/DELETE)
```
python sqlquery.py --host localhost --user root --password mypass --database testdb --query "UPDATE users SET name='John' WHERE id=1;"
```

#### 3. Run multiple queries (multi-statement)
```
python sqlquery.py --host localhost --user root --password mypass --database testdb --query "SELECT * FROM users; SELECT COUNT(*) FROM users;"
```

#### 4. Run queries from a SQL file
```
python sqlquery.py --host localhost --user root --password mypass --database testdb --sqlfile path/to/queries.sql
```

#### 5. Run a query with date, datetime, or decimal columns
```
python sqlquery.py --host localhost --user root --password mypass --database testdb --query "SELECT id, amount, created_at FROM orders;"
```

## Output
- Results are printed as formatted JSON.
- Handles MySQL `DATE`, `DATETIME`, and `DECIMAL` types.
- On error, prints a JSON error message.

## Example Output
```json
{
  "status": "success",
  "host": "localhost",
  "database": "testdb",
  "results": [
    {
      "query": "SELECT * FROM users;",
      "result": [
        {"id": 1, "name": "Alice", "balance": 123.45, "created_at": "2024-01-01T12:00:00"}
      ]
    }
  ]
}
```

## License
MIT
