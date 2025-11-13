#!/usr/bin/env python3
"""
zipファイルをbase64エンコードして表示するヘルパースクリプト
ローカルPCでこのスクリプトを実行すると、zipファイルが復元されます
"""
import base64

# base64エンコードされたzipファイルのデータ
# この下に、ターミナルから取得したbase64データを貼り付けてください

BASE64_DATA = """
# ここにbase64データを貼り付け
"""

def main():
    if not BASE64_DATA.strip() or BASE64_DATA.strip().startswith("#"):
        print("エラー: BASE64_DATAにbase64エンコードされたデータを貼り付けてください")
        return
    
    try:
        # base64デコード
        zip_data = base64.b64decode(BASE64_DATA.strip())
        
        # zipファイルとして保存
        with open("notion-ecommerce-sync.zip", "wb") as f:
            f.write(zip_data)
        
        print("✓ notion-ecommerce-sync.zip が正常に作成されました！")
        print(f"  ファイルサイズ: {len(zip_data)} bytes")
        
    except Exception as e:
        print(f"エラー: {e}")

if __name__ == "__main__":
    main()
