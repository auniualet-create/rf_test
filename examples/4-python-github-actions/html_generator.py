"""HTML生成モジュール"""

import html
from typing import Dict, Any


class HTMLGenerator:
    """ECモール用HTML生成クラス"""
    
    @staticmethod
    def escape(text: str) -> str:
        """HTMLエスケープ"""
        return html.escape(str(text)) if text else ''
    
    @staticmethod
    def nl2br(text: str) -> str:
        """改行を<br>タグに変換"""
        escaped = HTMLGenerator.escape(text)
        return escaped.replace('\n', '<br>')
    
    def generate_yahoo_html(self, product: Dict[str, Any]) -> str:
        """
        Yahoo Shopping用HTML生成
        
        Args:
            product: 商品データ辞書
            
        Returns:
            HTML文字列
        """
        html_template = '''<table width="100%" border="0" cellpadding="3" cellspacing="2" bgcolor="#fff">
  <tr>
    <td width="25%" bgcolor="#FFCC99">名称</td>
    <td>{name}</td>
  </tr>
  
  <tr>
    <td class="abst" bgcolor="#FFCC99">原材料名</td>
    <td>{ingredients}</td>
  </tr>
  
  <tr>
    <td bgcolor="#FFCC99">アレルゲン</td>
    <td>{allergen}</td>
  </tr>
  
  <tr>
    <td bgcolor="#FFCC99">栄養成分表示</td>
    <td>{nutrition}</td>
  </tr>
  
  <tr>
    <td bgcolor="#FFCC99">内容量</td>
    <td>{content}</td>
  </tr>
  
  <tr>
    <td bgcolor="#FFCC99">賞味期限</td>
    <td>{expiry}</td>
  </tr>
  
  <tr>
    <td bgcolor="#FFCC99">保存方法</td>
    <td>{storage}</td>
  </tr>
  
  <tr>
    <td bgcolor="#FFCC99">製造者/出荷元</td>
    <td>{manufacturer}</td>
  </tr>
</table>'''
        
        return html_template.format(
            name=self.escape(product.get('name', '')),
            ingredients=self.nl2br(product.get('ingredients', '')),
            allergen=self.nl2br(product.get('allergen', '')),
            nutrition=self.nl2br(product.get('nutrition', '')),
            content=self.escape(product.get('content', '')),
            expiry=self.escape(product.get('expiry', '')),
            storage=self.escape(product.get('storage', '')),
            manufacturer=self.nl2br(product.get('manufacturer', ''))
        )
    
    def generate_rakuten_html(self, product: Dict[str, Any]) -> str:
        """
        楽天市場用HTML生成
        
        Args:
            product: 商品データ辞書
            
        Returns:
            HTML文字列
        """
        html_template = '''<table width="100%" border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse;">
  <tr style="background-color: #FFE4B5;">
    <th width="150">名称</th>
    <td>{name}</td>
  </tr>
  
  <tr style="background-color: #FFE4B5;">
    <th>原材料名</th>
    <td>{ingredients}</td>
  </tr>
  
  <tr style="background-color: #FFE4B5;">
    <th>アレルゲン</th>
    <td>{allergen}</td>
  </tr>
  
  <tr style="background-color: #FFE4B5;">
    <th>栄養成分表示</th>
    <td>{nutrition}</td>
  </tr>
  
  <tr style="background-color: #FFE4B5;">
    <th>内容量</th>
    <td>{content}</td>
  </tr>
  
  <tr style="background-color: #FFE4B5;">
    <th>賞味期限</th>
    <td>{expiry}</td>
  </tr>
  
  <tr style="background-color: #FFE4B5;">
    <th>保存方法</th>
    <td>{storage}</td>
  </tr>
  
  <tr style="background-color: #FFE4B5;">
    <th>製造者/出荷元</th>
    <td>{manufacturer}</td>
  </tr>
</table>'''
        
        return html_template.format(
            name=self.escape(product.get('name', '')),
            ingredients=self.nl2br(product.get('ingredients', '')),
            allergen=self.nl2br(product.get('allergen', '')),
            nutrition=self.nl2br(product.get('nutrition', '')),
            content=self.escape(product.get('content', '')),
            expiry=self.escape(product.get('expiry', '')),
            storage=self.escape(product.get('storage', '')),
            manufacturer=self.nl2br(product.get('manufacturer', ''))
        )
