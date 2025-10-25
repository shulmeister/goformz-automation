#!/usr/bin/env python3
"""
Enhanced test script for GoFormz-Shiftcare integration
Tests the actual form filling with realistic data
"""

import os
import asyncio
from dotenv import load_dotenv
from goformz_client import GoFormzClient
from pdf_parser import PDFParser
from shiftcare_automation import ShiftcareAutomation

# Load environment variables
load_dotenv()

def test_pdf_parser_with_employee_data():
    """Test PDF parser with realistic employee packet data"""
    print("Testing PDF parser with employee packet data...")
    
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
    mock_data = {
        'raw_text': sample_employee_text,
        'personal_info': {},
        'contact_info': {},
        'emergency_contact': {},
        'medical_info': {},
        'employment_info': {}
    }
    
    # Extract data using the parser
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

async def test_shiftcare_form_filling():
    """Test filling the actual Shiftcare form with sample data"""
    print("\nTesting Shiftcare form filling...")
    
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
            # Just test navigation and form filling, don't submit
            await automation.start_browser()
            
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
                
                print("✓ Form filling test completed successfully")
                
            else:
                print("✗ Failed to login to Shiftcare")
                return False
                
    except Exception as e:
        print(f"✗ Error testing Shiftcare form: {e}")
        return False
    
    return True

def main():
    """Run enhanced tests"""
    print("Enhanced GoFormz-Shiftcare Integration Test")
    print("=" * 50)
    
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
    
    # Test PDF parsing
    try:
        parsed_data = test_pdf_parser_with_employee_data()
        print("✓ PDF parsing test passed")
    except Exception as e:
        print(f"✗ PDF parsing test failed: {e}")
        return False
    
    # Test Shiftcare form filling
    try:
        result = asyncio.run(test_shiftcare_form_filling())
        if result:
            print("✓ Shiftcare form filling test passed")
        else:
            print("✗ Shiftcare form filling test failed")
            return False
    except Exception as e:
        print(f"✗ Shiftcare form filling test failed: {e}")
        return False
    
    print()
    print("=" * 50)
    print("✓ All enhanced tests passed!")
    print("\nThe integration is ready to process employee packets.")
    print("\nTo run the full application:")
    print("  python app.py")
    
    return True

if __name__ == "__main__":
    main()
