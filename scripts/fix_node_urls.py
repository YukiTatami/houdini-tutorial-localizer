#!/usr/bin/env python3
"""
ノードデータのURLをHoudini公式ドキュメント日本語版に修正するスクリプト
"""

import json
import re
from pathlib import Path

def fix_node_url(old_url):
    """Houdini公式ドキュメントの正しい日本語版URL形式に変換"""
    # パターンマッチ: https://docs.sidefx.com/vex/lang/ja/{type}/{node}
    match = re.match(r'https://docs\.sidefx\.com/vex/lang/ja/([^/]+)/([^/]+)$', old_url)
    if match:
        node_type = match.group(1)
        node_name = match.group(2)
        return f"https://www.sidefx.com/ja/docs/houdini/nodes/{node_type}/{node_name}.html"
    
    return old_url

def fix_json_file(json_file_path):
    """JSONファイル内のURLを修正"""
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        fixed_count = 0
        for item in data:
            if 'doc_link_ja' in item:
                old_url = item['doc_link_ja']
                new_url = fix_node_url(old_url)
                if old_url != new_url:
                    item['doc_link_ja'] = new_url
                    fixed_count += 1
                    print(f"修正: {item['node_name']}")
                    print(f"  {old_url}")
                    print(f"  → {new_url}")
        
        if fixed_count > 0:
            with open(json_file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"\n[OK] {fixed_count}個のURLを修正しました: {json_file_path}")
        else:
            print(f"修正対象なし: {json_file_path}")
            
    except Exception as e:
        print(f"[ERROR] エラー: {e}")

def main():
    # Chapter 02のノードデータを修正
    json_file = Path("tutorials/Project_Skylark_Bridges/02_analysis_data/chapter_02_node_insertions.json")
    
    if json_file.exists():
        print(f"[START] {json_file} のURL修正を開始...")
        fix_json_file(json_file)
    else:
        print(f"[ERROR] ファイルが見つかりません: {json_file}")

if __name__ == "__main__":
    main()