import sqlite3
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.abspath(os.path.join(BASE_DIR, "../employee_attrition.db"))
SQL_PATH = os.path.abspath(os.path.join(BASE_DIR, "../employee_attrition_dump.sql"))

def dump_database():
    if not os.path.exists(DB_PATH):
        print("Database not found. Please run data_cleaning.py first.")
        return
        
    print(f"Connecting to SQLite database at {DB_PATH}...")
    conn = sqlite3.connect(DB_PATH)
    
    print(f"Exporting database commands and records to {SQL_PATH}...")
    with open(SQL_PATH, 'w', encoding='utf-8') as f:
        # iterdump generates the SQL commands to replicate the database
        for line in conn.iterdump():
            f.write('%s\n' % line)
            
    print("Database dump complete. File is now human-readable.")
    conn.close()

if __name__ == "__main__":
    dump_database()
