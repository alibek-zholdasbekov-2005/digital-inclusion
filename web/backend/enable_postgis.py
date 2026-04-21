import psycopg2
import sys
try:
    print("Connecting...")
    conn = psycopg2.connect("postgresql://web_db_zbgs_user:j1zzD9pOkPgz8SzwVi7QHBTc3NIcdsba@dpg-d7jglt8sfn5c73blvsqg-a.frankfurt-postgres.render.com:5432/web_db_zbgs")
    conn.autocommit = True
    cur = conn.cursor()
    print("Executing CREATE EXTENSION...")
    cur.execute("CREATE EXTENSION IF NOT EXISTS postgis;")
    print("PostGIS enabled successfully!")
    cur.close()
    conn.close()
except BaseException as e:
    print("Error:", e)
    sys.exit(1)
