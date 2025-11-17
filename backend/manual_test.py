#!/usr/bin/env python3
"""
Manual test script for CSV import functionality
"""
import requests
import os
from pathlib import Path

# Base URL for API
API_URL = 'http://localhost:5000'

# Path to sample CSV
SAMPLE_CSV = Path(__file__).parent.parent / 'sample_transactions.csv'

def test_health():
    """Test health endpoint"""
    print("Testing health endpoint...")
    try:
        response = requests.get(f'{API_URL}/api/health')
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_parse_csv():
    """Test CSV parsing"""
    print("\nTesting CSV parsing...")
    if not SAMPLE_CSV.exists():
        print(f"Sample CSV not found at {SAMPLE_CSV}")
        return False
    
    try:
        with open(SAMPLE_CSV, 'rb') as f:
            files = {'file': ('sample_transactions.csv', f, 'text/csv')}
            response = requests.post(f'{API_URL}/api/csv/parse', files=files)
        
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Columns: {data['columns']}")
            print(f"Detected mapping: {data['detected_mapping']}")
            print(f"Total rows: {data['total_rows']}")
            print(f"Sample data (first row): {data['sample_data'][0] if data['sample_data'] else 'None'}")
            return True
        else:
            print(f"Error: {response.json()}")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_import_csv():
    """Test CSV import"""
    print("\nTesting CSV import...")
    if not SAMPLE_CSV.exists():
        print(f"Sample CSV not found at {SAMPLE_CSV}")
        return False
    
    try:
        with open(SAMPLE_CSV, 'r') as f:
            file_content = f.read()
        
        payload = {
            'file_content': file_content,
            'mapping': {
                'date': 'Date',
                'description': 'Description',
                'amount': 'Amount',
                'category': 'Type'
            }
        }
        
        response = requests.post(
            f'{API_URL}/api/csv/import',
            json=payload
        )
        
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Success: {data['success']}")
            print(f"Transaction count: {data['count']}")
            print(f"First transaction: {data['transactions'][0] if data['transactions'] else 'None'}")
            return True
        else:
            print(f"Error: {response.json()}")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    print("=" * 60)
    print("CSV Import Manual Tests")
    print("=" * 60)
    
    print("\nNote: Make sure the backend server is running on port 5000")
    print("Run: cd backend && source venv/bin/activate && python app.py\n")
    
    results = []
    results.append(("Health Check", test_health()))
    results.append(("CSV Parse", test_parse_csv()))
    results.append(("CSV Import", test_import_csv()))
    
    print("\n" + "=" * 60)
    print("Test Results:")
    print("=" * 60)
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{name}: {status}")
    
    all_passed = all(r[1] for r in results)
    print("=" * 60)
    print(f"\nOverall: {' ALL TESTS PASSED' if all_passed else 'SOME TESTS FAILED'}")

if __name__ == '__main__':
    main()
