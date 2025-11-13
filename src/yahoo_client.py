"""
YahooショッピングAPIクライアント
商品情報を更新する
"""
import os
import requests
from typing import Dict, Optional
from dotenv import load_dotenv

load_dotenv()


class YahooShoppingClient:
    """YahooショッピングAPIクライアント"""
    
    def __init__(self):
        self.seller_id = os.getenv("YAHOO_SELLER_ID")
        self.application_id = os.getenv("YAHOO_APPLICATION_ID")
        self.client_id = os.getenv("YAHOO_CLIENT_ID")
        self.client_secret = os.getenv("YAHOO_CLIENT_SECRET")
        self.access_token = os.getenv("YAHOO_ACCESS_TOKEN")
        
        if not all([self.seller_id, self.application_id]):
            raise ValueError("Yahooショッピングの設定が不完全です")
        
        self.base_url = "https://circus.shopping.yahooapis.jp/ShoppingWebService/V1"
    
    def update_product_description(self, item_code: str, description_html: str) -> Dict:
        """
        商品の説明文を更新
        
        Args:
            item_code: 商品コード
            description_html: HTML形式の説明文
            
        Returns:
            更新結果
        """
        # 注意: YahooショッピングAPIの実際のエンドポイントとパラメータは
        # 公式ドキュメントを確認してください
        # ここでは一般的な構造を示しています
        
        url = f"{self.base_url}/itemUpdate"
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "seller_id": self.seller_id,
            "item_code": item_code,
            "description": description_html
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"YahooショッピングAPIの呼び出しに失敗しました: {e}")
    
    def get_product_info(self, item_code: str) -> Dict:
        """
        商品情報を取得
        
        Args:
            item_code: 商品コード
            
        Returns:
            商品情報
        """
        url = f"{self.base_url}/itemGet"
        
        params = {
            "seller_id": self.seller_id,
            "item_code": item_code
        }
        
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        
        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"YahooショッピングAPIの呼び出しに失敗しました: {e}")


class YahooShoppingBrowserClient:
    """
    Yahooショッピング管理画面をブラウザ自動化で操作するクライアント
    APIが利用できない場合の代替手段
    """
    
    def __init__(self):
        from playwright.sync_api import sync_playwright
        self.playwright = sync_playwright
        self.yahoo_login_url = "https://login.yahoo.co.jp"
        self.yahoo_manage_url = "https://shopping.yahoo.co.jp/seller"
    
    def update_product_via_browser(
        self,
        username: str,
        password: str,
        item_code: str,
        description_html: str
    ) -> bool:
        """
        ブラウザ自動化で商品情報を更新
        
        Args:
            username: Yahooアカウントのユーザー名
            password: Yahooアカウントのパスワード
            item_code: 商品コード
            description_html: HTML形式の説明文
            
        Returns:
            成功したかどうか
        """
        with self.playwright() as p:
            browser = p.chromium.launch(headless=False)  # デバッグ時はheadless=False
            context = browser.new_context()
            page = context.new_page()
            
            try:
                # ログイン
                page.goto(self.yahoo_login_url)
                page.fill('input[name="login"]', username)
                page.fill('input[name="password"]', password)
                page.click('button[type="submit"]')
                page.wait_for_url("**/seller/**")
                
                # 商品編集ページに移動
                edit_url = f"{self.yahoo_manage_url}/items/{item_code}/edit"
                page.goto(edit_url)
                
                # HTML入力欄を見つけて入力
                # 注意: 実際のセレクタはYahooの管理画面の構造に合わせて調整が必要
                html_textarea = page.locator('textarea[name="description"]')  # 実際のセレクタに合わせて変更
                html_textarea.fill(description_html)
                
                # 保存ボタンをクリック
                page.click('button[type="submit"]')
                page.wait_for_load_state("networkidle")
                
                browser.close()
                return True
                
            except Exception as e:
                print(f"ブラウザ自動化でエラーが発生しました: {e}")
                browser.close()
                return False
