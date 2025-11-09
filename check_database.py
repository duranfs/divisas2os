#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script to check database contents for client records
"""

import sqlite3
import os

# Check if database exists
db_path = "databases/storage.sqlite"
if not os.path.exists(db_path):
    print("❌ Database file not found at:", db_path)
    exit(1)

print("✅ Database file found")

try:
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check auth_user table
    cursor.execute("SELECT COUNT(*) FROM auth_user")
    user_count = cursor.fetchone()[0]
    print(f"📊 Total users in auth_user: {user_count}")
    
    if user_count > 0:
        cursor.execute("SELECT id, first_name, last_name, email, estado FROM auth_user LIMIT 5")
        users = cursor.fetchall()
        print("\n👥 Sample users:")
        for user in users:
            print(f"  ID: {user[0]}, Name: {user[1]} {user[2]}, Email: {user[3]}, Status: {user[4]}")
    
    # Check clientes table
    cursor.execute("SELECT COUNT(*) FROM clientes")
    client_count = cursor.fetchone()[0]
    print(f"\n📊 Total clients in clientes: {client_count}")
    
    if client_count > 0:
        cursor.execute("SELECT id, user_id, cedula, fecha_registro FROM clientes LIMIT 5")
        clients = cursor.fetchall()
        print("\n🏦 Sample clients:")
        for client in clients:
            print(f"  ID: {client[0]}, User ID: {client[1]}, Cedula: {client[2]}, Date: {client[3]}")
    
    # Check if there are clients with user data
    cursor.execute("""
        SELECT c.id, c.cedula, u.first_name, u.last_name, u.email, u.estado
        FROM clientes c
        JOIN auth_user u ON c.user_id = u.id
        LIMIT 5
    """)
    joined_data = cursor.fetchall()
    
    if joined_data:
        print(f"\n🔗 Clients with user data ({len(joined_data)} found):")
        for data in joined_data:
            print(f"  Client ID: {data[0]}, Cedula: {data[1]}, Name: {data[2]} {data[3]}, Email: {data[4]}, Status: {data[5]}")
    else:
        print("\n❌ No clients found with joined user data")
    
    conn.close()
    
except sqlite3.Error as e:
    print(f"❌ Database error: {e}")
except Exception as e:
    print(f"❌ Unexpected error: {e}")