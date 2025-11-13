"""
メイン実行スクリプト
"""
import argparse
import sys
import os
from sync_service import SyncService, ProductMapping

# パスを追加
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def main():
    parser = argparse.ArgumentParser(description="Notionからeコマースプラットフォームへの同期")
    parser.add_argument(
        "--notion-page-id",
        required=True,
        help="NotionページのID"
    )
    parser.add_argument(
        "--yahoo-item-code",
        help="Yahooショッピングの商品コード"
    )
    parser.add_argument(
        "--rakuten-item-code",
        help="楽天の商品コード"
    )
    parser.add_argument(
        "--use-browser",
        action="store_true",
        help="Yahooでブラウザ自動化を使用する"
    )
    parser.add_argument(
        "--mapping-file",
        help="商品マッピングファイルのパス（JSON形式）"
    )
    
    args = parser.parse_args()
    
    # 同期サービスを初期化
    sync_service = SyncService()
    
    # マッピングファイルが指定されている場合は使用
    yahoo_code = args.yahoo_item_code
    rakuten_code = args.rakuten_item_code
    
    if args.mapping_file:
        mapping = ProductMapping(args.mapping_file)
        if not yahoo_code:
            yahoo_code = mapping.get_yahoo_code(args.notion_page_id)
        if not rakuten_code:
            rakuten_code = mapping.get_rakuten_code(args.notion_page_id)
    
    # 同期実行
    if not yahoo_code and not rakuten_code:
        print("エラー: Yahooまたは楽天の商品コードを指定してください")
        sys.exit(1)
    
    results = sync_service.sync_all(
        notion_page_id=args.notion_page_id,
        yahoo_item_code=yahoo_code,
        rakuten_item_code=rakuten_code,
        use_browser_for_yahoo=args.use_browser
    )
    
    # 結果を表示
    print("\n=== 同期結果 ===")
    for result in results:
        platform = result.get("platform")
        success = result.get("success", False)
        status = "✓ 成功" if success else "✗ 失敗"
        
        print(f"{platform}: {status}")
        
        if not success:
            error = result.get("error", "不明なエラー")
            print(f"  エラー: {error}")
        else:
            method = result.get("method", "unknown")
            print(f"  方法: {method}")
    
    # エラーがある場合は終了コード1を返す
    if any(not r.get("success", False) for r in results):
        sys.exit(1)


if __name__ == "__main__":
    main()
