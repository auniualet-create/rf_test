#!/bin/bash
# zipファイルをbase64エンコードして出力するスクリプト
# 使用方法: bash download_zip.sh > zip_base64.txt
# その後、ローカルPCで base64 -d zip_base64.txt > notion-ecommerce-sync.zip を実行

base64 notion-ecommerce-sync.zip
