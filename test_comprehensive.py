#!/usr/bin/env python3
"""
Comprehensive test script for GoFormz-Shiftcare integration
Tests both client and employee packet processing with realistic data
"""

import os
import asyncio
from dotenv import load_dotenv
from goformz_client import GoFormzClient
from pdf_parser import PDFParser
from shiftcare_automation import ShiftcareAutomation

# Load environment variables
load_dotenv()

def test_pdf_parser_with_client_data():
    """Test PDF parser with realistic client packet data"""
    print("Testing PDF parser with client packet data...")
    
    parser = PDFParser()
    
    # Sample client packet text
    sample_client_text = """
    Client Packet
    
    Name: Mr. John Smith
    Preferred Name: Johnny
    Date of Birth: 05/15/1975
    Gender: Male
    SSN: 123-45-6789
    Place of Birth: Denver, Colorado
    Languages: English, Spanish
    
    Primary Phone: (555) 123-4567
    Secondary Phone: (555) 123-4568
    Primary Email: john.smith@email.com
    Secondary Email: johnny.smith@gmail.com
    
    Address: 123 Main Street
    Unit: Apt 4B
    Postal Code: 80202
    
    Preferred Contact Method: Phone
    
    Religion: Christian
    Marital Status: Married
    Nationality: American
    Ethnicity: Caucasian
    
    Emergency Contact: Jane Smith
    Emergency Phone: (555) 987-6543
    
    Medical Conditions: Diabetes, Hypertension
    Medications: Metformin, Lisinopril
    """
    
    # Parse the sample text
    parsed_data = parser._extract_data_from_text(sample_client_text)
    
    print("✓ PDF parser extracted client data:")
    print(f"  - Name: {parsed_data['personal_info'].get('full_name', 'N/A')}")
    print(f"  - Preferred Name: {parsed_data['personal_info'].get('preferred_name', 'N/A')}")
    print(f"  - Salutation: {parsed_data['personal_info'].get('salutation', 'N/A')}")
    print(f"  - Gender: {parsed_data['personal_info'].get('gender', 'N/A')}")
    print(f"  - SSN: {parsed_data['personal_info'].get('ssn', 'N/A')}")
    print(f"  - DOB: {parsed_data['personal_info'].get('date_of_birth', 'N/A')}")
    print(f"  - Place of Birth: {parsed_data['personal_info'].get('place_of_birth', 'N/A')}")
    print(f"  - Languages: {parsed_data['personal_info'].get('languages', 'N/A')}")
    print(f"  - Religion: {parsed_data['personal_info'].get('religion', 'N/A')}")
    print(f"  - Marital Status: {parsed_data['personal_info'].get('marital_status', 'N/A')}")
    print(f"  - Nationality: {parsed_data['personal_info'].get('nationality', 'N/A')}")
    print(f"  - Ethnicity: {parsed_data['personal_info'].get('ethnicity', 'N/A')}")
    print(f"  - Primary Phone: {parsed_data['contact_info'].get('phone', 'N/A')}")
    print(f"  - Secondary Phone: {parsed_data['contact_info'].get('secondary_phone', 'N/A')}")
    print(f"  - Primary Email: {parsed_data['contact_info'].get('email', 'N/A')}")
    print(f"  - Secondary Email: {parsed_data['contact_info'].get('secondary_email', 'N/A')}")
    print(f"  - Address: {parsed_data['contact_info'].get('address', 'N/A')}")
    print(f"  - Unit: {parsed_data['contact_info'].get('unit_apartment', 'N/A')}")
    print(f"  - Postal Code: {parsed_data['contact_info'].get('postal_code', 'N/A')}")
    print(f"  - Preferred Contact: {parsed_data['contact_info'].get('preferred_contact_method', 'N/A')}")
    print(f"  - Emergency Contact: {parsed_data['emergency_contact'].get('name', 'N/A')}")
    print(f"  - Emergency Phone: {parsed_data['emergency_contact'].get('phone', 'N/A')}")
    print(f"  - Medical Conditions: {parsed_data['medical_info'].get('conditions', 'N/A')}")
    print(f"  - Medications: {parsed_data['medical_info'].get('medications', 'N/A')}")
    
    # Test packet type detection
    packet_type = parser.determine_packet_type(parsed_data)
    print(f"  - Packet Type: {packet_type}")
    
    return parsed_data

def test_pdf_parser_with_employee_data():
    """Test PDF parser with realistic employee packet data"""
    print("\nTesting PDF parser with employee packet data...")
    
    parser = PDFParser()
    
    # Sample employee packet text
    sample_employee_text = """
    Employee Packet
    
    Name: Dr. Sarah Johnson
    Date of Birth: 03/22/1985
    Gender: Female
    Phone: (555) 234-5678
    Email: sarah.johnson@email.com
    Address: 456 Oak Street, Denver, CO 80202
    
    Position: Registered Nurse
    Department: Home Care
    Employment Type: Full-time
    
    Emergency Contact: Michael Johnson
    Emergency Phone: (555) 234-5679
    
    Medical Conditions: None
    Medications: None
    """
    
    # Parse the sample text
    parsed_data = parser._extract_data_from_text(sample_employee_text)
    
    print("✓ PDF parser extracted employee data:")
    print(f"  - Name: {parsed_data['personal_info'].get('full_name', 'N/A')}")
    print(f"  - Salutation: {parsed_data['personal_info'].get('salutation', 'N/A')}")
    print(f"  - Gender: {parsed_data['personal_info'].get('gender', 'N/A')}")
    print(f"  - DOB: {parsed_data['personal_info'].get('date_of_birth', 'N/A')}")
    print(f"  - Phone: {parsed_data['contact_info'].get('phone', 'N/A')}")
    print(f"  - Email: {parsed_data['contact_info'].get('email', 'N/A')}")
    print(f"  - Position: {parsed_data['employment_info'].get('position', 'N/A')}")
    print(f"  - Employment Type: {parsed_data['employment_info'].get('employment_type', 'N/A')}")
    
    # Test packet type detection
    packet_type = parser.determine_packet_type(parsed_data)
    print(f"  - Packet Type: {packet_type}")
    
    return parsed_data

async def test_shiftcare_client_form_filling():
    """Test filling the actual Shiftcare client form with sample data"""
    print("\nTesting Shiftcare client form filling...")
    
    # Sample client data
    client_data = {
        'personal_info': {
            'full_name': 'Mr. John Smith',
            'salutation': 'Mr',
            'preferred_name': 'Johnny',
            'gender': 'Male',
            'ssn': '123-45-6789',
            'date_of_birth': '05/15/1975',
            'place_of_birth': 'Denver, Colorado',
            'languages': 'English, Spanish',
            'religion': 'Christian',
            'marital_status': 'Married',
            'nationality': 'American',
            'ethnicity': 'Caucasian'
        },
        'contact_info': {
            'phone': '(555) 123-4567',
            'secondary_phone': '(555) 123-4568',
            'email': 'john.smith@email.com',
            'secondary_email': 'johnny.smith@gmail.com',
            'address': '123 Main Street',
            'unit_apartment': 'Apt 4B',
            'postal_code': '80202',
            'preferred_contact_method': 'Phone'
        },
        'emergency_contact': {
            'name': 'Jane Smith',
            'phone': '(555) 987-6543'
        },
        'medical_info': {
            'conditions': 'Diabetes, Hypertension',
            'medications': 'Metformin, Lisinopril'
        }
    }
    
    # Test the automation (without actually submitting)
    automation = ShiftcareAutomation(
        username=os.getenv('SHIFTCARE_USERNAME'),
        password=os.getenv('SHIFTCARE_PASSWORD')
    )
    
    try:
        async with automation:
            # Test login
            login_success = await automation.login()
            if login_success:
                print("✓ Successfully logged into Shiftcare")
                
                # Navigate to new client page
                await automation.page.goto(f"{automation.base_url}/clients/new")
                await automation.page.wait_for_load_state('networkidle')
                
                print("✓ Successfully navigated to new client page")
                
                # Test form field detection
                name_parts = client_data['personal_info']['full_name'].strip().split()
                
                # Check if form fields are present
                first_name_field = automation.page.locator('input[placeholder*="First Name"]')
                last_name_field = automation.page.locator('input[placeholder*="Last/Family Name"]')
                email_field = automation.page.locator('input[placeholder*="Email"]')
                ssn_field = automation.page.locator('input[placeholder*="Social Security Number"]')
                
                if await first_name_field.is_visible():
                    print("✓ First name field detected")
                if await last_name_field.is_visible():
                    print("✓ Last name field detected")
                if await email_field.is_visible():
                    print("✓ Email field detected")
                if await ssn_field.is_visible():
                    print("✓ SSN field detected")
                
                # Test filling form fields (without submitting)
                if len(name_parts) >= 1:
                    await first_name_field.fill(name_parts[0])
                    print(f"✓ Filled first name: {name_parts[0]}")
                
                if len(name_parts) >= 2:
                    await last_name_field.fill(name_parts[-1])
                    print(f"✓ Filled last name: {name_parts[-1]}")
                
                if client_data['contact_info'].get('email'):
                    await email_field.fill(client_data['contact_info']['email'])
                    print(f"✓ Filled email: {client_data['contact_info']['email']}")
                
                if client_data['personal_info'].get('ssn'):
                    await ssn_field.fill(client_data['personal_info']['ssn'])
                    print(f"✓ Filled SSN: {client_data['personal_info']['ssn']}")
                
                print("✓ Client form filling test completed successfully")
                
            else:
                print("✗ Failed to login to Shiftcare")
                return False
                
    except Exception as e:
        print(f"✗ Error testing Shiftcare client form: {e}")
        return False
    
    return True

async def test_shiftcare_employee_form_filling():
    """Test filling the actual Shiftcare employee form with sample data"""
    print("\nTesting Shiftcare employee form filling...")
    
    # Sample employee data
    employee_data = {
        'personal_info': {
            'full_name': 'Dr. Sarah Johnson',
            'salutation': 'Dr',
            'gender': 'Female',
            'date_of_birth': '03/22/1985'
        },
        'contact_info': {
            'phone': '(555) 234-5678',
            'email': 'sarah.johnson@email.com',
            'address': '456 Oak Street, Denver, CO 80202'
        },
        'employment_info': {
            'position': 'Registered Nurse',
            'department': 'Home Care',
            'employment_type': 'Full-time'
        }
    }
    
    # Test the automation (without actually submitting)
    automation = ShiftcareAutomation(
        username=os.getenv('SHIFTCARE_USERNAME'),
        password=os.getenv('SHIFTCARE_PASSWORD')
    )
    
    try:
        async with automation:
            # Test login
            login_success = await automation.login()
            if login_success:
                print("✓ Successfully logged into Shiftcare")
                
                # Navigate to new staff page
                await automation.page.goto(f"{automation.base_url}/users/staff/new")
                await automation.page.wait_for_load_state('networkidle')
                
                print("✓ Successfully navigated to new staff page")
                
                # Test form field detection
                name_parts = employee_data['personal_info']['full_name'].strip().split()
                
                # Check if form fields are present
                first_name_field = automation.page.locator('input[placeholder*="First Name"]')
                last_name_field = automation.page.locator('input[placeholder*="Last/Family Name"]')
                email_field = automation.page.locator('input[placeholder*="Email"]')
                
                if await first_name_field.is_visible():
                    print("✓ First name field detected")
                if await last_name_field.is_visible():
                    print("✓ Last name field detected")
                if await email_field.is_visible():
                    print("✓ Email field detected")
                
                # Test filling form fields (without submitting)
                if len(name_parts) >= 1:
                    await first_name_field.fill(name_parts[0])
                    print(f"✓ Filled first name: {name_parts[0]}")
                
                if len(name_parts) >= 2:
                    await last_name_field.fill(name_parts[-1])
                    print(f"✓ Filled last name: {name_parts[-1]}")
                
                if employee_data['contact_info'].get('email'):
                    await email_field.fill(employee_data['contact_info']['email'])
                    print(f"✓ Filled email: {employee_data['contact_info']['email']}")
                
                print("✓ Employee form filling test completed successfully")
                
            else:
                print("✗ Failed to login to Shiftcare")
                return False
                
    except Exception as e:
        print(f"✗ Error testing Shiftcare employee form: {e}")
        return False
    
    return True

def main():
    """Run comprehensive tests"""
    print("Comprehensive GoFormz-Shiftcare Integration Test")
    print("=" * 60)
    
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
    
    # Test PDF parsing for both client and employee
    try:
        client_data = test_pdf_parser_with_client_data()
        print("✓ Client PDF parsing test passed")
    except Exception as e:
        print(f"✗ Client PDF parsing test failed: {e}")
        return False
    
    try:
        employee_data = test_pdf_parser_with_employee_data()
        print("✓ Employee PDF parsing test passed")
    except Exception as e:
        print(f"✗ Employee PDF parsing test failed: {e}")
        return False
    
    # Test Shiftcare form filling for both client and employee
    try:
        client_result = asyncio.run(test_shiftcare_client_form_filling())
        if client_result:
            print("✓ Shiftcare client form filling test passed")
        else:
            print("✗ Shiftcare client form filling test failed")
            return False
    except Exception as e:
        print(f"✗ Shiftcare client form filling test failed: {e}")
        return False
    
    try:
        employee_result = asyncio.run(test_shiftcare_employee_form_filling())
        if employee_result:
            print("✓ Shiftcare employee form filling test passed")
        else:
            print("✗ Shiftcare employee form filling test failed")
            return False
    except Exception as e:
        print(f"✗ Shiftcare employee form filling test failed: {e}")
        return False
    
    print()
    print("=" * 60)
    print("✓ All comprehensive tests passed!")
    print("\nThe integration is ready to process both client and employee packets.")
    print("\nTo run the full application:")
    print("  python app.py")
    print("\nTo deploy to Heroku:")
    print("  ./deploy.sh")
    
    return True

if __name__ == "__main__":
    main()
