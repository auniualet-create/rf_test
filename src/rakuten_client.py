"""
楽天APIクライアント
商品情報を更新する
"""
import os
import requests
from typing import Dict, Optional
from dotenv import load_dotenv

load_dotenv()


class RakutenClient:
    """楽天APIクライアント"""
    
    def __init__(self):
        self.application_id = os.getenv("RAKUTEN_APPLICATION_ID")
        self.affiliate_id = os.getenv("RAKUTEN_AFFILIATE_ID")
        self.secret = os.getenv("RAKUTEN_SECRET")
        self.access_token = os.getenv("RAKUTEN_ACCESS_TOKEN")
        
        if not self.application_id:
            raise ValueError("楽天APIの設定が不完全です")
        
        self.base_url = "https://api.rms.rakuten.co.jp/es/1.0"
    
    def update_product_description(self, item_code: str, description_html: str) -> Dict:
        """
        商品の説明文を更新
        
        Args:
            item_code: 商品コード
            description_html: HTML形式の説明文
            
        Returns:
            更新結果
        """
        # 注意: 楽天APIの実際のエンドポイントとパラメータは
        # 公式ドキュメントを確認してください
        # ここでは一般的な構造を示しています
        
        url = f"{self.base_url}/item/update"
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "itemCode": item_code,
            "itemDetail": description_html
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"楽天APIの呼び出しに失敗しました: {e}")
    
    def get_product_info(self, item_code: str) -> Dict:
        """
        商品情報を取得
        
        Args:
            item_code: 商品コード
            
        Returns:
            商品情報
        """
        url = f"{self.base_url}/item/get"
        
        params = {
            "itemCode": item_code
        }
        
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        
        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"楽天APIの呼び出しに失敗しました: {e}")
