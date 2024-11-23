import os
import requests
import base64

class SpringConfigClient:
    def __init__(self):
        self.config_server_url = os.getenv('CONFIG_SERVER_URL', 'localhost:8888')
        self.application_name = os.getenv('APPLICATION_NAME', 'application')
        self.profile = os.getenv('PROFILE', 'dev')
        
        # Basic 인증 정보
        self.username = os.getenv('CONFIG_SERVER_USERNAME')
        self.password = os.getenv('CONFIG_SERVER_PASSWORD')
        
        self.config = self._fetch_config()

    def _fetch_config(self):
        """Spring Cloud Config Server에서 설정을 가져옵니다"""
        url = f"http://{self.username}:{self.password}@{self.config_server_url}/{self.application_name}/{self.profile}"
            
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"설정 서버에서 설정을 가져오는데 실패했습니다: {e}")
            return {}

    def get_property(self, key, default=None):
        """설정값을 가져옵니다"""
        try:
            for source in self.config.get('propertySources', []):
                properties = source.get('source', {})
                if key in properties:
                    return properties[key]
            return default
        except Exception as e:
            print(f"설정값을 가져오는데 실패했습니다: {e}")
            return default 