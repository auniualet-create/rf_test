"""
定期実行スケジューラー
cronやタスクスケジューラーから呼び出される
"""
import os
import time
import json
import logging
from typing import List, Dict
from sync_service import SyncService, ProductMapping

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class Scheduler:
    """定期実行スケジューラー"""
    
    def __init__(self, mapping_file: str):
        """
        Args:
            mapping_file: 商品マッピングファイルのパス
        """
        self.sync_service = SyncService()
        self.mapping = ProductMapping(mapping_file)
        
        # マッピングファイルを読み込む
        if os.path.exists(mapping_file):
            with open(mapping_file, "r", encoding="utf-8") as f:
                self.product_mappings = json.load(f)
        else:
            logger.warning(f"マッピングファイルが見つかりません: {mapping_file}")
            self.product_mappings = {}
    
    def sync_all_products(self) -> List[Dict]:
        """
        すべての商品を同期
        
        Returns:
            各商品の同期結果のリスト
        """
        results = []
        
        for notion_page_id, platforms in self.product_mappings.items():
            logger.info(f"商品を同期中: NotionページID={notion_page_id}")
            
            yahoo_code = platforms.get("yahoo")
            rakuten_code = platforms.get("rakuten")
            use_browser = platforms.get("use_browser_for_yahoo", False)
            
            result = self.sync_service.sync_all(
                notion_page_id=notion_page_id,
                yahoo_item_code=yahoo_code,
                rakuten_item_code=rakuten_code,
                use_browser_for_yahoo=use_browser
            )
            
            # NotionページIDを結果に追加
            for r in result:
                r["notion_page_id"] = notion_page_id
            
            results.extend(result)
            
            # レート制限を考慮して少し待機
            time.sleep(1)
        
        return results
    
    def run_once(self):
        """一度だけ実行"""
        logger.info("定期同期を開始します...")
        results = self.sync_all_products()
        
        # 結果をログに記録
        success_count = sum(1 for r in results if r.get("success", False))
        total_count = len(results)
        
        logger.info(f"同期完了: {success_count}/{total_count} 成功")
        
        # エラーがある場合は詳細をログに記録
        for result in results:
            if not result.get("success", False):
                logger.error(
                    f"同期失敗 - "
                    f"NotionページID: {result.get('notion_page_id')}, "
                    f"プラットフォーム: {result.get('platform')}, "
                    f"エラー: {result.get('error')}"
                )


def main():
    """メイン関数（cronから呼び出される想定）"""
    mapping_file = os.getenv("PRODUCT_MAPPING_FILE", "product_mapping.json")
    
    scheduler = Scheduler(mapping_file)
    scheduler.run_once()


if __name__ == "__main__":
    main()
