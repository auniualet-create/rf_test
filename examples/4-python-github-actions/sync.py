#!/usr/bin/env python3
"""
Notion → ECモール 商品データ同期スクリプト

このスクリプトは以下の処理を実行します：
1. Notion APIから商品データを取得
2. 各ECモール用のHTMLを生成
3. ECモールAPIを使って商品ページを更新
"""

import os
import sys
import logging
from datetime import datetime
from typing import List, Dict, Any

from dotenv import load_dotenv
from colorama import init, Fore, Style

from notion_client_wrapper import NotionClient
from html_generator import HTMLGenerator
from ec_clients.yahoo import YahooShoppingClient
from ec_clients.rakuten import RakutenClient

# カラー出力の初期化
init(autoreset=True)

# ロガーの設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('sync.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)


class NotionECSyncManager:
    """Notion → ECモール同期マネージャー"""
    
    def __init__(self):
        """初期化"""
        load_dotenv()
        
        # 設定の読み込み
        self.dry_run = os.getenv('DRY_RUN', 'false').lower() == 'true'
        
        # クライアントの初期化
        self.notion = NotionClient(
            api_key=os.getenv('NOTION_API_KEY'),
            database_id=os.getenv('NOTION_DATABASE_ID')
        )
        
        self.html_generator = HTMLGenerator()
        
        self.yahoo = YahooShoppingClient(
            api_key=os.getenv('YAHOO_API_KEY'),
            api_secret=os.getenv('YAHOO_API_SECRET'),
            store_account=os.getenv('YAHOO_STORE_ACCOUNT')
        )
        
        self.rakuten = RakutenClient(
            service_secret=os.getenv('RAKUTEN_SERVICE_SECRET'),
            license_key=os.getenv('RAKUTEN_LICENSE_KEY')
        )
        
        logger.info(f"{Fore.GREEN}同期マネージャーを初期化しました")
        if self.dry_run:
            logger.warning(f"{Fore.YELLOW}⚠️  DRY RUNモード: 実際の更新は行いません")
    
    def sync_all_products(self) -> Dict[str, Any]:
        """全商品を同期"""
        logger.info(f"{Fore.CYAN}=== 商品データ同期開始 ===")
        start_time = datetime.now()
        
        results = {
            'success': 0,
            'failed': 0,
            'skipped': 0,
            'total': 0,
            'errors': []
        }
        
        try:
            # 1. Notionから商品データを取得
            logger.info(f"{Fore.CYAN}📖 Notionから商品データを取得中...")
            products = self.notion.fetch_all_products()
            results['total'] = len(products)
            
            if not products:
                logger.warning(f"{Fore.YELLOW}⚠️  商品データが見つかりませんでした")
                return results
            
            logger.info(f"{Fore.GREEN}✓ {len(products)}件の商品データを取得しました")
            
            # 2. 各商品を処理
            for idx, product in enumerate(products, 1):
                logger.info(f"\n{Fore.CYAN}--- 商品 {idx}/{len(products)}: {product.get('name', 'N/A')} ---")
                
                try:
                    self._sync_single_product(product)
                    results['success'] += 1
                    logger.info(f"{Fore.GREEN}✓ 同期成功")
                    
                except Exception as e:
                    results['failed'] += 1
                    error_msg = f"商品ID: {product.get('id', 'N/A')}, エラー: {str(e)}"
                    results['errors'].append(error_msg)
                    logger.error(f"{Fore.RED}✗ 同期失敗: {str(e)}")
            
            # 3. 結果サマリー
            duration = (datetime.now() - start_time).total_seconds()
            self._print_summary(results, duration)
            
        except Exception as e:
            logger.error(f"{Fore.RED}致命的なエラー: {str(e)}")
            results['errors'].append(f"致命的エラー: {str(e)}")
        
        return results
    
    def _sync_single_product(self, product: Dict[str, Any]):
        """単一商品を同期"""
        product_id = product.get('id', 'N/A')
        
        # 1. HTMLを生成
        logger.info(f"  📝 HTML生成中...")
        yahoo_html = self.html_generator.generate_yahoo_html(product)
        rakuten_html = self.html_generator.generate_rakuten_html(product)
        
        # 2. Yahoo Shoppingに更新
        if product.get('yahoo_product_id'):
            logger.info(f"  🔄 Yahoo Shopping更新中...")
            if not self.dry_run:
                self.yahoo.update_product(
                    product_id=product['yahoo_product_id'],
                    html_content=yahoo_html
                )
            else:
                logger.info(f"  {Fore.YELLOW}(DRY RUN: 実際の更新はスキップ)")
        else:
            logger.warning(f"  {Fore.YELLOW}⚠️  Yahoo商品IDが未設定のためスキップ")
        
        # 3. 楽天に更新
        if product.get('rakuten_product_id'):
            logger.info(f"  🔄 楽天市場更新中...")
            if not self.dry_run:
                self.rakuten.update_product(
                    product_id=product['rakuten_product_id'],
                    html_content=rakuten_html
                )
            else:
                logger.info(f"  {Fore.YELLOW}(DRY RUN: 実際の更新はスキップ)")
        else:
            logger.warning(f"  {Fore.YELLOW}⚠️  楽天商品IDが未設定のためスキップ")
    
    def _print_summary(self, results: Dict[str, Any], duration: float):
        """結果サマリーを出力"""
        logger.info(f"\n{Fore.CYAN}{'='*50}")
        logger.info(f"{Fore.CYAN}同期完了サマリー")
        logger.info(f"{Fore.CYAN}{'='*50}")
        logger.info(f"総商品数:   {results['total']}")
        logger.info(f"{Fore.GREEN}成功:       {results['success']}")
        logger.info(f"{Fore.RED}失敗:       {results['failed']}")
        logger.info(f"{Fore.YELLOW}スキップ:   {results['skipped']}")
        logger.info(f"実行時間:   {duration:.2f}秒")
        
        if results['errors']:
            logger.info(f"\n{Fore.RED}エラー詳細:")
            for error in results['errors']:
                logger.error(f"  - {error}")
        
        logger.info(f"{Fore.CYAN}{'='*50}\n")


def main():
    """メイン処理"""
    try:
        # 環境変数のチェック
        required_vars = ['NOTION_API_KEY', 'NOTION_DATABASE_ID']
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            logger.error(f"{Fore.RED}必須の環境変数が設定されていません: {', '.join(missing_vars)}")
            sys.exit(1)
        
        # 同期実行
        manager = NotionECSyncManager()
        results = manager.sync_all_products()
        
        # 終了コード設定
        if results['failed'] > 0:
            sys.exit(1)  # エラーあり
        else:
            sys.exit(0)  # 正常終了
            
    except KeyboardInterrupt:
        logger.warning(f"\n{Fore.YELLOW}処理が中断されました")
        sys.exit(130)
    except Exception as e:
        logger.error(f"{Fore.RED}予期しないエラー: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
