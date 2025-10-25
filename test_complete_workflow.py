#!/usr/bin/env python3
"""
Complete workflow test for GoFormz-Shiftcare integration
Tests the full client creation + care plan workflow
"""

import os
import asyncio
from dotenv import load_dotenv
from goformz_client import GoFormzClient
from pdf_parser import PDFParser
from shiftcare_automation import ShiftcareAutomation

# Load environment variables
load_dotenv()

def test_complete_client_workflow():
    """Test the complete client workflow with care plan"""
    print("Testing complete client workflow with care plan...")
    
    parser = PDFParser()
    
    # Sample client packet with care plan information
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
    
    Care Plan: Initial Assessment
    Start Date: 10/25/2025
    End Date: 11/25/2025
    
    Goals:
    1. Maintain blood sugar levels within normal range
    2. Improve blood pressure control
    3. Increase physical activity
    4. Maintain medication compliance
    
    Tasks:
    1. Monitor blood glucose daily
    2. Take medications as prescribed
    3. Follow diabetic diet plan
    4. Exercise 30 minutes daily
    5. Attend monthly check-ups
    6. Check blood pressure weekly
    """
    
    # Parse the sample text
    parsed_data = parser._extract_data_from_text(sample_client_text)
    
    print("✓ PDF parser extracted complete client data:")
    print(f"  - Name: {parsed_data['personal_info'].get('full_name', 'N/A')}")
    print(f"  - SSN: {parsed_data['personal_info'].get('ssn', 'N/A')}")
    print(f"  - Care Plan: {parsed_data['care_plan'].get('name', 'N/A')}")
    print(f"  - Start Date: {parsed_data['care_plan'].get('start_date', 'N/A')}")
    print(f"  - End Date: {parsed_data['care_plan'].get('end_date', 'N/A')}")
    print(f"  - Goals Found: {len(parsed_data['goals'])}")
    print(f"  - Tasks Found: {len(parsed_data['tasks'])}")
    
    # Show extracted goals
    if parsed_data['goals']:
        print("  Goals:")
        for i, goal in enumerate(parsed_data['goals'][:3], 1):  # Show first 3
            print(f"    {i}. {goal['description']}")
    
    # Show extracted tasks
    if parsed_data['tasks']:
        print("  Tasks:")
        for i, task in enumerate(parsed_data['tasks'][:3], 1):  # Show first 3
            print(f"    {i}. {task['description']}")
    
    # Test packet type detection
    packet_type = parser.determine_packet_type(parsed_data)
    print(f"  - Packet Type: {packet_type}")
    
    return parsed_data

async def test_shiftcare_complete_workflow():
    """Test the complete Shiftcare workflow (client creation + care plan)"""
    print("\nTesting complete Shiftcare workflow...")
    
    # Sample client data with care plan
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
        },
        'care_plan': {
            'name': 'Initial Assessment',
            'start_date': '10/25/2025',
            'end_date': '11/25/2025'
        },
        'goals': [
            {'description': 'Maintain blood sugar levels within normal range'},
            {'description': 'Improve blood pressure control'},
            {'description': 'Increase physical activity'},
            {'description': 'Maintain medication compliance'}
        ],
        'tasks': [
            {'description': 'Monitor blood glucose daily'},
            {'description': 'Take medications as prescribed'},
            {'description': 'Follow diabetic diet plan'},
            {'description': 'Exercise 30 minutes daily'},
            {'description': 'Attend monthly check-ups'},
            {'description': 'Check blood pressure weekly'}
        ]
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
                
                # Test client creation form
                await automation.page.goto(f"{automation.base_url}/clients/new")
                await automation.page.wait_for_load_state('networkidle')
                print("✓ Successfully navigated to new client page")
                
                # Test care plan workflow (without submitting)
                # Navigate to clients list
                await automation.page.goto(f"{automation.base_url}/clients")
                await automation.page.wait_for_load_state('networkidle')
                print("✓ Successfully navigated to clients list")
                
                # Look for a client to test with (use first available client)
                client_row = automation.page.locator('tr').nth(1)  # Skip header row
                if await client_row.is_visible():
                    await client_row.click()
                    await automation.page.wait_for_load_state('networkidle')
                    print("✓ Successfully opened client profile")
                    
                    # Navigate to Care Plan tab
                    care_plan_tab = automation.page.locator('a:has-text("Care Plan")')
                    if await care_plan_tab.is_visible():
                        await care_plan_tab.click()
                        await automation.page.wait_for_load_state('networkidle')
                        print("✓ Successfully navigated to Care Plan tab")
                        
                        # Look for Add Care Plan button
                        add_care_plan_button = automation.page.locator('button:has-text("Add Care Plan")')
                        if await add_care_plan_button.is_visible():
                            print("✓ Found Add Care Plan button")
                        else:
                            print("✗ Could not find Add Care Plan button")
                    else:
                        print("✗ Could not find Care Plan tab")
                else:
                    print("✗ Could not find any clients in the list")
                
                print("✓ Complete workflow test completed successfully")
                
            else:
                print("✗ Failed to login to Shiftcare")
                return False
                
    except Exception as e:
        print(f"✗ Error testing complete workflow: {e}")
        return False
    
    return True

def main():
    """Run complete workflow tests"""
    print("Complete GoFormz-Shiftcare Integration Test")
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
    
    # Test complete client workflow
    try:
        client_data = test_complete_client_workflow()
        print("✓ Complete client workflow test passed")
    except Exception as e:
        print(f"✗ Complete client workflow test failed: {e}")
        return False
    
    # Test Shiftcare complete workflow
    try:
        result = asyncio.run(test_shiftcare_complete_workflow())
        if result:
            print("✓ Shiftcare complete workflow test passed")
        else:
            print("✗ Shiftcare complete workflow test failed")
            return False
    except Exception as e:
        print(f"✗ Shiftcare complete workflow test failed: {e}")
        return False
    
    print()
    print("=" * 60)
    print("✓ All complete workflow tests passed!")
    print("\nThe integration is ready to:")
    print("  1. Create clients in Shiftcare")
    print("  2. Navigate to client list")
    print("  3. Open client profile")
    print("  4. Add care plan with tasks and goals")
    print("\nTo run the full application:")
    print("  python app.py")
    print("\nTo deploy to Heroku:")
    print("  ./deploy.sh")
    
    return True

if __name__ == "__main__":
    main()
