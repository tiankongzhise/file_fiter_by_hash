import psycopg2
import os
import dotenv

dotenv.load_dotenv()



def main():
    conn = psycopg2.connect(
        host=os.getenv("PG_HOST"),
        port=int(os.getenv("PG_PORT")),
        password=os.getenv("PG_PASSWORD"),
        user=os.getenv("PG_USERNAME"),
        database=os.getenv("PG_DATABASE"),
        # sslmode="require",
    )

    query_sql = 'SELECT VERSION()'

    cur = conn.cursor()
    cur.execute(query_sql)

    version = cur.fetchone()[0]
    print(version)


if __name__ == "__main__":
    main()
