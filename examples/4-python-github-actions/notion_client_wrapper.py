"""Notion API クライアントラッパー"""

import logging
from typing import List, Dict, Any, Optional

from notion_client import Client

logger = logging.getLogger(__name__)


class NotionClient:
    """Notion API クライアント"""
    
    def __init__(self, api_key: str, database_id: str):
        """
        初期化
        
        Args:
            api_key: Notion Integration Token
            database_id: データベースID
        """
        self.client = Client(auth=api_key)
        self.database_id = database_id
    
    def fetch_all_products(self) -> List[Dict[str, Any]]:
        """
        データベースから全商品を取得
        
        Returns:
            商品データのリスト
        """
        products = []
        has_more = True
        start_cursor = None
        
        while has_more:
            response = self.client.databases.query(
                database_id=self.database_id,
                start_cursor=start_cursor,
                page_size=100
            )
            
            for page in response['results']:
                product = self._extract_product_data(page)
                if product:
                    products.append(product)
            
            has_more = response['has_more']
            start_cursor = response.get('next_cursor')
        
        logger.info(f"Notionから{len(products)}件の商品を取得しました")
        return products
    
    def _extract_product_data(self, page: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Notionページから商品データを抽出
        
        Args:
            page: Notion APIレスポンスのページオブジェクト
            
        Returns:
            商品データ辞書
        """
        try:
            props = page['properties']
            
            # プロパティ名は実際のNotionデータベースに合わせて調整してください
            product = {
                'id': self._get_text(props.get('商品ID') or props.get('ID')),
                'name': self._get_text(props.get('名称') or props.get('商品名')),
                'ingredients': self._get_text(props.get('原材料名')),
                'allergen': self._get_text(props.get('アレルゲン')),
                'nutrition': self._get_text(props.get('栄養成分表示')),
                'content': self._get_text(props.get('内容量')),
                'expiry': self._get_text(props.get('賞味期限')),
                'storage': self._get_text(props.get('保存方法')),
                'manufacturer': self._get_text(props.get('製造者/出荷元') or props.get('製造者')),
                
                # ECモール連携用ID
                'yahoo_product_id': self._get_text(props.get('Yahoo商品ID')),
                'rakuten_product_id': self._get_text(props.get('楽天商品ID')),
                
                # メタ情報
                'notion_page_id': page['id'],
                'last_edited': page['last_edited_time']
            }
            
            return product
            
        except Exception as e:
            logger.warning(f"商品データの抽出に失敗: {str(e)}")
            return None
    
    def _get_text(self, prop: Optional[Dict[str, Any]]) -> str:
        """
        Notionプロパティからテキストを取得
        
        Args:
            prop: Notionプロパティオブジェクト
            
        Returns:
            テキスト文字列
        """
        if not prop:
            return ''
        
        prop_type = prop.get('type')
        
        if prop_type == 'title':
            return ''.join([t['plain_text'] for t in prop.get('title', [])])
        
        elif prop_type == 'rich_text':
            return ''.join([t['plain_text'] for t in prop.get('rich_text', [])])
        
        elif prop_type == 'number':
            num = prop.get('number')
            return str(num) if num is not None else ''
        
        elif prop_type == 'select':
            select = prop.get('select')
            return select['name'] if select else ''
        
        elif prop_type == 'multi_select':
            return ', '.join([s['name'] for s in prop.get('multi_select', [])])
        
        elif prop_type == 'date':
            date = prop.get('date')
            return date['start'] if date else ''
        
        elif prop_type == 'checkbox':
            return 'はい' if prop.get('checkbox') else 'いいえ'
        
        elif prop_type == 'url':
            return prop.get('url', '')
        
        elif prop_type == 'email':
            return prop.get('email', '')
        
        elif prop_type == 'phone_number':
            return prop.get('phone_number', '')
        
        else:
            return ''
