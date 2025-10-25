import requests
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class GoFormzClient:
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = "https://api.goformz.com/v1"
        self.access_token = None
        
    def _get_access_token(self) -> str:
        """Get OAuth2 access token"""
        if self.access_token:
            return self.access_token
            
        token_url = f"{self.base_url}/oauth/token"
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        
        try:
            response = requests.post(token_url, data=data)
            response.raise_for_status()
            token_data = response.json()
            self.access_token = token_data['access_token']
            return self.access_token
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get access token: {e}")
            raise
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Make authenticated request to GoFormz API"""
        token = self._get_access_token()
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        url = f"{self.base_url}{endpoint}"
        response = requests.request(method, url, headers=headers, **kwargs)
        response.raise_for_status()
        return response
    
    def get_recent_forms(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent forms from GoFormz"""
        try:
            response = self._make_request('GET', f'/forms?limit={limit}')
            return response.json().get('data', [])
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get forms: {e}")
            raise
    
    def get_form_details(self, form_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific form"""
        try:
            response = self._make_request('GET', f'/forms/{form_id}')
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get form details for {form_id}: {e}")
            raise
    
    def download_form_pdf(self, form_id: str) -> bytes:
        """Download PDF for a specific form"""
        try:
            response = self._make_request('GET', f'/forms/{form_id}/pdf')
            return response.content
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to download PDF for form {form_id}: {e}")
            raise
    
    def search_forms(self, query: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Search forms by query"""
        try:
            params = {'q': query, 'limit': limit}
            response = self._make_request('GET', '/forms/search', params=params)
            return response.json().get('data', [])
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to search forms: {e}")
            raise
