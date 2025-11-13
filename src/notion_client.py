"""
Notion APIクライアント
Notionの商品ページからデータを取得する
"""
import os
from typing import Dict, List, Optional
from notion_client import Client
from dotenv import load_dotenv

load_dotenv()


class NotionProductClient:
    """Notionから商品情報を取得するクライアント"""
    
    def __init__(self):
        api_key = os.getenv("NOTION_API_KEY")
        if not api_key:
            raise ValueError("NOTION_API_KEYが設定されていません")
        self.client = Client(auth=api_key)
    
    def get_page_content(self, page_id: str) -> Dict:
        """
        Notionページの内容を取得
        
        Args:
            page_id: NotionページのID
            
        Returns:
            ページの内容を含む辞書
        """
        try:
            page = self.client.pages.retrieve(page_id)
            return page
        except Exception as e:
            raise Exception(f"Notionページの取得に失敗しました: {e}")
    
    def get_page_blocks(self, page_id: str) -> List[Dict]:
        """
        Notionページのブロック（コンテンツ）を取得
        
        Args:
            page_id: NotionページのID
            
        Returns:
            ブロックのリスト
        """
        try:
            blocks = []
            cursor = None
            
            while True:
                response = self.client.blocks.children.list(
                    block_id=page_id,
                    start_cursor=cursor
                )
                blocks.extend(response.get("results", []))
                
                if not response.get("has_more"):
                    break
                cursor = response.get("next_cursor")
            
            return blocks
        except Exception as e:
            raise Exception(f"Notionブロックの取得に失敗しました: {e}")
    
    def search_pages_by_database(self, database_id: str, filter_conditions: Optional[Dict] = None) -> List[Dict]:
        """
        データベースからページを検索
        
        Args:
            database_id: NotionデータベースのID
            filter_conditions: フィルタ条件（オプション）
            
        Returns:
            ページのリスト
        """
        try:
            query = {"database_id": database_id}
            if filter_conditions:
                query["filter"] = filter_conditions
            
            results = []
            cursor = None
            
            while True:
                if cursor:
                    query["start_cursor"] = cursor
                
                response = self.client.databases.query(**query)
                results.extend(response.get("results", []))
                
                if not response.get("has_more"):
                    break
                cursor = response.get("next_cursor")
            
            return results
        except Exception as e:
            raise Exception(f"Notionデータベースの検索に失敗しました: {e}")
    
    def extract_text_from_blocks(self, blocks: List[Dict]) -> str:
        """
        ブロックからテキストを抽出
        
        Args:
            blocks: Notionブロックのリスト
            
        Returns:
            抽出されたテキスト
        """
        text_parts = []
        
        for block in blocks:
            block_type = block.get("type")
            
            if block_type == "paragraph":
                rich_text = block.get("paragraph", {}).get("rich_text", [])
                text = self._extract_rich_text(rich_text)
                if text:
                    text_parts.append(text)
            
            elif block_type == "heading_1":
                rich_text = block.get("heading_1", {}).get("rich_text", [])
                text = self._extract_rich_text(rich_text)
                if text:
                    text_parts.append(f"<h1>{text}</h1>")
            
            elif block_type == "heading_2":
                rich_text = block.get("heading_2", {}).get("rich_text", [])
                text = self._extract_rich_text(rich_text)
                if text:
                    text_parts.append(f"<h2>{text}</h2>")
            
            elif block_type == "heading_3":
                rich_text = block.get("heading_3", {}).get("rich_text", [])
                text = self._extract_rich_text(rich_text)
                if text:
                    text_parts.append(f"<h3>{text}</h3>")
            
            elif block_type == "bulleted_list_item":
                rich_text = block.get("bulleted_list_item", {}).get("rich_text", [])
                text = self._extract_rich_text(rich_text)
                if text:
                    text_parts.append(f"<li>{text}</li>")
            
            elif block_type == "numbered_list_item":
                rich_text = block.get("numbered_list_item", {}).get("rich_text", [])
                text = self._extract_rich_text(rich_text)
                if text:
                    text_parts.append(f"<li>{text}</li>")
            
            # 子ブロックがある場合は再帰的に処理
            if block.get("has_children"):
                children = self.get_page_blocks(block["id"])
                child_text = self.extract_text_from_blocks(children)
                if child_text:
                    text_parts.append(child_text)
        
        return "\n".join(text_parts)
    
    def _extract_rich_text(self, rich_text: List[Dict]) -> str:
        """
        リッチテキストからテキストを抽出（HTML形式）
        
        Args:
            rich_text: Notionのリッチテキスト配列
            
        Returns:
            HTML形式のテキスト
        """
        html_parts = []
        
        for text_obj in rich_text:
            text = text_obj.get("plain_text", "")
            annotations = text_obj.get("annotations", {})
            
            # 装飾の適用
            if annotations.get("bold"):
                text = f"<strong>{text}</strong>"
            if annotations.get("italic"):
                text = f"<em>{text}</em>"
            if annotations.get("code"):
                text = f"<code>{text}</code>"
            
            # リンクの処理
            if text_obj.get("href"):
                text = f'<a href="{text_obj["href"]}">{text}</a>'
            
            html_parts.append(text)
        
        return "".join(html_parts)
    
    def format_as_html(self, blocks: List[Dict], wrap_in_list: bool = True) -> str:
        """
        ブロックをHTML形式に変換
        
        Args:
            blocks: Notionブロックのリスト
            wrap_in_list: リストアイテムを<ul>で囲むかどうか
            
        Returns:
            HTML形式の文字列
        """
        html_parts = []
        in_list = False
        
        for block in blocks:
            block_type = block.get("type")
            
            if block_type in ["bulleted_list_item", "numbered_list_item"]:
                if not in_list:
                    html_parts.append("<ul>" if wrap_in_list else "")
                    in_list = True
                
                rich_text = block.get(block_type, {}).get("rich_text", [])
                text = self._extract_rich_text(rich_text)
                if text:
                    html_parts.append(f"<li>{text}</li>")
            else:
                if in_list:
                    html_parts.append("</ul>" if wrap_in_list else "")
                    in_list = False
                
                if block_type == "paragraph":
                    rich_text = block.get("paragraph", {}).get("rich_text", [])
                    text = self._extract_rich_text(rich_text)
                    if text:
                        html_parts.append(f"<p>{text}</p>")
                
                elif block_type == "heading_1":
                    rich_text = block.get("heading_1", {}).get("rich_text", [])
                    text = self._extract_rich_text(rich_text)
                    if text:
                        html_parts.append(f"<h1>{text}</h1>")
                
                elif block_type == "heading_2":
                    rich_text = block.get("heading_2", {}).get("rich_text", [])
                    text = self._extract_rich_text(rich_text)
                    if text:
                        html_parts.append(f"<h2>{text}</h2>")
                
                elif block_type == "heading_3":
                    rich_text = block.get("heading_3", {}).get("rich_text", [])
                    text = self._extract_rich_text(rich_text)
                    if text:
                        html_parts.append(f"<h3>{text}</h3>")
            
            # 子ブロックの処理
            if block.get("has_children"):
                children = self.get_page_blocks(block["id"])
                child_html = self.format_as_html(children, wrap_in_list=False)
                html_parts.append(child_html)
        
        if in_list:
            html_parts.append("</ul>" if wrap_in_list else "")
        
        return "\n".join(html_parts)
