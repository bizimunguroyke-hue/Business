#!/usr/bin/env python3
"""
Test script to verify that admin, manager, and staff roles have full access
"""

import requests
import json
import sys

# Test configuration
BASE_URL = "http://localhost:5000"  # Adjust if your backend runs on different port

def test_role_access(username, password, role_name):
    """Test access for a specific role"""
    print(f"\n=== Testing {role_name} Role Access ===")
    
    # Login
    login_data = {
        "username": username,
        "password": password
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        if response.status_code != 200:
            print(f"❌ Login failed for {role_name}: {response.status_code}")
            return False
            
        token = response.json().get('access_token')
        headers = {'Authorization': f'Bearer {token}'}
        
        # Test various endpoints that should be accessible
        test_endpoints = [
            ('/products', 'GET'),
            ('/customers', 'GET'),
            ('/suppliers', 'GET'),
            ('/orders', 'GET'),
            ('/invoices', 'GET'),
            ('/warehouses', 'GET'),
            ('/projects', 'GET'),
            ('/expenses/expenses', 'GET'),
            ('/employees', 'GET'),
            ('/assets', 'GET'),
        ]
        
        success_count = 0
        total_count = len(test_endpoints)
        
        for endpoint, method in test_endpoints:
            try:
                if method == 'GET':
                    response = requests.get(f"{BASE_URL}{endpoint}", headers=headers)
                elif method == 'POST':
                    response = requests.post(f"{BASE_URL}{endpoint}", headers=headers, json={})
                
                if response.status_code == 200:
                    print(f"✅ {method} {endpoint} - Access granted")
                    success_count += 1
                elif response.status_code == 403:
                    print(f"❌ {method} {endpoint} - Access denied (403)")
                else:
                    print(f"⚠️  {method} {endpoint} - Status: {response.status_code}")
                    
            except Exception as e:
                print(f"❌ {method} {endpoint} - Error: {str(e)}")
        
        print(f"\n📊 {role_name} Access Summary: {success_count}/{total_count} endpoints accessible")
        return success_count == total_count
        
    except Exception as e:
        print(f"❌ Error testing {role_name}: {str(e)}")
        return False

def main():
    """Main test function"""
    print("🔍 Testing Full Access Implementation")
    print("=" * 50)
    
    # Test different roles (you'll need to create these users or use existing ones)
    test_users = [
        # Format: (username, password, role_name)
        # Update these with actual user credentials from your system
        ("admin", "admin123", "Admin"),
        ("manager", "manager123", "Manager"), 
        ("staff", "staff123", "Staff"),
    ]
    
    all_passed = True
    
    for username, password, role_name in test_users:
        success = test_role_access(username, password, role_name)
        if not success:
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All tests passed! Full access implementation is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the implementation.")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
