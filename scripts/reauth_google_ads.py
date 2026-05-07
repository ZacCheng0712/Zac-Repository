#!/usr/bin/env python3
"""
Google Ads API 重新授權腳本
執行後會印出一個授權 URL，在瀏覽器開啟並登入，
複製授權碼貼回終端機，腳本自動更新 google_ads.yaml。
"""
import warnings
warnings.filterwarnings('ignore')

import os
import yaml
from google_auth_oauthlib.flow import InstalledAppFlow

CONFIG_PATH = os.path.join(os.path.dirname(__file__), '..', 'config', 'google_ads.yaml')

import json

def _load_client_config():
    ga4_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'ga4.json')
    with open(ga4_path) as f:
        c = json.load(f)
    return {"installed": {
        "client_id": c["client_id"],
        "client_secret": c["client_secret"],
        "redirect_uris": ["http://localhost"],
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
    }}

CLIENT_CONFIG = _load_client_config()

SCOPES = ["https://www.googleapis.com/auth/adwords"]

def main():
    print("=" * 60)
    print("Google Ads API 重新授權")
    print("=" * 60)

    flow = InstalledAppFlow.from_client_config(CLIENT_CONFIG, scopes=SCOPES)

    # 使用 localhost redirect，會自動開啟瀏覽器
    try:
        creds = flow.run_local_server(port=8080, prompt='consent', access_type='offline')
    except Exception:
        # fallback: 手動複製貼上
        flow.redirect_uri = "urn:ietf:wg:oauth:2.0:oob"
        auth_url, _ = flow.authorization_url(prompt='consent', access_type='offline')
        print(f"\n請在瀏覽器開啟以下網址並登入：\n\n{auth_url}\n")
        code = input("登入後複製授權碼並貼在這裡：").strip()
        flow.fetch_token(code=code)
        creds = flow.credentials

    new_refresh_token = creds.refresh_token
    print(f"\n✅ 取得新 refresh_token：{new_refresh_token[:20]}...")

    # 更新 google_ads.yaml
    with open(CONFIG_PATH, 'r') as f:
        config = yaml.safe_load(f)

    config['refresh_token'] = new_refresh_token

    with open(CONFIG_PATH, 'w') as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True)

    print(f"✅ 已更新 {CONFIG_PATH}")
    print("現在可以重新執行週報腳本了！")

if __name__ == '__main__':
    main()
