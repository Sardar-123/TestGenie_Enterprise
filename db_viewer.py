"""
TestGenie Database Viewer
Simple script to view all data in the SQLite database
"""

import sqlite3
import json
from datetime import datetime

def view_database():
    """View all data in the TestGenie database"""
    
    print("🗄️ TestGenie Database Viewer")
    print("=" * 50)
    
    try:
        # Connect to the database
        conn = sqlite3.connect('testgenie.db')
        conn.row_factory = sqlite3.Row  # Enable column access by name
        cursor = conn.cursor()
        
        # Get all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print(f"📊 Found {len(tables)} tables in database\n")
        
        for table in tables:
            table_name = table['name']
            print(f"📋 Table: {table_name}")
            print("-" * 30)
            
            # Get table schema
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            column_names = [col['name'] for col in columns]
            
            # Get row count
            cursor.execute(f"SELECT COUNT(*) as count FROM {table_name};")
            row_count = cursor.fetchone()['count']
            
            print(f"   Columns: {', '.join(column_names)}")
            print(f"   Rows: {row_count}")
            
            if row_count > 0:
                # Show first few rows
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 3;")
                rows = cursor.fetchall()
                
                print("   Sample Data:")
                for i, row in enumerate(rows, 1):
                    print(f"   Row {i}:")
                    for col_name in column_names:
                        value = row[col_name]
                        # Truncate long values
                        if isinstance(value, str) and len(value) > 50:
                            value = value[:47] + "..."
                        print(f"     {col_name}: {value}")
                    print()
            
            print()
        
        conn.close()
        
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
    except FileNotFoundError:
        print("❌ Database file 'testgenie.db' not found!")
        print("💡 Run 'python init_db.py' to create the database first.")

def view_table_details(table_name):
    """View detailed data for a specific table"""
    
    print(f"📋 Detailed view of table: {table_name}")
    print("=" * 50)
    
    try:
        conn = sqlite3.connect('testgenie.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Check if table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (table_name,))
        if not cursor.fetchone():
            print(f"❌ Table '{table_name}' not found!")
            return
        
        # Get all rows
        cursor.execute(f"SELECT * FROM {table_name};")
        rows = cursor.fetchall()
        
        if not rows:
            print(f"📭 Table '{table_name}' is empty")
            return
        
        # Get column names
        column_names = rows[0].keys()
        
        print(f"Found {len(rows)} rows\n")
        
        for i, row in enumerate(rows, 1):
            print(f"🔍 Record {i}:")
            for col_name in column_names:
                value = row[col_name]
                
                # Pretty print JSON fields
                if col_name in ['steps', 'tags', 'results', 'test_case_ids'] and value:
                    try:
                        parsed = json.loads(value)
                        print(f"   {col_name}: {json.dumps(parsed, indent=4)}")
                    except (json.JSONDecodeError, TypeError):
                        print(f"   {col_name}: {value}")
                else:
                    print(f"   {col_name}: {value}")
            print("-" * 40)
        
        conn.close()
        
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")

def search_test_cases(search_term=""):
    """Search test cases by title or description"""
    
    print(f"🔍 Searching test cases for: '{search_term}'")
    print("=" * 50)
    
    try:
        conn = sqlite3.connect('testgenie.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        if search_term:
            query = """
            SELECT tc.*, p.name as project_name 
            FROM test_cases tc 
            LEFT JOIN projects p ON tc.project_id = p.id
            WHERE tc.title LIKE ? OR tc.description LIKE ?
            ORDER BY tc.created_at DESC
            """
            cursor.execute(query, (f'%{search_term}%', f'%{search_term}%'))
        else:
            query = """
            SELECT tc.*, p.name as project_name 
            FROM test_cases tc 
            LEFT JOIN projects p ON tc.project_id = p.id
            ORDER BY tc.created_at DESC
            """
            cursor.execute(query)
        
        rows = cursor.fetchall()
        
        if not rows:
            print("📭 No test cases found")
            return
        
        print(f"Found {len(rows)} test cases:\n")
        
        for row in rows:
            print(f"📝 {row['title']}")
            print(f"   ID: {row['id']}")
            print(f"   Project: {row['project_name'] or 'Unknown'}")
            print(f"   Status: {row['status']}")
            print(f"   Priority: {row['priority']}")
            print(f"   Created: {row['created_at']}")
            
            # Show tags if available
            if row['tags']:
                try:
                    tags = json.loads(row['tags'])
                    print(f"   Tags: {', '.join(tags)}")
                except:
                    print(f"   Tags: {row['tags']}")
            
            print()
        
        conn.close()
        
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "overview":
            view_database()
        elif command == "projects":
            view_table_details('projects')
        elif command == "testcases":
            view_table_details('test_cases')
        elif command == "suites":
            view_table_details('test_suites')
        elif command == "runs":
            view_table_details('test_runs')
        elif command == "users":
            view_table_details('users')
        elif command == "search":
            search_term = sys.argv[2] if len(sys.argv) > 2 else ""
            search_test_cases(search_term)
        else:
            print("❌ Unknown command")
            print("\nUsage:")
            print("  python db_viewer.py overview     - Show all tables overview")
            print("  python db_viewer.py projects     - Show all projects")
            print("  python db_viewer.py testcases    - Show all test cases")
            print("  python db_viewer.py suites       - Show all test suites")
            print("  python db_viewer.py runs         - Show all test runs")
            print("  python db_viewer.py users        - Show all users")
            print("  python db_viewer.py search <term> - Search test cases")
    else:
        # Default: show overview
        view_database()
