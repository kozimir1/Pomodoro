from dataclasses import dataclass

import requests

from settings import Settings


@dataclass
class GoogleClient:
    settings: Settings

    def get_user_info(self, code: str) -> dict:
        access_token = self.settings.get_access_token(code)
        user_info = requests.get('https://www.googleapis.com/oauth2/v4/userinfo?access_token={}',
                                 headers={'Authorization': f'Bearer {access_token}'})
        return user_info.json()

    def _get_user_access_token(self, code: str) -> str:
        data = {
            'code': code,
            'client_id': self.settings.GOOGLE_CLIENT_ID,
            'client_secret': self.settings.GOOGLE_SECRET_KEY,
            'redirect_uri': self.settings.GOOGLE_REDIRECT_URI,
            'grant_type': 'authorization_code',
        }
        response = requests.get(self.settings.GOOGLE_REDIRECT_URI, data=data)
        return response.json()['access_token']