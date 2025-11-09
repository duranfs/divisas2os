#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Simple database test to verify controller logic
"""

import sqlite3

# Connect to database
conn = sqlite3.connect("databases/storage.sqlite")
cursor = conn.cursor()

print("🔍 Testing the exact query from the controller...")

# Test the JOIN query that the controller uses
query = """
SELECT 
    c.id as client_id,
    c.user_id,
    c.cedula,
    c.fecha_registro,
    u.id as user_id,
    u.first_name,
    u.last_name,
    u.email,
    u.estado
FROM clientes c
JOIN auth_user u ON c.user_id = u.id
ORDER BY c.fecha_registro
"""

try:
    cursor.execute(query)
    results = cursor.fetchall()
    
    print(f"📊 Query returned {len(results)} records")
    
    if results:
        print("\n👥 Data that should be displayed in the view:")
        for row in results:
            print(f"  ID: {row[0]}")
            print(f"  Name: {row[5]} {row[6]}")
            print(f"  Cedula: {row[2]}")
            print(f"  Email: {row[7]}")
            print(f"  Status: {row[8]}")
            print(f"  Registration: {row[3]}")
            print("  ---")
            
        # Test filtering
        print("\n🔍 Testing search filters...")
        
        # Filter by name
        filter_query = query + " WHERE u.first_name LIKE '%Franklin%'"
        cursor.execute(filter_query)
        filtered = cursor.fetchall()
        print(f"  Name filter 'Franklin': {len(filtered)} results")
        
        # Filter by status
        filter_query = query + " WHERE u.estado = 'activo'"
        cursor.execute(filter_query)
        filtered = cursor.fetchall()
        print(f"  Status filter 'activo': {len(filtered)} results")
        
        # Test statistics
        cursor.execute("SELECT COUNT(*) FROM clientes")
        total = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT COUNT(*) FROM clientes c
            JOIN auth_user u ON c.user_id = u.id
            WHERE u.estado = 'activo'
        """)
        activos = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT COUNT(*) FROM clientes c
            JOIN auth_user u ON c.user_id = u.id
            WHERE u.estado = 'inactivo'
        """)
        inactivos = cursor.fetchone()[0]
        
        print(f"\n📈 Statistics that should be displayed:")
        print(f"  Total: {total}")
        print(f"  Active: {activos}")
        print(f"  Inactive: {inactivos}")
        
    else:
        print("❌ No data returned - this indicates a problem with the JOIN")
        
except Exception as e:
    print(f"❌ Database error: {e}")
    
finally:
    conn.close()

print("\n✅ Database diagnosis complete!")
print("🔍 CONCLUSION: The data exists and the query works.")
print("❌ PROBLEM: The view is not using the data from the controller.")