"""
基本的な使用例
"""
import sys
import os

# プロジェクトルートをパスに追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.sync_service import SyncService


def example_sync_single_product():
    """単一商品の同期例"""
    
    # 同期サービスを初期化
    sync_service = SyncService()
    
    # NotionページIDと各プラットフォームの商品コード
    notion_page_id = "your-notion-page-id-here"
    yahoo_item_code = "yahoo-item-code-here"
    rakuten_item_code = "rakuten-item-code-here"
    
    # Yahooショッピングに同期（API使用）
    print("Yahooショッピングに同期中...")
    yahoo_result = sync_service.sync_notion_to_yahoo(
        notion_page_id=notion_page_id,
        yahoo_item_code=yahoo_item_code,
        use_browser=False  # APIを使用
    )
    print(f"結果: {yahoo_result}")
    
    # 楽天に同期
    print("\n楽天に同期中...")
    rakuten_result = sync_service.sync_notion_to_rakuten(
        notion_page_id=notion_page_id,
        rakuten_item_code=rakuten_item_code
    )
    print(f"結果: {rakuten_result}")


def example_sync_with_browser():
    """ブラウザ自動化を使用した同期例（Yahoo APIが使えない場合）"""
    
    sync_service = SyncService()
    
    notion_page_id = "your-notion-page-id-here"
    yahoo_item_code = "yahoo-item-code-here"
    
    # ブラウザ自動化を使用
    print("ブラウザ自動化でYahooショッピングに同期中...")
    result = sync_service.sync_notion_to_yahoo(
        notion_page_id=notion_page_id,
        yahoo_item_code=yahoo_item_code,
        use_browser=True  # ブラウザ自動化を使用
    )
    print(f"結果: {result}")


def example_sync_all_platforms():
    """すべてのプラットフォームに一度に同期"""
    
    sync_service = SyncService()
    
    notion_page_id = "your-notion-page-id-here"
    
    # すべてのプラットフォームに同期
    results = sync_service.sync_all(
        notion_page_id=notion_page_id,
        yahoo_item_code="yahoo-item-code-here",
        rakuten_item_code="rakuten-item-code-here",
        use_browser_for_yahoo=False
    )
    
    # 結果を表示
    for result in results:
        platform = result.get("platform")
        success = result.get("success", False)
        print(f"{platform}: {'成功' if success else '失敗'}")


if __name__ == "__main__":
    print("=== 基本的な使用例 ===\n")
    
    # 例1: 単一商品の同期
    # example_sync_single_product()
    
    # 例2: ブラウザ自動化を使用
    # example_sync_with_browser()
    
    # 例3: すべてのプラットフォームに同期
    # example_sync_all_platforms()
    
    print("使用例を実行するには、上記の関数のコメントアウトを解除してください。")
