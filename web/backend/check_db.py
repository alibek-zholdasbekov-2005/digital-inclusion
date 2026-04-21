import psycopg2
import sys
try:
    conn = psycopg2.connect("postgresql://web_db_zbgs_user:j1zzD9pOkPgz8SzwVi7QHBTc3NIcdsba@dpg-d7jglt8sfn5c73blvsqg-a.frankfurt-postgres.render.com:5432/web_db_zbgs")
    cur = conn.cursor()
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")
    tables = cur.fetchall()
    print("Tables:", [t[0] for t in tables])
    
    cur.execute("SELECT count(*) FROM django_migrations;")
    migrations = cur.fetchone()[0]
    print("Number of applied migrations:", migrations)
    
    cur.close()
    conn.close()
except BaseException as e:
    print("Error:", e)
    sys.exit(1)
