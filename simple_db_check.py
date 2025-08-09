"""
Simple Database Checker
Quick way to see what's in your TestGenie database
"""

def check_db():
    try:
        import sqlite3
        
        # Connect to database
        conn = sqlite3.connect('testgenie.db')
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        print("🗄️ TestGenie Database Status")
        print("=" * 30)
        print(f"📊 Tables found: {len(tables)}")
        
        if not tables:
            print("❌ No tables found - database might be empty")
            print("💡 Try running: python init_db.py")
            return
        
        # Check each table
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            
            print(f"📋 {table_name}: {count} rows")
            
            # Show a sample row if exists
            if count > 0:
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 1")
                sample = cursor.fetchone()
                print(f"   Sample: {sample}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    check_db()
