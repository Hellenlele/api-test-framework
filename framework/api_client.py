import requests
import json
import logging
from typing import Dict, Any, Optional


class APIClient:
    def __init__(self, base_url: str, timeout: int = 30):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self.logger = logging.getLogger(__name__)
        
    def set_auth(self, auth_type: str, **kwargs):
        if auth_type == 'bearer':
            token = kwargs.get('token')
            self.session.headers.update({'Authorization': f'Bearer {token}'})
        elif auth_type == 'basic':
            username = kwargs.get('username')
            password = kwargs.get('password')
            self.session.auth = (username, password)
        elif auth_type == 'api_key':
            key_name = kwargs.get('key_name', 'X-API-Key')
            api_key = kwargs.get('api_key')
            self.session.headers.update({key_name: api_key})

    
    def set_headers(self, headers: Dict[str, str]):
        self.session.headers.update(headers)
    
    def get(self, endpoint: str, params: Optional[Dict] = None, headers: Optional[Dict] = None) -> requests.Response:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        self.logger.info(f"GET {url}")
        if params:
            self.logger.debug(f"Query params: {params}")
        
        response = self.session.get(
            url, 
            params=params, 
            headers=headers, 
            timeout=self.timeout
        )
        self._log_response(response)
        return response
    
    def post(self, endpoint: str, data: Optional[Dict] = None, json_data: Optional[Dict] = None, 
             headers: Optional[Dict] = None) -> requests.Response:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        self.logger.info(f"POST {url}")
        if json_data:
            self.logger.debug(f"JSON payload: {json.dumps(json_data, indent=2)}")
        elif data:
            self.logger.debug(f"Form data: {data}")
        
        response = self.session.post(
            url, 
            data=data, 
            json=json_data, 
            headers=headers, 
            timeout=self.timeout
        )
        self._log_response(response)
        return response
    
    def put(self, endpoint: str, data: Optional[Dict] = None, json_data: Optional[Dict] = None, 
            headers: Optional[Dict] = None) -> requests.Response:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        self.logger.info(f"PUT {url}")
        if json_data:
            self.logger.debug(f"JSON payload: {json.dumps(json_data, indent=2)}")
        elif data:
            self.logger.debug(f"Form data: {data}")
        
        response = self.session.put(
            url, 
            data=data, 
            json=json_data, 
            headers=headers, 
            timeout=self.timeout
        )
        self._log_response(response)
        return response
    
    def delete(self, endpoint: str, headers: Optional[Dict] = None) -> requests.Response:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        self.logger.info(f"DELETE {url}")
        
        response = self.session.delete(
            url, 
            headers=headers, 
            timeout=self.timeout
        )
        self._log_response(response)
        return response
    
    def patch(self, endpoint: str, data: Optional[Dict] = None, json_data: Optional[Dict] = None, 
              headers: Optional[Dict] = None) -> requests.Response:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        self.logger.info(f"PATCH {url}")
        if json_data:
            self.logger.debug(f"JSON payload: {json.dumps(json_data, indent=2)}")
        elif data:
            self.logger.debug(f"Form data: {data}")
        
        response = self.session.patch(
            url, 
            data=data, 
            json=json_data, 
            headers=headers, 
            timeout=self.timeout
        )
        self._log_response(response)
        return response
    
    def _log_response(self, response: requests.Response):
        self.logger.info(f"Response: {response.status_code} {response.reason}")
        self.logger.debug(f"Response headers: {dict(response.headers)}")
        try:
            self.logger.debug(f"Response body: {response.json()}")
        except:
            self.logger.debug(f"Response body: {response.text[:500]}")