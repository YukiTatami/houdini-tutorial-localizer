#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""マークダウン学習ガイド生成ツール"""

import argparse
import json
import re
import sys
from pathlib import Path
from datetime import datetime

class MarkdownGenerator:
    def __init__(self):
        self.subtitle_segments = []
        self.node_insertions = []
        self.series_name = ""
        self.chapter_number = ""
        self.chapter_title = ""
        self.total_chapters = 6
        self.video_url = ""  # 動画URL（外部から設定可能）
        
    def extract_series_info(self, subtitle_file_path):
        """ファイルパスからシリーズ情報を抽出"""
        try:
            path = Path(subtitle_file_path)
            path_parts = path.parts
            
            # tutorials/Project_Skylark_Bridges/01_raw_data/chapter_02_basic_logic/transcript_*.srt
            # からシリーズ名とチャプター情報を抽出
            for i, part in enumerate(path_parts):
                if part == "tutorials" and i + 1 < len(path_parts):
                    self.series_name = path_parts[i + 1].replace("_", " ")
                elif part.startswith("chapter_"):
                    # chapter_02_basic_logic から番号とタイトルを抽出
                    chapter_parts = part.split("_", 2)
                    if len(chapter_parts) >= 3:
                        self.chapter_number = chapter_parts[1].lstrip("0") or "0"  # ゼロ埋めを削除
                        self.chapter_title = chapter_parts[2].replace("_", "")
                        
                        # 日本語タイトルマッピング
                        title_mapping = {
                            "introduction": "導入", "basiclogic": "基本ロジック", "bridgestructure": "橋梁構造",
                            "details": "詳細", "finishingtouches": "仕上げ", "finaltouches": "最終調整"
                        }
                        self.chapter_title = title_mapping.get(self.chapter_title, self.chapter_title)
            
            # シリーズ名からSideFX公式チュートリアルページのURLを設定
            if not self.video_url and self.series_name:
                tutorial_url = self.generate_sidefx_tutorial_url(self.series_name)
                if tutorial_url:
                    self.video_url = tutorial_url
                        
            
        except Exception as e:
            self.series_name = "Project Skylark Bridges"
            self.chapter_number = "Unknown"
            self.chapter_title = "Unknown"
    
    def generate_sidefx_tutorial_url(self, series_name):
        """シリーズ名からSideFX公式チュートリアルページのURLを生成"""
        if not series_name:
            return None
        
        # シリーズ名をURLフレンドリーな形式に変換
        url_name = series_name.lower().replace(' ', '-').replace('_', '-')
        return f"https://www.sidefx.com/ja/tutorials/{url_name}/"
    
    def get_video_duration(self):
        """最後の字幕セグメントから動画時間を取得"""
        if not self.subtitle_segments:
            return "Unknown"
        
        last_segment = self.subtitle_segments[-1]
        end_time = last_segment['end_time']
        # HH:MM:SS,mmm → HH:MM:SS 形式に変換
        return end_time.split(',')[0]
        
    def parse_srt_file(self, srt_file_path):
        """SRTファイルをパースしてセグメントリストを生成"""
        try:
            with open(srt_file_path, 'r', encoding='utf-8') as file:
                content = file.read().strip()
            
            # SRTセグメントを分割（空行で区切られている）
            segments = re.split(r'\n\s*\n', content)
            
            for segment_text in segments:
                if not segment_text.strip():
                    continue
                
                lines = segment_text.strip().split('\n')
                if len(lines) < 3:
                    continue
                
                # セグメント ID
                segment_id = lines[0].strip()
                
                # タイムスタンプ行
                timestamp_line = lines[1].strip()
                timestamp_match = re.match(r'(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})', timestamp_line)
                
                if not timestamp_match:
                    continue
                
                start_time = timestamp_match.group(1)
                end_time = timestamp_match.group(2)
                
                # 字幕テキスト（3行目以降）
                subtitle_text = '\n'.join(lines[2:]).strip()
                
                segment = {
                    'id': segment_id,
                    'start_time': start_time,
                    'end_time': end_time,
                    'text': subtitle_text,
                    'start_seconds': self.timestamp_to_seconds(start_time),
                    'end_seconds': self.timestamp_to_seconds(end_time)
                }
                
                self.subtitle_segments.append(segment)
                
            return True
            
        except Exception as e:
            return False
    
    def parse_node_data(self, node_file_path):
        """ノードデータJSONファイルをパース"""
        try:
            with open(node_file_path, 'r', encoding='utf-8') as file:
                self.node_insertions = json.load(file)
            
            # タイムスタンプを秒に変換して追加
            for node in self.node_insertions:
                if 'insert_after_timestamp' in node:
                    # HH:MM:SS形式をHH:MM:SS,000形式に変換
                    timestamp = node['insert_after_timestamp']
                    if ',' not in timestamp:
                        timestamp = timestamp + ',000'
                    node['insert_seconds'] = self.timestamp_to_seconds(timestamp)
            
            return True
            
        except Exception as e:
            return False
    
    def timestamp_to_seconds(self, timestamp):
        """タイムスタンプ (HH:MM:SS,mmm) を秒に変換"""
        # カンマをピリオドに置換
        timestamp = timestamp.replace(',', '.')
        
        parts = timestamp.split(':')
        hours = int(parts[0])
        minutes = int(parts[1])
        seconds_parts = parts[2].split('.')
        seconds = int(seconds_parts[0])
        milliseconds = int(seconds_parts[1]) if len(seconds_parts) > 1 else 0
        
        return hours * 3600 + minutes * 60 + seconds + milliseconds / 1000
    
    def format_timestamp_for_markdown(self, timestamp):
        """マークダウン表示用のタイムスタンプ形式 (HH:MM:SS) に変換"""
        # HH:MM:SS,mmm → HH:MM:SS
        return timestamp.split(',')[0]
    
    def extract_node_type(self, doc_link):
        """ドキュメントリンクからノード種別を抽出"""
        try:
            # URLから /sop/, /dop/, /rop/ などを抽出して大文字化
            match = re.search(r'/([a-z]+)/[^/]+$', doc_link.lower())
            if match:
                return match.group(1).upper()
        except:
            pass
        return ""
    
    def find_best_segment_for_node(self, node_insert_time):
        """ノード挿入タイミングに最も近いセグメントのインデックスを検索"""
        best_segment_idx = None
        min_distance = float('inf')
        
        for idx, segment in enumerate(self.subtitle_segments):
            segment_start = segment['start_seconds']
            segment_end = segment['end_seconds']
            
            # ノードの挿入タイミングがセグメント開始時刻と一致する場合、このセグメントに配置
            if abs(node_insert_time - segment_start) < 0.1:  # 0.1秒の許容誤差
                return idx
            
            # セグメント範囲内の場合（終了時刻は含まない）
            if segment_start <= node_insert_time < segment_end:
                return idx
            
            # セグメント終了時刻からの距離を計算（後続セグメントの場合）
            if node_insert_time >= segment_end:
                distance = node_insert_time - segment_end
                if distance < min_distance:
                    min_distance = distance
                    best_segment_idx = idx
        
        return best_segment_idx
    
    def generate_markdown_content(self):
        """マークダウンコンテンツ生成"""
        markdown_lines = []
        
        video_duration = self.get_video_duration()
        
        markdown_lines.append(f"# {self.series_name} - Chapter {self.chapter_number}: {self.chapter_title} 学習ガイド（日本語版）")
        markdown_lines.append("")
        markdown_lines.append("**シリーズ情報**:")
        markdown_lines.append("")
        markdown_lines.append(f"- シリーズ: {self.series_name}")
        markdown_lines.append(f"- チャプター: {self.chapter_number} / {self.total_chapters}")
        
        # 動画URLの設定（リンクまたは単純テキスト）
        if self.video_url:
            markdown_lines.append(f"- 動画URL: [{self.series_name}]({self.video_url})")
        else:
            markdown_lines.append(f"- 動画URL: {self.series_name}")
            
        markdown_lines.append(f"- 時間: {video_duration}")
        markdown_lines.append("")
        markdown_lines.append("---")
        markdown_lines.append("")
        
        # 各ノードに対して最適なセグメントを事前計算
        nodes_by_segment = {}
        for node in self.node_insertions:
            node_insert_time = node.get('insert_seconds', 0)
            best_segment_idx = self.find_best_segment_for_node(node_insert_time)
            
            if best_segment_idx is not None:
                if best_segment_idx not in nodes_by_segment:
                    nodes_by_segment[best_segment_idx] = []
                nodes_by_segment[best_segment_idx].append(node)
        
        # 各字幕セグメントを処理
        for idx, segment in enumerate(self.subtitle_segments):
            # セグメントタイトル（タイムスタンプ）
            timestamp_display = self.format_timestamp_for_markdown(segment['start_time'])
            markdown_lines.append(f"## {timestamp_display}")
            markdown_lines.append("")
            
            # 字幕テキスト（引用形式）
            subtitle_text = segment['text']
            markdown_lines.append(f'「{subtitle_text}」')
            markdown_lines.append("")
            
            # このセグメントに割り当てられたノードを挿入
            if idx in nodes_by_segment:
                for node in nodes_by_segment[idx]:
                    node_name = node.get('node_name', 'Unknown Node')
                    doc_link = node.get('doc_link_ja', '#')
                    
                    # ノード種別を抽出してノード名に追加
                    node_type = self.extract_node_type(doc_link)
                    if node_type:
                        full_node_name = f"{node_name} {node_type}"
                    else:
                        full_node_name = node_name
                    
                    # ノード情報を📝アイコン付きで挿入
                    markdown_lines.append(f"📝 **[{full_node_name}]({doc_link})**")
                    markdown_lines.append("")
            
            markdown_lines.append("---")
            markdown_lines.append("")
        
        return '\n'.join(markdown_lines)
    
    def generate_markdown_file(self, output_file_path):
        """マークダウンファイルを生成"""
        try:
            markdown_content = self.generate_markdown_content()
            
            # 出力ディレクトリを作成
            output_path = Path(output_file_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # ファイルに書き込み
            with open(output_file_path, 'w', encoding='utf-8') as file:
                file.write(markdown_content)
            
            print(f"マークダウン生成完了: {output_file_path}")
            
            return True
            
        except Exception as e:
            return False

def main():
    """メイン処理"""
    parser = argparse.ArgumentParser(
        description='Houdiniチュートリアル学習ガイドマークダウン生成ツール',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--subtitle-file',
        required=True,
        help='翻訳済み日本語字幕ファイル (.srt)'
    )
    
    parser.add_argument(
        '--node-data', 
        required=False,
        help='ノード挿入データファイル (.json) - オプション'
    )
    
    parser.add_argument(
        '--output',
        required=True, 
        help='出力マークダウンファイル (.md)'
    )
    
    parser.add_argument(
        '--video-url',
        required=False,
        help='動画URL（オプション）'
    )
    
    args = parser.parse_args()
    
    # ファイル存在確認
    subtitle_file = Path(args.subtitle_file)
    
    if not subtitle_file.exists():
        print(f"[ERROR] 字幕ファイルが見つかりません: {subtitle_file}")
        sys.exit(1)
    
    # node-dataはオプションなので指定された場合のみ確認
    node_file = None
    if args.node_data:
        node_file = Path(args.node_data)
        if not node_file.exists():
            print(f"[ERROR] ノードデータファイルが見つかりません: {node_file}")
            sys.exit(1)
    
    print("[START] マークダウン生成開始...")
    print(f"[INPUT] 字幕ファイル: {subtitle_file}")
    if node_file:
        print(f"[INPUT] ノードデータ: {node_file}")
    else:
        print("[INPUT] ノードデータ: なし（シンプルモード）")
    print(f"[OUTPUT] 出力ファイル: {args.output}")
    print()
    
    # マークダウン生成実行
    generator = MarkdownGenerator()
    
    # 動画URLを設定（オプション）
    if args.video_url:
        generator.video_url = args.video_url
    
    # シリーズ情報を抽出
    generator.extract_series_info(subtitle_file)
    
    # ファイル解析
    if not generator.parse_srt_file(subtitle_file):
        sys.exit(1)
    
    # ノードデータが指定された場合のみ解析
    if node_file and not generator.parse_node_data(node_file):
        sys.exit(1)
    
    # マークダウン生成
    if not generator.generate_markdown_file(args.output):
        sys.exit(1)
    
    print()
    print("[COMPLETE] マークダウン生成処理が正常に完了しました！")

if __name__ == "__main__":
    main()