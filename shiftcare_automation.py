import asyncio
import logging
from typing import Dict, Any, Optional
from playwright.async_api import async_playwright, Browser, Page

logger = logging.getLogger(__name__)

class ShiftcareAutomation:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.base_url = "https://us.shiftcare.com"
        self.browser = None
        self.page = None
    
    async def __aenter__(self):
        """Async context manager entry"""
        await self.start_browser()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close_browser()
    
    async def start_browser(self):
        """Start browser and navigate to login page"""
        try:
            playwright = await async_playwright().start()
            self.browser = await playwright.chromium.launch(headless=True)
            self.page = await self.browser.new_page()
            
            # Navigate to login page
            await self.page.goto(f"{self.base_url}/users/sign_in")
            await self.page.wait_for_load_state('networkidle')
            
        except Exception as e:
            logger.error(f"Failed to start browser: {e}")
            raise
    
    async def close_browser(self):
        """Close browser"""
        if self.browser:
            await self.browser.close()
    
    async def login(self) -> bool:
        """Login to Shiftcare"""
        try:
            # Fill in login form
            await self.page.fill('input[name="user[email]"]', self.username)
            await self.page.fill('input[name="user[password]"]', self.password)
            
            # Click sign in button
            await self.page.click('input[type="submit"]')
            
            # Wait for redirect after login
            await self.page.wait_for_load_state('networkidle')
            
            # Check if login was successful
            if "dashboard" in self.page.url or "clients" in self.page.url:
                logger.info("Successfully logged in to Shiftcare")
                return True
            else:
                logger.error("Login failed - not redirected to dashboard")
                return False
                
        except Exception as e:
            logger.error(f"Login failed: {e}")
            return False
    
    async def create_client(self, client_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new client in Shiftcare"""
        try:
            # Ensure we're logged in
            if not await self._ensure_logged_in():
                return {"error": "Failed to login"}
            
            # Navigate to new client page
            await self.page.goto(f"{self.base_url}/clients/new")
            await self.page.wait_for_load_state('networkidle')
            
            # Fill in client information
            personal_info = client_data.get('personal_info', {})
            contact_info = client_data.get('contact_info', {})
            emergency_contact = client_data.get('emergency_contact', {})
            medical_info = client_data.get('medical_info', {})
            
            # Social Security Number
            if personal_info.get('ssn'):
                await self.page.fill('input[placeholder*="Social Security Number"]', personal_info['ssn'])
            
            # Name fields - handle salutation and name parts
            if personal_info.get('full_name'):
                name_parts = personal_info['full_name'].strip().split()
                
                # Set salutation (default to Mr if not specified)
                salutation = personal_info.get('salutation', 'Mr')
                await self.page.select_option('select[name*="salutation"]', salutation)
                
                # Fill name fields
                if len(name_parts) >= 1:
                    await self.page.fill('input[placeholder*="First Name"]', name_parts[0])
                if len(name_parts) >= 2:
                    await self.page.fill('input[placeholder*="Last/Family Name"]', name_parts[-1])
                if len(name_parts) >= 3:
                    await self.page.fill('input[placeholder*="Middle Name"]', ' '.join(name_parts[1:-1]))
            
            # Display Name (use first name if not specified)
            display_name = personal_info.get('display_name', personal_info.get('full_name', '').split()[0] if personal_info.get('full_name') else '')
            if display_name:
                await self.page.fill('input[placeholder*="Display Name"]', display_name)
            
            # Preferred Name
            if personal_info.get('preferred_name'):
                await self.page.fill('input[placeholder*="Preferred Name"]', personal_info['preferred_name'])
            
            # Gender
            gender = personal_info.get('gender', '')
            if gender:
                await self.page.select_option('select[placeholder*="Gender"]', gender)
            
            # Date of Birth
            if personal_info.get('date_of_birth'):
                dob = personal_info['date_of_birth']
                await self.page.fill('input[placeholder*="Date Of Birth"]', dob)
            
            # Primary Address
            if contact_info.get('address'):
                await self.page.fill('input[placeholder*="Enter Address"]', contact_info['address'])
            
            # Unit/Apartment Number
            if contact_info.get('unit_apartment'):
                await self.page.fill('input[placeholder*="Unit/Apartment No"]', contact_info['unit_apartment'])
            
            # Postal Code
            if contact_info.get('postal_code'):
                await self.page.fill('input[placeholder*="Postal Code"]', contact_info['postal_code'])
            
            # Mobile Number
            if contact_info.get('phone'):
                await self.page.fill('input[placeholder*="Mobile Number"]', contact_info['phone'])
            
            # Phone Number (secondary)
            if contact_info.get('secondary_phone'):
                await self.page.fill('input[placeholder*="Phone Number"]', contact_info['secondary_phone'])
            
            # Email
            if contact_info.get('email'):
                await self.page.fill('input[placeholder*="Email"]', contact_info['email'])
            
            # Secondary Email
            if contact_info.get('secondary_email'):
                await self.page.fill('input[placeholder*="Secondary Email"]', contact_info['secondary_email'])
            
            # Preferred Contact Method
            if contact_info.get('preferred_contact_method'):
                await self.page.select_option('select[placeholder*="Preferred Contact Method"]', contact_info['preferred_contact_method'])
            
            # Place of Birth
            if personal_info.get('place_of_birth'):
                await self.page.fill('input[placeholder*="Place of Birth"]', personal_info['place_of_birth'])
            
            # Languages
            if personal_info.get('languages'):
                await self.page.fill('input[placeholder*="Languages"]', personal_info['languages'])
            
            # Religion
            if personal_info.get('religion'):
                await self.page.select_option('select[placeholder*="Religion"]', personal_info['religion'])
            
            # Marital Status
            if personal_info.get('marital_status'):
                await self.page.select_option('select[placeholder*="Marital Status"]', personal_info['marital_status'])
            
            # Nationality
            if personal_info.get('nationality'):
                await self.page.select_option('select[placeholder*="Nationality"]', personal_info['nationality'])
            
            # Ethnicity
            if personal_info.get('ethnicity'):
                await self.page.select_option('select[placeholder*="Ethnicity"]', personal_info['ethnicity'])
            
            # Sexuality
            if personal_info.get('sexuality'):
                await self.page.select_option('select[placeholder*="Sexuality"]', personal_info['sexuality'])
            
            # Teams
            if personal_info.get('team'):
                await self.page.select_option('select[placeholder*="Teams"]', personal_info['team'])
            
            # Client status - uncheck "Client is a prospect" by default
            prospect_checkbox = self.page.locator('input[name*="prospect"]')
            if await prospect_checkbox.is_checked():
                await prospect_checkbox.uncheck()
            
            # Submit the form
            await self.page.click('button:has-text("Create")')
            await self.page.wait_for_load_state('networkidle')
            
            # Check if client was created successfully
            current_url = self.page.url
            if "/clients/new" not in current_url:
                logger.info("Client created successfully")
                return {"success": True, "message": "Client created successfully"}
            else:
                # Check for error messages
                error_elements = await self.page.query_selector_all('.error, .alert-danger, [class*="error"]')
                if error_elements:
                    error_text = await error_elements[0].text_content()
                    logger.error(f"Failed to create client: {error_text}")
                    return {"error": f"Failed to create client: {error_text}"}
                else:
                    logger.error("Failed to create client - unknown error")
                    return {"error": "Failed to create client - unknown error"}
                
        except Exception as e:
            logger.error(f"Error creating client: {e}")
            return {"error": str(e)}
    
    async def create_client_with_care_plan(self, client_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new client and then add a care plan"""
        try:
            # First create the client
            client_result = await self.create_client(client_data)
            
            if not client_result.get('success'):
                return client_result
            
            # Wait a moment for the client to be created
            await asyncio.sleep(2)
            
            # Now navigate to client list and find the newly created client
            care_plan_result = await self.add_care_plan_to_client(client_data)
            
            if care_plan_result.get('success'):
                return {
                    "success": True, 
                    "message": "Client created and care plan added successfully",
                    "client_result": client_result,
                    "care_plan_result": care_plan_result
                }
            else:
                return {
                    "success": True,
                    "message": "Client created but care plan failed",
                    "client_result": client_result,
                    "care_plan_error": care_plan_result.get('error')
                }
                
        except Exception as e:
            logger.error(f"Error in create_client_with_care_plan: {e}")
            return {"error": str(e)}
    
    async def add_care_plan_to_client(self, client_data: Dict[str, Any]) -> Dict[str, Any]:
        """Navigate to client list, find the client, and add a care plan"""
        try:
            # Navigate to clients list
            await self.page.goto(f"{self.base_url}/clients")
            await self.page.wait_for_load_state('networkidle')
            
            # Get the client name to search for
            client_name = client_data.get('personal_info', {}).get('full_name', '')
            if not client_name:
                return {"error": "No client name provided"}
            
            # Extract first and last name for searching
            name_parts = client_name.strip().split()
            if len(name_parts) < 2:
                return {"error": "Client name must have at least first and last name"}
            
            first_name = name_parts[0]
            last_name = name_parts[-1]
            
            # Search for the client in the table
            # Look for the client name in the table
            client_row = None
            try:
                # Try to find the client by name in the table
                client_link = self.page.locator(f'tr:has-text("{first_name}")').first
                if await client_link.is_visible():
                    client_row = client_link
                else:
                    # Try alternative search methods
                    client_link = self.page.locator(f'a:has-text("{first_name} {last_name}")').first
                    if await client_link.is_visible():
                        client_row = client_link
            except:
                pass
            
            if not client_row:
                return {"error": f"Could not find client {first_name} {last_name} in the list"}
            
            # Click on the client to open their profile
            await client_row.click()
            await self.page.wait_for_load_state('networkidle')
            
            # Navigate to Care Plan tab
            care_plan_tab = self.page.locator('a:has-text("Care Plan")')
            if await care_plan_tab.is_visible():
                await care_plan_tab.click()
                await self.page.wait_for_load_state('networkidle')
            else:
                return {"error": "Could not find Care Plan tab"}
            
            # Click "Add Care Plan" button
            add_care_plan_button = self.page.locator('button:has-text("Add Care Plan")')
            if await add_care_plan_button.is_visible():
                await add_care_plan_button.click()
                await self.page.wait_for_load_state('networkidle')
            else:
                return {"error": "Could not find Add Care Plan button"}
            
            # Fill in the care plan modal
            care_plan_info = client_data.get('care_plan', {})
            
            # Care plan name
            care_plan_name = care_plan_info.get('name', 'Care Plan Assessment')
            name_field = self.page.locator('input[placeholder*="Care plan assessment"]')
            if await name_field.is_visible():
                await name_field.fill(care_plan_name)
            
            # Start date (default to today)
            start_date = care_plan_info.get('start_date', '')
            if start_date:
                start_date_field = self.page.locator('input[name*="start_date"]')
                if await start_date_field.is_visible():
                    await start_date_field.fill(start_date)
            
            # End date (default to 30 days from start)
            end_date = care_plan_info.get('end_date', '')
            if end_date:
                end_date_field = self.page.locator('input[name*="end_date"]')
                if await end_date_field.is_visible():
                    await end_date_field.fill(end_date)
            
            # Confirm the care plan creation
            confirm_button = self.page.locator('button:has-text("Confirm")')
            if await confirm_button.is_visible():
                await confirm_button.click()
                await self.page.wait_for_load_state('networkidle')
            else:
                return {"error": "Could not find Confirm button"}
            
            # Now add tasks and goals to the care plan
            tasks_result = await self.add_tasks_to_care_plan(client_data)
            
            return {
                "success": True,
                "message": "Care plan created successfully",
                "tasks_result": tasks_result
            }
            
        except Exception as e:
            logger.error(f"Error adding care plan to client: {e}")
            return {"error": str(e)}
    
    async def add_tasks_to_care_plan(self, client_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add tasks and goals to the care plan"""
        try:
            # Extract tasks and goals from the client data
            tasks = client_data.get('tasks', [])
            goals = client_data.get('goals', [])
            
            # Look for "Add First Goal" or "Add First Task" buttons
            add_goal_button = self.page.locator('button:has-text("Add First Goal")')
            add_task_button = self.page.locator('button:has-text("Add First Task")')
            
            results = {"goals_added": 0, "tasks_added": 0, "errors": []}
            
            # Add goals first
            if goals and await add_goal_button.is_visible():
                for goal in goals:
                    try:
                        await add_goal_button.click()
                        await self.page.wait_for_load_state('networkidle')
                        
                        # Fill in goal details
                        goal_text_field = self.page.locator('textarea, input[type="text"]').first
                        if await goal_text_field.is_visible():
                            await goal_text_field.fill(goal.get('description', goal))
                        
                        # Save the goal
                        save_button = self.page.locator('button:has-text("Save"), button:has-text("Add")').first
                        if await save_button.is_visible():
                            await save_button.click()
                            await self.page.wait_for_load_state('networkidle')
                            results["goals_added"] += 1
                        
                    except Exception as e:
                        results["errors"].append(f"Error adding goal '{goal}': {str(e)}")
            
            # Add tasks
            if tasks and await add_task_button.is_visible():
                for task in tasks:
                    try:
                        await add_task_button.click()
                        await self.page.wait_for_load_state('networkidle')
                        
                        # Fill in task details
                        task_text_field = self.page.locator('textarea, input[type="text"]').first
                        if await task_text_field.is_visible():
                            await task_text_field.fill(task.get('description', task))
                        
                        # Save the task
                        save_button = self.page.locator('button:has-text("Save"), button:has-text("Add")').first
                        if await save_button.is_visible():
                            await save_button.click()
                            await self.page.wait_for_load_state('networkidle')
                            results["tasks_added"] += 1
                        
                    except Exception as e:
                        results["errors"].append(f"Error adding task '{task}': {str(e)}")
            
            return results
            
        except Exception as e:
            logger.error(f"Error adding tasks to care plan: {e}")
            return {"error": str(e)}
    
    async def create_employee(self, employee_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new employee in Shiftcare"""
        try:
            # Ensure we're logged in
            if not await self._ensure_logged_in():
                return {"error": "Failed to login"}
            
            # Navigate to new staff page
            await self.page.goto(f"{self.base_url}/users/staff/new")
            await self.page.wait_for_load_state('networkidle')
            
            # Fill in employee information
            personal_info = employee_data.get('personal_info', {})
            contact_info = employee_data.get('contact_info', {})
            employment_info = employee_data.get('employment_info', {})
            
            # Name fields - handle salutation and name parts
            if personal_info.get('full_name'):
                name_parts = personal_info['full_name'].strip().split()
                
                # Set salutation (default to Mr if not specified)
                salutation = personal_info.get('salutation', 'Mr')
                await self.page.select_option('select[name*="salutation"]', salutation)
                
                # Fill name fields
                if len(name_parts) >= 1:
                    await self.page.fill('input[placeholder*="First Name"]', name_parts[0])
                if len(name_parts) >= 2:
                    await self.page.fill('input[placeholder*="Last/Family Name"]', name_parts[-1])
                if len(name_parts) >= 3:
                    await self.page.fill('input[placeholder*="Middle Name"]', ' '.join(name_parts[1:-1]))
            
            # Display Name (use first name if not specified)
            display_name = personal_info.get('display_name', personal_info.get('full_name', '').split()[0] if personal_info.get('full_name') else '')
            if display_name:
                await self.page.fill('input[placeholder*="Display Name"]', display_name)
            
            # Email
            if contact_info.get('email'):
                await self.page.fill('input[placeholder*="Email"]', contact_info['email'])
            
            # Contact numbers
            if contact_info.get('phone'):
                # Try mobile first, then phone
                mobile_field = self.page.locator('input[placeholder*="Mobile Number"]')
                phone_field = self.page.locator('input[placeholder*="Phone Number"]')
                
                if await mobile_field.is_visible():
                    await mobile_field.fill(contact_info['phone'])
                elif await phone_field.is_visible():
                    await phone_field.fill(contact_info['phone'])
            
            # Select Caregiver role (default)
            caregiver_radio = self.page.locator('input[value="Caregiver"]')
            if await caregiver_radio.is_visible():
                await caregiver_radio.check()
            
            # Gender
            gender = personal_info.get('gender', '')
            if gender:
                await self.page.select_option('select[placeholder*="Gender"]', gender)
            
            # Date of Birth
            if personal_info.get('date_of_birth'):
                dob = personal_info['date_of_birth']
                # Convert date format if needed (MM-DD-YYYY)
                await self.page.fill('input[placeholder*="Date Of Birth"]', dob)
            
            # Employment Type (default to Casual)
            employment_type = employment_info.get('employment_type', 'Casual')
            await self.page.select_option('select[name*="employment_type"]', employment_type)
            
            # Address
            if contact_info.get('address'):
                await self.page.fill('input[placeholder*="Address"]', contact_info['address'])
            
            # Uncheck "Send Onboarding Email" to avoid sending emails during automation
            onboarding_email_checkbox = self.page.locator('input[name*="onboarding_email"]')
            if await onboarding_email_checkbox.is_checked():
                await onboarding_email_checkbox.uncheck()
            
            # Submit the form
            await self.page.click('button:has-text("Create")')
            await self.page.wait_for_load_state('networkidle')
            
            # Check if employee was created successfully
            # Look for success indicators or redirect away from new page
            current_url = self.page.url
            if "/staff/new" not in current_url or "success" in current_url.lower():
                logger.info("Employee created successfully")
                return {"success": True, "message": "Employee created successfully"}
            else:
                # Check for error messages
                error_elements = await self.page.query_selector_all('.error, .alert-danger, [class*="error"]')
                if error_elements:
                    error_text = await error_elements[0].text_content()
                    logger.error(f"Failed to create employee: {error_text}")
                    return {"error": f"Failed to create employee: {error_text}"}
                else:
                    logger.error("Failed to create employee - unknown error")
                    return {"error": "Failed to create employee - unknown error"}
                
        except Exception as e:
            logger.error(f"Error creating employee: {e}")
            return {"error": str(e)}
    
    async def _ensure_logged_in(self) -> bool:
        """Ensure we're logged in, login if not"""
        try:
            # Check if we're already logged in
            if "dashboard" in self.page.url or "clients" in self.page.url or "staff" in self.page.url:
                return True
            
            # Try to login
            return await self.login()
            
        except Exception as e:
            logger.error(f"Error ensuring login: {e}")
            return False
    
    # Synchronous wrapper methods for Flask
    def create_client_sync(self, client_data: Dict[str, Any]) -> Dict[str, Any]:
        """Synchronous wrapper for create_client"""
        return asyncio.run(self._create_client_async(client_data))
    
    def create_client_with_care_plan_sync(self, client_data: Dict[str, Any]) -> Dict[str, Any]:
        """Synchronous wrapper for create_client_with_care_plan"""
        return asyncio.run(self._create_client_with_care_plan_async(client_data))
    
    def create_employee_sync(self, employee_data: Dict[str, Any]) -> Dict[str, Any]:
        """Synchronous wrapper for create_employee"""
        return asyncio.run(self._create_employee_async(employee_data))
    
    async def _create_client_async(self, client_data: Dict[str, Any]) -> Dict[str, Any]:
        """Async method for creating client"""
        async with self:
            return await self.create_client(client_data)
    
    async def _create_client_with_care_plan_async(self, client_data: Dict[str, Any]) -> Dict[str, Any]:
        """Async method for creating client with care plan"""
        async with self:
            return await self.create_client_with_care_plan(client_data)
    
    async def _create_employee_async(self, employee_data: Dict[str, Any]) -> Dict[str, Any]:
        """Async method for creating employee"""
        async with self:
            return await self.create_employee(employee_data)
