"""
Debug Database Connection
Direct SQLite inspection to troubleshoot database issues
"""

import sqlite3
import os

def debug_database():
    db_path = 'testgenie.db'
    
    print("🔍 Database Debug Information")
    print("=" * 50)
    
    # Check if file exists and get size
    if os.path.exists(db_path):
        size = os.path.getsize(db_path)
        print(f"📁 Database file: {db_path}")
        print(f"📏 File size: {size} bytes")
        
        if size == 0:
            print("⚠️ Database file is empty!")
            return
    else:
        print(f"❌ Database file not found: {db_path}")
        return
    
    try:
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        print(f"📊 Tables found: {len(tables)}")
        
        if tables:
            print("\n📋 Table Details:")
            for table in tables:
                table_name = table[0]
                print(f"\n🔖 Table: {table_name}")
                
                # Get row count
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                print(f"   📊 Rows: {count}")
                
                # Get column info
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = cursor.fetchall()
                print(f"   📝 Columns: {len(columns)}")
                for col in columns:
                    print(f"      - {col[1]} ({col[2]})")
        else:
            print("❌ No tables found")
            
        # Check the master table directly
        cursor.execute("SELECT * FROM sqlite_master")
        master_rows = cursor.fetchall()
        print(f"\n🗄️ sqlite_master entries: {len(master_rows)}")
        for row in master_rows:
            print(f"   - {row}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error connecting to database: {e}")

if __name__ == "__main__":
    debug_database()
