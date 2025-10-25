import requests
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class GoFormzClient:
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = "https://api.goformz.com/v2"
        self.access_token = None
        
    def _get_access_token(self) -> str:
        """Get API access token - using client_id as API key for v2"""
        # For GoFormz v2 API, the client_id is used as the API key
        return self.client_id
    
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
            response = self._make_request('GET', f'/formz?limit={limit}')
            return response.json().get('data', [])
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get forms: {e}")
            raise
    
    def get_form_details(self, form_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific form"""
        try:
            response = self._make_request('GET', f'/formz/{form_id}')
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get form details for {form_id}: {e}")
            raise
    
    def download_form_pdf(self, form_id: str) -> bytes:
        """Download PDF for a specific form"""
        try:
            response = self._make_request('GET', f'/formz/{form_id}/pdf')
            return response.content
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to download PDF for form {form_id}: {e}")
            raise
    
    def search_forms(self, query: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Search forms by query"""
        try:
            params = {'q': query, 'limit': limit}
            response = self._make_request('GET', '/formz/search', params=params)
            return response.json().get('data', [])
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to search forms: {e}")
            raise
