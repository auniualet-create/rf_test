"""
Notionからデータを取得する例
"""
import sys
import os

# プロジェクトルートをパスに追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.notion_client import NotionProductClient


def example_get_page_content():
    """Notionページの内容を取得する例"""
    
    client = NotionProductClient()
    
    # NotionページIDを指定
    page_id = "your-notion-page-id-here"
    
    # ページの基本情報を取得
    page = client.get_page_content(page_id)
    print("ページ情報:")
    print(f"タイトル: {page.get('properties', {}).get('title', {}).get('title', [{}])[0].get('plain_text', 'N/A')}")
    
    # ページのブロック（コンテンツ）を取得
    blocks = client.get_page_blocks(page_id)
    print(f"\nブロック数: {len(blocks)}")
    
    # HTML形式に変換
    html_content = client.format_as_html(blocks)
    print("\n=== HTML形式のコンテンツ ===")
    print(html_content)
    
    # プレーンテキストとして抽出
    text_content = client.extract_text_from_blocks(blocks)
    print("\n=== テキスト形式のコンテンツ ===")
    print(text_content)


def example_search_database():
    """Notionデータベースから商品を検索する例"""
    
    client = NotionProductClient()
    
    # データベースIDを指定
    database_id = "your-database-id-here"
    
    # すべてのページを取得
    pages = client.search_pages_by_database(database_id)
    
    print(f"見つかったページ数: {len(pages)}")
    
    for page in pages:
        # ページのプロパティを表示
        properties = page.get("properties", {})
        print(f"\nページID: {page.get('id')}")
        
        # タイトルプロパティを探す（プロパティ名は実際のものに合わせて変更）
        for prop_name, prop_value in properties.items():
            if prop_value.get("type") == "title":
                title = prop_value.get("title", [{}])[0].get("plain_text", "N/A")
                print(f"タイトル: {title}")


if __name__ == "__main__":
    print("=== Notionデータ取得の例 ===\n")
    
    # 例1: ページの内容を取得
    # example_get_page_content()
    
    # 例2: データベースから検索
    # example_search_database()
    
    print("使用例を実行するには、上記の関数のコメントアウトを解除してください。")
