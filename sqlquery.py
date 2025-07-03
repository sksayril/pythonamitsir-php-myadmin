import mysql.connector
import argparse
import sys
import os
import json
from datetime import date, datetime
import decimal  # Added import

# Custom encoder to handle date, datetime, and decimal.Decimal objects
def custom_json_encoder(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    if isinstance(obj, decimal.Decimal):
        return float(obj)  # or str(obj) if you want string representation
    raise TypeError(f"Type {type(obj)} not serializable")

def print_json(data, is_error=False):
    output = json.dumps(data, indent=2, default=custom_json_encoder, ensure_ascii=False)
    if is_error:
        print(output, file=sys.stderr, flush=True)
    else:
        print(output, flush=True)

def connect_and_execute(host, user, password, database, query=None, sql_file=None):
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        if not connection.is_connected():
            print_json({
                "status": "error",
                "message": "Connection failed"
            }, is_error=True)
            return

        # If SQL file is given, read query from file
        if sql_file:
            if not os.path.exists(sql_file):
                print_json({
                    "status": "error",
                    "message": f"SQL file not found: {sql_file}"
                }, is_error=True)
                return
            with open(sql_file, 'r') as f:
                query = f.read()

        if not query:
            print_json({
                "status": "error",
                "message": "No SQL query or file provided"
            }, is_error=True)
            return

        all_results = []

        # MULTI STATEMENT SUPPORT
        if ";" in query.strip().rstrip(";"):
            cursor = connection.cursor()  # No dictionary=True in multi=True
            for result in cursor.execute(query, multi=True):
                if result.with_rows:
                    columns = result.column_names
                    rows = result.fetchall()
                    row_dicts = [dict(zip(columns, row)) for row in rows]
                    all_results.append({
                        "query": result.statement,
                        "result": row_dicts
                    })
                else:
                    all_results.append({
                        "query": result.statement,
                        "rows_affected": result.rowcount
                    })
        else:
            # Single-statement mode with key-value output
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query)
            if cursor.with_rows:
                rows = cursor.fetchall()
                all_results.append({
                    "query": query,
                    "result": rows
                })
            else:
                all_results.append({
                    "query": query,
                    "rows_affected": cursor.rowcount
                })

        connection.commit()
        cursor.close()
        connection.close()

        response = {
            "status": "success",
            "host": host,
            "database": database,
            "results": all_results
        }

        print_json(response)

    except mysql.connector.Error as e:
        print_json({
            "status": "error",
            "message": str(e)
        }, is_error=True)
        sys.exit(1)
    except Exception as e:
        print_json({
            "status": "error",
            "message": f"Unexpected error: {str(e)}"
        }, is_error=True)
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run SQL queries or files and return JSON")

    parser.add_argument('--host', required=True, help='MySQL host')
    parser.add_argument('--user', required=True, help='MySQL username')
    parser.add_argument('--password', required=True, help='MySQL password')
    parser.add_argument('--database', required=True, help='Database name')
    parser.add_argument('--query', help='SQL query to execute')
    parser.add_argument('--sqlfile', help='Path to SQL file to execute')

    args = parser.parse_args()

    connect_and_execute(
        host=args.host,
        user=args.user,
        password=args.password,
        database=args.database,
        query=args.query,
        sql_file=args.sqlfile
    )
