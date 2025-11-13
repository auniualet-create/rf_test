"""
同期サービス
Notionから各eコマースプラットフォームへの同期を実行
"""
import os
import logging
from typing import Dict, List, Optional
from dotenv import load_dotenv

from notion_client import NotionProductClient
from yahoo_client import YahooShoppingClient, YahooShoppingBrowserClient
from rakuten_client import RakutenClient

load_dotenv()

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class SyncService:
    """同期サービス"""
    
    def __init__(self):
        self.notion_client = NotionProductClient()
        self.yahoo_client = YahooShoppingClient()
        self.rakuten_client = RakutenClient()
        self.yahoo_browser_client = YahooShoppingBrowserClient()
    
    def sync_notion_to_yahoo(
        self,
        notion_page_id: str,
        yahoo_item_code: str,
        use_browser: bool = False
    ) -> Dict:
        """
        NotionのページをYahooショッピングに同期
        
        Args:
            notion_page_id: NotionページのID
            yahoo_item_code: Yahooショッピングの商品コード
            use_browser: ブラウザ自動化を使用するか（APIが使えない場合）
            
        Returns:
            同期結果
        """
        try:
            logger.info(f"Notionページ {notion_page_id} からデータを取得中...")
            
            # Notionからデータを取得
            blocks = self.notion_client.get_page_blocks(notion_page_id)
            html_content = self.notion_client.format_as_html(blocks)
            
            logger.info(f"取得したHTMLコンテンツ: {html_content[:100]}...")
            
            # Yahooショッピングに更新
            if use_browser:
                logger.info("ブラウザ自動化でYahooショッピングを更新中...")
                # ブラウザ自動化の場合は認証情報が必要
                username = os.getenv("YAHOO_USERNAME")
                password = os.getenv("YAHOO_PASSWORD")
                
                if not username or not password:
                    raise ValueError("ブラウザ自動化にはYAHOO_USERNAMEとYAHOO_PASSWORDが必要です")
                
                success = self.yahoo_browser_client.update_product_via_browser(
                    username=username,
                    password=password,
                    item_code=yahoo_item_code,
                    description_html=html_content
                )
                
                return {
                    "success": success,
                    "platform": "Yahooショッピング",
                    "method": "browser_automation"
                }
            else:
                logger.info("APIでYahooショッピングを更新中...")
                result = self.yahoo_client.update_product_description(
                    item_code=yahoo_item_code,
                    description_html=html_content
                )
                
                return {
                    "success": True,
                    "platform": "Yahooショッピング",
                    "method": "api",
                    "result": result
                }
        
        except Exception as e:
            logger.error(f"Yahooショッピングへの同期に失敗しました: {e}")
            return {
                "success": False,
                "platform": "Yahooショッピング",
                "error": str(e)
            }
    
    def sync_notion_to_rakuten(
        self,
        notion_page_id: str,
        rakuten_item_code: str
    ) -> Dict:
        """
        Notionのページを楽天に同期
        
        Args:
            notion_page_id: NotionページのID
            rakuten_item_code: 楽天の商品コード
            
        Returns:
            同期結果
        """
        try:
            logger.info(f"Notionページ {notion_page_id} からデータを取得中...")
            
            # Notionからデータを取得
            blocks = self.notion_client.get_page_blocks(notion_page_id)
            html_content = self.notion_client.format_as_html(blocks)
            
            logger.info(f"取得したHTMLコンテンツ: {html_content[:100]}...")
            
            # 楽天に更新
            logger.info("APIで楽天を更新中...")
            result = self.rakuten_client.update_product_description(
                item_code=rakuten_item_code,
                description_html=html_content
            )
            
            return {
                "success": True,
                "platform": "楽天",
                "method": "api",
                "result": result
            }
        
        except Exception as e:
            logger.error(f"楽天への同期に失敗しました: {e}")
            return {
                "success": False,
                "platform": "楽天",
                "error": str(e)
            }
    
    def sync_all(
        self,
        notion_page_id: str,
        yahoo_item_code: Optional[str] = None,
        rakuten_item_code: Optional[str] = None,
        use_browser_for_yahoo: bool = False
    ) -> List[Dict]:
        """
        すべてのプラットフォームに同期
        
        Args:
            notion_page_id: NotionページのID
            yahoo_item_code: Yahooショッピングの商品コード（オプション）
            rakuten_item_code: 楽天の商品コード（オプション）
            use_browser_for_yahoo: Yahooでブラウザ自動化を使用するか
            
        Returns:
            各プラットフォームの同期結果のリスト
        """
        results = []
        
        if yahoo_item_code:
            yahoo_result = self.sync_notion_to_yahoo(
                notion_page_id=notion_page_id,
                yahoo_item_code=yahoo_item_code,
                use_browser=use_browser_for_yahoo
            )
            results.append(yahoo_result)
        
        if rakuten_item_code:
            rakuten_result = self.sync_notion_to_rakuten(
                notion_page_id=notion_page_id,
                rakuten_item_code=rakuten_item_code
            )
            results.append(rakuten_result)
        
        return results


# 設定ファイルから商品マッピングを読み込む例
class ProductMapping:
    """NotionページIDと各プラットフォームの商品コードのマッピング"""
    
    def __init__(self, mapping_file: Optional[str] = None):
        """
        Args:
            mapping_file: マッピングファイルのパス（JSON形式）
        """
        self.mappings = {}
        
        if mapping_file and os.path.exists(mapping_file):
            import json
            with open(mapping_file, "r", encoding="utf-8") as f:
                self.mappings = json.load(f)
        else:
            # デフォルトのマッピング（環境変数から読み込む例）
            # 実際の実装では、データベースや設定ファイルから読み込む
            pass
    
    def get_yahoo_code(self, notion_page_id: str) -> Optional[str]:
        """NotionページIDからYahoo商品コードを取得"""
        return self.mappings.get(notion_page_id, {}).get("yahoo")
    
    def get_rakuten_code(self, notion_page_id: str) -> Optional[str]:
        """NotionページIDから楽天商品コードを取得"""
        return self.mappings.get(notion_page_id, {}).get("rakuten")
