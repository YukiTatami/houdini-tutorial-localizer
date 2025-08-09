#!/usr/bin/env python3
"""
Vimeo翻訳ワークフロー - MD→HTML変換ツール

このスクリプトは、学習ガイドのMarkdownファイルを
スタイル付きHTMLファイルに変換します。
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple, Dict


class MDtoHTMLConverter:
    """MarkdownからHTMLへの変換を行うクラス"""
    
    def __init__(self):
        """初期化"""
        self.html_template = self._get_html_template()
        self.content_sections = []
        self.title = ""
        self.series_info = {}
        
    def _get_html_template(self) -> str:
        """HTMLテンプレートを返す"""
        return '''<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        :root {{
            --bg-primary: #ffffff;
            --bg-secondary: #f8fafc;
            --bg-accent: #f1f5f9;
            --text-primary: #1a202c;
            --text-secondary: #4a5568;
            --border-light: #e2e8f0;
            --border-medium: #cbd5e0;
            --highlight-bg: #ebf8ff;
            --highlight-border: #3182ce;
            --info-bg: #f0fff4;
            --success-bg: #f0fff4;
            --success-border: #38a169;
            --warning-bg: #fffaf0;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: var(--text-primary);
            background-color: var(--bg-primary);
            margin: 0;
            padding: 0;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }}

        .header {{
            background: linear-gradient(135deg, var(--highlight-bg), var(--info-bg));
            border-radius: 16px;
            padding: 2rem;
            margin-bottom: 2rem;
            border: 2px solid var(--highlight-border);
        }}

        .header h1 {{
            color: var(--highlight-border);
            margin: 0 0 1rem 0;
            font-size: 2rem;
        }}

        .series-info {{
            background: var(--bg-secondary);
            border-radius: 8px;
            padding: 1rem;
            margin-top: 1rem;
        }}

        .series-info strong {{
            color: var(--text-primary);
        }}

        /* コンテンツセクション */
        .content-section {{
            background: var(--bg-secondary);
            border: 1px solid var(--border-light);
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1.5rem 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }}

        /* セクションヘッダー */
        .section-header {{
            margin-bottom: 1rem;
            display: flex;
            align-items: flex-start;
            gap: 1rem;
        }}

        /* タイムスタンプ */
        .timestamp {{
            display: inline-block;
            background: linear-gradient(135deg, var(--highlight-bg), var(--info-bg));
            color: var(--highlight-border);
            font-weight: 700;
            font-size: 1.1rem;
            padding: 0.4rem 0.8rem;
            border-radius: 8px;
            border: 2px solid var(--highlight-border);
            margin-right: 0.8rem;
            font-family: 'Monaco', 'Consolas', monospace;
            min-width: 60px;
            text-align: center;
        }}

        /* 翻訳文（最重要要素） */
        .quote-text {{
            font-style: normal;
            color: var(--text-primary);
            font-size: 1.1rem;
            font-weight: 500;
            line-height: 1.7;
            flex: 1;
            background: linear-gradient(90deg, #f8fafc 0%, transparent 100%);
            padding: 0.8rem 1rem;
            border-radius: 8px;
            border-left: 4px solid var(--highlight-border);
        }}

        /* キーワード解説 */
        .keyword-explanation {{
            background: var(--bg-accent);
            border-left: 3px solid var(--border-medium);
            padding: 0.8rem;
            margin-top: 1rem;
            border-radius: 0 6px 6px 0;
        }}

        .keyword-explanation ul {{
            margin: 0.5rem 0;
            padding-left: 1.5rem;
        }}

        .keyword-explanation li {{
            margin: 0.3rem 0;
        }}

        /* ノード初出マーク */
        .node-debut {{
            display: inline-block;
            background: linear-gradient(135deg, var(--success-bg), var(--warning-bg));
            color: var(--success-border);
            font-weight: 700;
            font-size: 0.9rem;
            padding: 0.3rem 0.6rem;
            border-radius: 6px;
            border: 1px solid var(--success-border);
            margin-left: 0.5rem;
        }}

        .node-debut.series-debut {{
            background: linear-gradient(135deg, var(--success-bg), var(--warning-bg));
        }}

        .node-debut.chapter-debut {{
            background: linear-gradient(135deg, var(--info-bg), var(--highlight-bg));
            color: var(--highlight-border);
            border-color: var(--highlight-border);
        }}

        /* アイコン */
        .icon {{
            font-size: 1.2rem;
            margin-right: 0.5rem;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{title}</h1>
            <div class="series-info">
                {series_info}
            </div>
        </div>
        
        {content}
    </div>
</body>
</html>'''

    def _extract_title(self, line: str) -> str:
        """タイトルを抽出"""
        match = re.match(r'^#\s+(.+)$', line)
        if match:
            return match.group(1)
        return ""
    
    def _extract_series_info(self, lines: List[str], start_idx: int) -> Tuple[Dict[str, str], int]:
        """シリーズ情報を抽出"""
        info = {}
        idx = start_idx
        
        # 空行をスキップ
        while idx < len(lines) and not lines[idx].strip():
            idx += 1
        
        # リスト項目を処理
        while idx < len(lines):
            line = lines[idx].strip()
            
            # 終了条件
            if line.startswith('---') or line.startswith('#') or not line:
                break
                
            # リスト項目をパース: "- キー: 値"
            match = re.match(r'^-\s+(.+?):\s+(.+)$', line)
            if match:
                key, value = match.groups()
                info[key] = value
            idx += 1
            
        return info, idx
    
    def _format_series_info(self, info: Dict[str, str]) -> str:
        """シリーズ情報をHTML形式にフォーマット"""
        html_parts = []
        for key, value in info.items():
            # Markdownリンク [テキスト](URL) をHTMLリンクに変換
            value = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2" target="_blank">\1</a>', value)
            html_parts.append(f'<strong>{key}</strong>: {value}<br>')
        return '\n                '.join(html_parts)
    
    def _process_bold_text(self, text: str) -> str:
        """統一されたアスタリスク処理（全箇所で使用）"""
        if not text:
            return text
        
        # Markdownリンク [テキスト](URL) をHTMLリンクに変換
        text = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2" target="_blank">\1</a>', text)
        
        # 不正な*テキスト**:パターンを修正（*が1個、**が2個のケース）
        text = re.sub(r'(?<!\*)\*([^*]+?)\*\*:', r'<strong>\1:</strong>', text)
        
        # 不正な*テキスト**パターンを修正（*が1個、**が2個のケース）
        text = re.sub(r'(?<!\*)\*([^*]+?)\*\*(?!:)', r'<strong>\1</strong>', text)
        
        # 正常な**テキスト**: パターンを処理（コロンも太字に含める）
        text = re.sub(r'\*\*([^*]+?)\*\*:', r'<strong>\1:</strong>', text)
        
        # 残りの**テキスト**パターンを処理
        text = re.sub(r'\*\*([^*]+?)\*\*', r'<strong>\1</strong>', text)
        
        return text
    
    def _process_timestamp_section(self, lines: List[str], start_idx: int) -> Tuple[str, int]:
        """タイムスタンプセクションを処理"""
        # 両方のフォーマットに対応: MM:SS または HH:MM:SS
        timestamp_match = re.match(r'^##\s+(\d{2}:\d{2}(?::\d{2})?)$', lines[start_idx])
        if not timestamp_match:
            return "", start_idx + 1
            
        timestamp = timestamp_match.group(1)
        idx = start_idx + 1
        
        # 空行をスキップ
        while idx < len(lines) and not lines[idx].strip():
            idx += 1
        
        # 翻訳文を取得
        quote_text = ""
        if idx < len(lines) and lines[idx].strip().startswith('「') and lines[idx].strip().endswith('」'):
            quote_text = lines[idx].strip()
            idx += 1  # 翻訳文の行をスキップ
            
        # 翻訳文の後の空行もスキップ
        while idx < len(lines) and not lines[idx].strip():
            idx += 1
        
        # セクション内の解説部分を取得（翻訳文は既に処理済みなので除外される）
        explanation_lines = []
        while idx < len(lines):
            line = lines[idx].strip()
            # 次のセクション（##）で終了
            if line.startswith('## '):
                break
            # 区切り線で終了
            if line == '---':
                break
            # 内容を追加（空行も含める）
            explanation_lines.append(lines[idx])
            idx += 1
        
        # 解説部分をHTML化
        explanation_html = ""
        if explanation_lines:
            explanation_html = self._format_markdown_content_advanced('\n'.join(explanation_lines))
        
        # セクションHTMLを構築
        section_html = f'''
        <div class="content-section">
            <div class="section-header">
                <span class="timestamp">{timestamp}</span>
                <span class="quote-text">{quote_text}</span>
            </div>
{explanation_html}
        </div>'''
        
        return section_html, idx
    
    def _process_general_section(self, lines: List[str], start_idx: int) -> Tuple[str, int]:
        """通常のMarkdownセクション（## タイトル）を処理"""
        title_match = re.match(r'^##\s+(.+)$', lines[start_idx])
        if not title_match:
            return "", start_idx + 1
            
        title = title_match.group(1)
        idx = start_idx + 1
        content_lines = []
        
        # セクション内容を取得（サブセクションも含める）
        while idx < len(lines):
            line = lines[idx].strip()
            # 次の同レベル（##）セクションで終了
            if line.startswith('## ') and not line.startswith('### '):
                break
            # 区切り線で終了
            if line == '---':
                break
            # 内容を追加（空行も含める）
            content_lines.append(lines[idx])
            idx += 1
        
        # HTMLセクションを構築
        content_html = self._format_markdown_content_advanced('\n'.join(content_lines))
        section_html = f'''
        <div class="content-section">
            <h2>{title}</h2>
            {content_html}
        </div>'''
        
        return section_html, idx
    
    def _process_bold_section(self, lines: List[str], start_idx: int) -> Tuple[str, int]:
        """**太字項目**:セクションを処理"""
        bold_match = re.match(r'^\*\*(.+?)\*\*:?$', lines[start_idx])
        if not bold_match:
            return "", start_idx + 1
            
        title = bold_match.group(1)
        idx = start_idx + 1
        content_lines = []
        
        # セクション内容を取得
        while idx < len(lines):
            line = lines[idx].strip()
            # 次のセクションの開始で終了
            if line.startswith('##') or line.startswith('**') or line == '---':
                break
            if line:  # 空行以外を追加
                content_lines.append(lines[idx])
            elif content_lines:  # 内容がある場合は空行も含める
                content_lines.append(lines[idx])
            idx += 1
        
        # HTMLセクションを構築
        content_html = self._format_markdown_content('\n'.join(content_lines))
        section_html = f'''
        <div class="content-section">
            <h3><strong>{title}</strong></h3>
            {content_html}
        </div>'''
        
        return section_html, idx
    
    def _format_markdown_content(self, content: str) -> str:
        """Markdownコンテンツを基本的なHTMLに変換"""
        if not content.strip():
            return ""
        
        lines = content.split('\n')
        html_lines = []
        in_list = False
        
        for line in lines:
            line = line.strip()
            if not line:
                if in_list:
                    html_lines.append('</ul>')
                    in_list = False
                continue
                
            # リスト項目
            if line.startswith('- '):
                if not in_list:
                    html_lines.append('<ul>')
                    in_list = True
                item_content = line[2:].strip()
                # 太字の処理
                item_content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', item_content)
                html_lines.append(f'<li>{item_content}</li>')
            else:
                if in_list:
                    html_lines.append('</ul>')
                    in_list = False
                # 太字の処理
                line = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', line)
                html_lines.append(f'<p>{line}</p>')
        
        if in_list:
            html_lines.append('</ul>')
        
        return '\n'.join(html_lines)
    
    def _format_markdown_content_advanced(self, content: str) -> str:
        """高度なMarkdownコンテンツを詳細HTMLに変換（サブセクション、アイコン等対応）"""
        if not content.strip():
            return ""
        
        lines = content.split('\n')
        html_lines = []
        in_list = False
        in_numbered_list = False
        
        for line in lines:
            original_line = line
            line = line.strip()
            
            if not line:
                if in_list:
                    html_lines.append('</ul>')
                    in_list = False
                if in_numbered_list:
                    html_lines.append('</ol>')
                    in_numbered_list = False
                continue
            
            # サブセクション（### タイトル）
            if line.startswith('### '):
                if in_list:
                    html_lines.append('</ul>')
                    in_list = False
                if in_numbered_list:
                    html_lines.append('</ol>')
                    in_numbered_list = False
                title = line[4:].strip()
                html_lines.append(f'<h3>{title}</h3>')
                continue
            
            # 📝アイコン付きセクション
            if line.startswith('📝 '):
                if in_list:
                    html_lines.append('</ul>')
                    in_list = False
                if in_numbered_list:
                    html_lines.append('</ol>')
                    in_numbered_list = False
                content_part = line[3:].strip()
                # 統一されたアスタリスク処理を使用
                content_part = self._process_bold_text(content_part)
                html_lines.append(f'<div class="keyword-explanation"><span class="icon">📝</span> {content_part}</div>')
                continue
            
            # 番号付きリスト (1. 2. 3. など)
            if re.match(r'^\d+\.\s+', line):
                if in_list:
                    html_lines.append('</ul>')
                    in_list = False
                if not in_numbered_list:
                    html_lines.append('<ol>')
                    in_numbered_list = True
                item_content = re.sub(r'^\d+\.\s+', '', line)
                # 統一されたアスタリスク処理を使用
                item_content = self._process_bold_text(item_content)
                html_lines.append(f'<li>{item_content}</li>')
                continue
            
            # 通常のリスト項目 (- で始まる)
            if line.startswith('- '):
                if in_numbered_list:
                    html_lines.append('</ol>')
                    in_numbered_list = False
                if not in_list:
                    html_lines.append('<ul>')
                    in_list = True
                item_content = line[2:].strip()
                # 統一されたアスタリスク処理を使用
                item_content = self._process_bold_text(item_content)
                html_lines.append(f'<li>{item_content}</li>')
                continue
            
            # 通常の段落
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            if in_numbered_list:
                html_lines.append('</ol>')
                in_numbered_list = False
            
            # 統一されたアスタリスク処理を使用
            line = self._process_bold_text(line)
            html_lines.append(f'<p>{line}</p>')
        
        # 最後にリストを閉じる
        if in_list:
            html_lines.append('</ul>')
        if in_numbered_list:
            html_lines.append('</ol>')
        
        return '\n'.join(html_lines)
    
    def convert(self, md_content: str) -> str:
        """MarkdownをHTMLに変換"""
        lines = md_content.split('\n')
        idx = 0
        content_html = []
        
        # タイトルを抽出
        if lines[0].startswith('# '):
            self.title = self._extract_title(lines[0])
            idx = 1
        
        # 空行をスキップ
        while idx < len(lines) and not lines[idx].strip():
            idx += 1
        
        # シリーズ情報を抽出
        if idx < len(lines) and lines[idx].startswith('**シリーズ情報**'):
            idx += 1
            self.series_info, idx = self._extract_series_info(lines, idx)
        
        # 全てのセクションを処理
        while idx < len(lines):
            line = lines[idx].strip()
            
            # 空行をスキップ
            if not line:
                idx += 1
                continue
                
            # 区切り線をスキップ
            if line == '---':
                idx += 1
                continue
            
            # タイムスタンプセクション（## 00:09 または ## 00:00:01）を処理
            if re.match(r'^## \d{2}:\d{2}(?::\d{2})?$', line.strip()):
                section_html, idx = self._process_timestamp_section(lines, idx)
                if section_html:
                    content_html.append(section_html)
            
            # 通常のMarkdownセクション（## タイトル）を処理
            elif line.startswith('## '):
                section_html, idx = self._process_general_section(lines, idx)
                if section_html:
                    content_html.append(section_html)
            
            # **太字項目**を処理
            elif line.startswith('**') and line.endswith('**:'):
                section_html, idx = self._process_bold_section(lines, idx)
                if section_html:
                    content_html.append(section_html)
            
            else:
                idx += 1
        
        # HTMLを組み立て
        html = self.html_template.format(
            title=self.title,
            series_info=self._format_series_info(self.series_info),
            content='\n'.join(content_html)
        )
        
        return html


def main():
    """メイン処理"""
    if len(sys.argv) < 2:
        print("=== Vimeo翻訳ワークフロー - MD→HTML変換ツール ===")
        print("使用方法: python md_to_html_converter.py <MDファイルパス> [出力HTMLファイルパス]")
        print("")
        print("例:")
        print("  python md_to_html_converter.py chapter_01_学習ガイド.md")
        print("  python md_to_html_converter.py chapter_01_学習ガイド.md chapter_01_学習ガイド.html")
        print("")
        print("出力HTMLファイルパスを指定しない場合、.mdを.htmlに変更したファイル名で保存されます。")
        sys.exit(1)
    
    md_file_path = Path(sys.argv[1])
    
    # 出力パスの決定
    if len(sys.argv) >= 3:
        html_file_path = Path(sys.argv[2])
    else:
        html_file_path = md_file_path.with_suffix('.html')
    
    # ファイル存在確認
    if not md_file_path.exists():
        print(f"エラー: MDファイル '{md_file_path}' が見つかりません。")
        sys.exit(1)
    
    try:
        # MDファイルを読み込み
        with open(md_file_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # 変換実行
        converter = MDtoHTMLConverter()
        html_content = converter.convert(md_content)
        
        # HTMLファイルを書き込み
        with open(html_file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"変換完了: {md_file_path} → {html_file_path}")
        
    except Exception as e:
        print(f"エラー: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()