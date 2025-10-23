#!/usr/bin/env python3
import sqlite3
import os

def view_database():
    db_path = os.path.join('instance', 'app.db')
    
    if not os.path.exists(db_path):
        print(f"Database file not found at {db_path}")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print("=== DATABASE TABLES ===")
        for table in tables:
            print(f"- {table[0]}")
        
        print("\n=== TABLE CONTENTS ===")
        
        # Show contents of each table
        for table in tables:
            table_name = table[0]
            print(f"\n--- {table_name.upper()} ---")
            
            # Get table schema
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            print("Columns:", [col[1] for col in columns])
            
            # Get table data
            cursor.execute(f"SELECT * FROM {table_name};")
            rows = cursor.fetchall()
            
            if rows:
                for row in rows:
                    print(row)
            else:
                print("(No data)")
        
        conn.close()
        
    except Exception as e:
        print(f"Error viewing database: {e}")

if __name__ == "__main__":
    view_database()
