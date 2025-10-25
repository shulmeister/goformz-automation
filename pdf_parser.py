import PyPDF2
import re
import logging
from typing import Dict, Any, Optional
from io import BytesIO

logger = logging.getLogger(__name__)

class PDFParser:
    def __init__(self):
        self.client_keywords = ['client', 'customer', 'patient', 'resident']
        self.employee_keywords = ['employee', 'staff', 'worker', 'caregiver']
    
    def parse_pdf(self, pdf_data: bytes) -> Dict[str, Any]:
        """Parse PDF and extract structured data"""
        try:
            pdf_file = BytesIO(pdf_data)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            # Extract text from all pages
            full_text = ""
            for page in pdf_reader.pages:
                full_text += page.extract_text() + "\n"
            
            # Parse the text to extract structured data
            parsed_data = self._extract_data_from_text(full_text)
            
            return parsed_data
            
        except Exception as e:
            logger.error(f"Error parsing PDF: {e}")
            raise
    
    def _extract_data_from_text(self, text: str) -> Dict[str, Any]:
        """Extract structured data from PDF text"""
        data = {
            'raw_text': text,
            'personal_info': {},
            'contact_info': {},
            'emergency_contact': {},
            'medical_info': {},
            'employment_info': {},
            'other_info': {}
        }
        
        # Extract personal information
        data['personal_info'] = self._extract_personal_info(text)
        
        # Extract contact information
        data['contact_info'] = self._extract_contact_info(text)
        
        # Extract emergency contact
        data['emergency_contact'] = self._extract_emergency_contact(text)
        
        # Extract medical information
        data['medical_info'] = self._extract_medical_info(text)
        
        # Extract employment information
        data['employment_info'] = self._extract_employment_info(text)
        
        # Extract care plan information (tasks, goals, etc.)
        data['care_plan'] = self._extract_care_plan_info(text)
        data['tasks'] = self._extract_tasks(text)
        data['goals'] = self._extract_goals(text)
        
        return data
    
    def _extract_personal_info(self, text: str) -> Dict[str, str]:
        """Extract personal information like name, DOB, SSN"""
        info = {}
        
        # Name patterns
        name_patterns = [
            r'Name[:\s]+([A-Za-z\s,.-]+)',
            r'Full Name[:\s]+([A-Za-z\s,.-]+)',
            r'Client Name[:\s]+([A-Za-z\s,.-]+)',
            r'Employee Name[:\s]+([A-Za-z\s,.-]+)',
            r'Patient Name[:\s]+([A-Za-z\s,.-]+)'
        ]
        
        for pattern in name_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                info['full_name'] = match.group(1).strip()
                break
        
        # Preferred Name
        preferred_name_patterns = [
            r'Preferred Name[:\s]+([A-Za-z\s,.-]+)',
            r'Nickname[:\s]+([A-Za-z\s,.-]+)',
            r'Goes By[:\s]+([A-Za-z\s,.-]+)'
        ]
        
        for pattern in preferred_name_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                info['preferred_name'] = match.group(1).strip()
                break
        
        # Date of Birth
        dob_patterns = [
            r'Date of Birth[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
            r'DOB[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
            r'Birth Date[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
            r'Born[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})'
        ]
        
        for pattern in dob_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                info['date_of_birth'] = match.group(1).strip()
                break
        
        # Social Security Number
        ssn_pattern = r'SSN[:\s]+(\d{3}-?\d{2}-?\d{4})'
        match = re.search(ssn_pattern, text, re.IGNORECASE)
        if match:
            info['ssn'] = match.group(1).strip()
        
        # Gender
        gender_patterns = [
            r'Gender[:\s]+(Male|Female|Other)',
            r'Sex[:\s]+(Male|Female|Other)',
            r'Gender[:\s]+(M|F)',
            r'Sex[:\s]+(M|F)'
        ]
        
        for pattern in gender_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                gender = match.group(1).strip()
                # Convert M/F to full words
                if gender.upper() == 'M':
                    info['gender'] = 'Male'
                elif gender.upper() == 'F':
                    info['gender'] = 'Female'
                else:
                    info['gender'] = gender
                break
        
        # Salutation (Mr, Mrs, Ms, Dr, etc.)
        salutation_patterns = [
            r'(Mr|Mrs|Ms|Dr|Prof)\.?\s+([A-Za-z\s]+)',
            r'Title[:\s]+(Mr|Mrs|Ms|Dr|Prof)',
            r'Salutation[:\s]+(Mr|Mrs|Ms|Dr|Prof)'
        ]
        
        for pattern in salutation_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                info['salutation'] = match.group(1).strip()
                break
        
        # Place of Birth
        place_of_birth_patterns = [
            r'Place of Birth[:\s]+([^\n]+)',
            r'Born in[:\s]+([^\n]+)',
            r'Birth Place[:\s]+([^\n]+)'
        ]
        
        for pattern in place_of_birth_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                info['place_of_birth'] = match.group(1).strip()
                break
        
        # Languages
        languages_patterns = [
            r'Languages[:\s]+([^\n]+)',
            r'Language[:\s]+([^\n]+)',
            r'Speaks[:\s]+([^\n]+)'
        ]
        
        for pattern in languages_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                info['languages'] = match.group(1).strip()
                break
        
        # Religion
        religion_patterns = [
            r'Religion[:\s]+([^\n]+)',
            r'Faith[:\s]+([^\n]+)',
            r'Religious Affiliation[:\s]+([^\n]+)'
        ]
        
        for pattern in religion_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                info['religion'] = match.group(1).strip()
                break
        
        # Marital Status
        marital_patterns = [
            r'Marital Status[:\s]+(Single|Married|Divorced|Widowed|Separated)',
            r'Status[:\s]+(Single|Married|Divorced|Widowed|Separated)'
        ]
        
        for pattern in marital_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                info['marital_status'] = match.group(1).strip()
                break
        
        # Nationality
        nationality_patterns = [
            r'Nationality[:\s]+([^\n]+)',
            r'Citizenship[:\s]+([^\n]+)',
            r'Country of Origin[:\s]+([^\n]+)'
        ]
        
        for pattern in nationality_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                info['nationality'] = match.group(1).strip()
                break
        
        # Ethnicity
        ethnicity_patterns = [
            r'Ethnicity[:\s]+([^\n]+)',
            r'Ethnic Background[:\s]+([^\n]+)',
            r'Race[:\s]+([^\n]+)'
        ]
        
        for pattern in ethnicity_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                info['ethnicity'] = match.group(1).strip()
                break
        
        return info
    
    def _extract_contact_info(self, text: str) -> Dict[str, str]:
        """Extract contact information"""
        info = {}
        
        # Phone numbers
        phone_patterns = [
            r'Phone[:\s]+(\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})',
            r'Mobile[:\s]+(\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})',
            r'Cell[:\s]+(\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})',
            r'Primary Phone[:\s]+(\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})'
        ]
        
        for pattern in phone_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                info['phone'] = match.group(1).strip()
                break
        
        # Secondary Phone
        secondary_phone_patterns = [
            r'Secondary Phone[:\s]+(\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})',
            r'Home Phone[:\s]+(\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})',
            r'Work Phone[:\s]+(\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})'
        ]
        
        for pattern in secondary_phone_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                info['secondary_phone'] = match.group(1).strip()
                break
        
        # Email
        email_patterns = [
            r'Email[:\s]+([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
            r'Primary Email[:\s]+([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
            r'E-mail[:\s]+([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
        ]
        
        for pattern in email_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                info['email'] = match.group(1).strip()
                break
        
        # Secondary Email
        secondary_email_pattern = r'Secondary Email[:\s]+([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
        match = re.search(secondary_email_pattern, text, re.IGNORECASE)
        if match:
            info['secondary_email'] = match.group(1).strip()
        
        # Address
        address_patterns = [
            r'Address[:\s]+([^\n]+)',
            r'Street Address[:\s]+([^\n]+)',
            r'Home Address[:\s]+([^\n]+)',
            r'Primary Address[:\s]+([^\n]+)'
        ]
        
        for pattern in address_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                info['address'] = match.group(1).strip()
                break
        
        # Unit/Apartment Number
        unit_patterns = [
            r'Unit[:\s]+([^\n]+)',
            r'Apartment[:\s]+([^\n]+)',
            r'Apt[:\s]+([^\n]+)',
            r'Suite[:\s]+([^\n]+)'
        ]
        
        for pattern in unit_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                info['unit_apartment'] = match.group(1).strip()
                break
        
        # Postal Code
        postal_patterns = [
            r'Postal Code[:\s]+([^\n]+)',
            r'Zip Code[:\s]+([^\n]+)',
            r'ZIP[:\s]+([^\n]+)',
            r'Postcode[:\s]+([^\n]+)'
        ]
        
        for pattern in postal_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                info['postal_code'] = match.group(1).strip()
                break
        
        # Preferred Contact Method
        contact_method_patterns = [
            r'Preferred Contact[:\s]+(Phone|Email|Text|SMS|Mail)',
            r'Contact Method[:\s]+(Phone|Email|Text|SMS|Mail)',
            r'Best Way to Contact[:\s]+(Phone|Email|Text|SMS|Mail)'
        ]
        
        for pattern in contact_method_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                info['preferred_contact_method'] = match.group(1).strip()
                break
        
        return info
    
    def _extract_emergency_contact(self, text: str) -> Dict[str, str]:
        """Extract emergency contact information"""
        info = {}
        
        # Emergency contact name
        ec_name_pattern = r'Emergency Contact[:\s]+([A-Za-z\s,.-]+)'
        match = re.search(ec_name_pattern, text, re.IGNORECASE)
        if match:
            info['name'] = match.group(1).strip()
        
        # Emergency contact phone
        ec_phone_pattern = r'Emergency Phone[:\s]+(\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})'
        match = re.search(ec_phone_pattern, text, re.IGNORECASE)
        if match:
            info['phone'] = match.group(1).strip()
        
        return info
    
    def _extract_medical_info(self, text: str) -> Dict[str, str]:
        """Extract medical information"""
        info = {}
        
        # Medical conditions
        conditions_pattern = r'Medical Conditions[:\s]+([^\n]+)'
        match = re.search(conditions_pattern, text, re.IGNORECASE)
        if match:
            info['conditions'] = match.group(1).strip()
        
        # Medications
        medications_pattern = r'Medications[:\s]+([^\n]+)'
        match = re.search(medications_pattern, text, re.IGNORECASE)
        if match:
            info['medications'] = match.group(1).strip()
        
        return info
    
    def _extract_employment_info(self, text: str) -> Dict[str, str]:
        """Extract employment information"""
        info = {}
        
        # Position/Title
        position_patterns = [
            r'Position[:\s]+([^\n]+)',
            r'Title[:\s]+([^\n]+)',
            r'Job Title[:\s]+([^\n]+)',
            r'Role[:\s]+([^\n]+)'
        ]
        
        for pattern in position_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                info['position'] = match.group(1).strip()
                break
        
        # Department
        dept_pattern = r'Department[:\s]+([^\n]+)'
        match = re.search(dept_pattern, text, re.IGNORECASE)
        if match:
            info['department'] = match.group(1).strip()
        
        # Employment Type
        employment_type_patterns = [
            r'Employment Type[:\s]+(Full-time|Part-time|Casual|Contract|Temporary)',
            r'Type[:\s]+(Full-time|Part-time|Casual|Contract|Temporary)',
            r'Status[:\s]+(Full-time|Part-time|Casual|Contract|Temporary)'
        ]
        
        for pattern in employment_type_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                info['employment_type'] = match.group(1).strip()
                break
        
        # If no employment type found, try to infer from context
        if not info.get('employment_type'):
            text_lower = text.lower()
            if 'casual' in text_lower:
                info['employment_type'] = 'Casual'
            elif 'part-time' in text_lower or 'part time' in text_lower:
                info['employment_type'] = 'Part-time'
            elif 'full-time' in text_lower or 'full time' in text_lower:
                info['employment_type'] = 'Full-time'
            else:
                info['employment_type'] = 'Casual'  # Default
        
        return info
    
    def _extract_care_plan_info(self, text: str) -> Dict[str, str]:
        """Extract care plan information"""
        info = {}
        
        # Care plan name/title
        care_plan_patterns = [
            r'Care Plan[:\s]+([^\n]+)',
            r'Plan Name[:\s]+([^\n]+)',
            r'Assessment[:\s]+([^\n]+)',
            r'Treatment Plan[:\s]+([^\n]+)'
        ]
        
        for pattern in care_plan_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                info['name'] = match.group(1).strip()
                break
        
        # Start date
        start_date_patterns = [
            r'Start Date[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
            r'Plan Start[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
            r'Effective Date[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})'
        ]
        
        for pattern in start_date_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                info['start_date'] = match.group(1).strip()
                break
        
        # End date
        end_date_patterns = [
            r'End Date[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
            r'Plan End[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
            r'Review Date[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})'
        ]
        
        for pattern in end_date_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                info['end_date'] = match.group(1).strip()
                break
        
        return info
    
    def _extract_tasks(self, text: str) -> list:
        """Extract tasks from the PDF"""
        tasks = []
        
        # Look for task patterns
        task_patterns = [
            r'Task[:\s]+([^\n]+)',
            r'Activity[:\s]+([^\n]+)',
            r'Action[:\s]+([^\n]+)',
            r'To Do[:\s]+([^\n]+)',
            r'Care Task[:\s]+([^\n]+)',
            r'Service[:\s]+([^\n]+)'
        ]
        
        for pattern in task_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                task_text = match.strip()
                if task_text and len(task_text) > 3:  # Filter out very short matches
                    tasks.append({
                        'description': task_text,
                        'type': 'task'
                    })
        
        # Look for numbered lists that might be tasks
        numbered_task_pattern = r'^\d+[\.\)]\s*([^\n]+)'
        matches = re.findall(numbered_task_pattern, text, re.MULTILINE)
        for match in matches:
            task_text = match.strip()
            if task_text and len(task_text) > 3:
                tasks.append({
                    'description': task_text,
                    'type': 'task'
                })
        
        # Look for bullet points that might be tasks
        bullet_pattern = r'^[-•*]\s*([^\n]+)'
        matches = re.findall(bullet_pattern, text, re.MULTILINE)
        for match in matches:
            task_text = match.strip()
            if task_text and len(task_text) > 3:
                tasks.append({
                    'description': task_text,
                    'type': 'task'
                })
        
        return tasks
    
    def _extract_goals(self, text: str) -> list:
        """Extract goals from the PDF"""
        goals = []
        
        # Look for goal patterns
        goal_patterns = [
            r'Goal[:\s]+([^\n]+)',
            r'Objective[:\s]+([^\n]+)',
            r'Target[:\s]+([^\n]+)',
            r'Aim[:\s]+([^\n]+)',
            r'Outcome[:\s]+([^\n]+)',
            r'Care Goal[:\s]+([^\n]+)'
        ]
        
        for pattern in goal_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                goal_text = match.strip()
                if goal_text and len(goal_text) > 3:  # Filter out very short matches
                    goals.append({
                        'description': goal_text,
                        'type': 'goal'
                    })
        
        # Look for sections that might contain goals
        goal_section_patterns = [
            r'Goals?[:\s]*\n([^\n]+(?:\n[^\n]+)*)',
            r'Objectives?[:\s]*\n([^\n]+(?:\n[^\n]+)*)',
            r'Targets?[:\s]*\n([^\n]+(?:\n[^\n]+)*)'
        ]
        
        for pattern in goal_section_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                # Split the match into individual goals
                lines = match.strip().split('\n')
                for line in lines:
                    line = line.strip()
                    if line and len(line) > 3:
                        goals.append({
                            'description': line,
                            'type': 'goal'
                        })
        
        return goals
    
    def determine_packet_type(self, parsed_data: Dict[str, Any]) -> str:
        """Determine if this is a client or employee packet"""
        text = parsed_data.get('raw_text', '').lower()
        
        # Count keyword occurrences
        client_score = sum(1 for keyword in self.client_keywords if keyword in text)
        employee_score = sum(1 for keyword in self.employee_keywords if keyword in text)
        
        # Check for specific indicators
        if 'employee packet' in text or 'staff packet' in text:
            return 'employee'
        elif 'client packet' in text or 'patient packet' in text:
            return 'client'
        
        # Use keyword scoring
        if employee_score > client_score:
            return 'employee'
        elif client_score > employee_score:
            return 'client'
        else:
            # Default to client if unclear
            return 'client'
