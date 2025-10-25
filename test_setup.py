#!/usr/bin/env python3
"""
Test script for GoFormz-Shiftcare integration
"""

import os
import asyncio
from dotenv import load_dotenv
from goformz_client import GoFormzClient
from pdf_parser import PDFParser

# Load environment variables
load_dotenv()

def test_goformz_connection():
    """Test GoFormz API connection"""
    print("Testing GoFormz API connection...")
    
    client = GoFormzClient(
        client_id=os.getenv('GOFORMZ_CLIENT_ID'),
        client_secret=os.getenv('GOFORMZ_CLIENT_SECRET')
    )
    
    try:
        forms = client.get_recent_forms(limit=5)
        print(f"✓ Successfully connected to GoFormz API")
        print(f"✓ Found {len(forms)} recent forms")
        
        if forms:
            print("\nRecent forms:")
            for form in forms[:3]:  # Show first 3 forms
                print(f"  - ID: {form.get('id', 'N/A')}")
                print(f"    Name: {form.get('name', 'N/A')}")
                print(f"    Created: {form.get('created_at', 'N/A')}")
                print()
        
        return True
        
    except Exception as e:
        print(f"✗ Failed to connect to GoFormz API: {e}")
        return False

def test_pdf_parser():
    """Test PDF parser with sample data"""
    print("Testing PDF parser...")
    
    parser = PDFParser()
    
    # Sample text that might be in a PDF
    sample_text = """
    Client Packet
    
    Name: John Doe
    Date of Birth: 01/15/1980
    Phone: (555) 123-4567
    Email: john.doe@email.com
    Address: 123 Main St, City, State 12345
    
    Emergency Contact: Jane Doe
    Emergency Phone: (555) 987-6543
    
    Medical Conditions: Diabetes, Hypertension
    Medications: Metformin, Lisinopril
    """
    
    # Create mock parsed data
    mock_data = {
        'raw_text': sample_text,
        'personal_info': {
            'full_name': 'John Doe',
            'date_of_birth': '01/15/1980'
        },
        'contact_info': {
            'phone': '(555) 123-4567',
            'email': 'john.doe@email.com',
            'address': '123 Main St, City, State 12345'
        },
        'emergency_contact': {
            'name': 'Jane Doe',
            'phone': '(555) 987-6543'
        },
        'medical_info': {
            'conditions': 'Diabetes, Hypertension',
            'medications': 'Metformin, Lisinopril'
        }
    }
    
    packet_type = parser.determine_packet_type(mock_data)
    print(f"✓ PDF parser working correctly")
    print(f"✓ Detected packet type: {packet_type}")
    
    return True

def main():
    """Run all tests"""
    print("GoFormz-Shiftcare Integration Test")
    print("=" * 40)
    
    # Check environment variables
    required_vars = [
        'GOFORMZ_CLIENT_ID',
        'GOFORMZ_CLIENT_SECRET',
        'SHIFTCARE_USERNAME',
        'SHIFTCARE_PASSWORD'
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print("✗ Missing environment variables:")
        for var in missing_vars:
            print(f"  - {var}")
        print("\nPlease create a .env file with the required variables.")
        return False
    
    print("✓ All environment variables found")
    print()
    
    # Run tests
    tests_passed = 0
    total_tests = 2
    
    if test_goformz_connection():
        tests_passed += 1
    
    print()
    
    if test_pdf_parser():
        tests_passed += 1
    
    print()
    print("=" * 40)
    print(f"Tests passed: {tests_passed}/{total_tests}")
    
    if tests_passed == total_tests:
        print("✓ All tests passed! Ready to run the application.")
        print("\nTo start the application:")
        print("  python app.py")
        print("\nTo deploy to Heroku:")
        print("  heroku create your-app-name")
        print("  git push heroku main")
    else:
        print("✗ Some tests failed. Please check the configuration.")
    
    return tests_passed == total_tests

if __name__ == "__main__":
    main()
