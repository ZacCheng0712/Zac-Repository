#!/usr/bin/env python3
"""
手動登入 Google Ads 並儲存 session，供後續自動化使用。
執行後會開啟瀏覽器視窗，請登入後關閉瀏覽器，session 會自動儲存。
"""

import os
import json
from playwright.sync_api import sync_playwright

SESSION_PATH = os.path.join(os.path.dirname(__file__), '..', 'config', 'google_ads_session.json')

def main():
    with sync_playwright() as p:
        import time, shutil, tempfile

        # 複製 Chrome profile 到暫存目錄（避免衝突）
        chrome_profile = os.path.expanduser("~/Library/Application Support/Google/Chrome")
        tmp_profile = tempfile.mkdtemp(prefix="chrome_tmp_")
        print(f"複製 Chrome profile 中...")
        ignore = shutil.ignore_patterns("SingletonSocket", "SingletonLock", "SingletonCookie", "RunningChromeVersion", "*.tmp")
        shutil.copytree(chrome_profile, os.path.join(tmp_profile, "Chrome"), dirs_exist_ok=True, ignore=ignore)

        context = p.chromium.launch_persistent_context(
            os.path.join(tmp_profile, "Chrome"),
            channel="chrome",
            headless=False,
            args=["--profile-directory=Default"],
            viewport={"width": 1440, "height": 900},
        )

        page = context.new_page()
        print("\n✅ 開啟你的 Chrome（已登入狀態），等待 30 秒讓頁面載入...\n")
        page.goto("https://ads.google.com/aw/overview?ocid=3382089284")
        time.sleep(30)

        storage = context.storage_state()
        with open(SESSION_PATH, 'w') as f:
            json.dump(storage, f)

        context.close()
        shutil.rmtree(tmp_profile, ignore_errors=True)
        print(f"\n✅ Session 已儲存：{SESSION_PATH}")

if __name__ == '__main__':
    main()
