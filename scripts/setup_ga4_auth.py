#!/usr/bin/env python3
"""GA4 OAuth 授權設定腳本"""

import json
import yaml
import os
from google_auth_oauthlib.flow import InstalledAppFlow

CONFIG_DIR = os.path.join(os.path.dirname(__file__), '..', 'config')
ADS_YAML = os.path.join(CONFIG_DIR, 'google_ads.yaml')
GA4_CONFIG = os.path.join(CONFIG_DIR, 'ga4.json')

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']

def main():
    with open(ADS_YAML) as f:
        ads_config = yaml.safe_load(f)

    client_config = {
        "installed": {
            "client_id": ads_config['client_id'],
            "client_secret": ads_config['client_secret'],
            "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token"
        }
    }

    flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
    creds = flow.run_local_server(port=0)

    config = {
        "client_id": ads_config['client_id'],
        "client_secret": ads_config['client_secret'],
        "refresh_token": creds.refresh_token
    }

    with open(GA4_CONFIG, 'w') as f:
        json.dump(config, f, indent=2)

    print(f"\n✅ GA4 授權完成，設定已存入：{GA4_CONFIG}")

if __name__ == '__main__':
    main()
