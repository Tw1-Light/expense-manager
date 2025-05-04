import csv
import pandas as pd
from db.database import connect_db


def export_to_csv(filename="expenses_export.csv"):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM expenses')
    data = cursor.fetchall()
    headers = [desc[0] for desc in cursor.description]

    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(data)

    print(f"Exported to {filename}")
    conn.close()


def export_to_excel(filename="expenses_export.xlsx"):
    conn = connect_db()
    df = pd.read_sql_query("SELECT * FROM expenses", conn)
    df.to_excel(filename, index=False)
    print(f"Exported to {filename}")
    conn.close()
