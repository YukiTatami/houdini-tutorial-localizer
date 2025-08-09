#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SRT品質修正ツール"""

import re
import sys
import os
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional


class SRTQualityFixer:
    """SRT品質修正を行うクラス"""
    
    def __init__(self, target_duration: int = 40, completion_threshold: float = 0.8):
        """
        初期化
        
        Args:
            target_duration: 目標セグメント時間（秒）
            completion_threshold: 文完結時の早期終了閾値（0.0-1.0）
        """
        self.target_duration = target_duration
        self.completion_threshold = completion_threshold
        self.stats = {
            'original_segments': 0,
            'fixed_segments': 0,
            'avg_original_duration': 0.0,
            'avg_fixed_duration': 0.0,
            'processing_time': 0.0
        }
    
    def parse_timestamp(self, timestamp_str: str) -> float:
        """SRTタイムスタンプを秒に変換"""
        try:
            time_parts = timestamp_str.split(':')
            hours = int(time_parts[0])
            minutes = int(time_parts[1])
            seconds_parts = time_parts[2].split(',')
            seconds = int(seconds_parts[0])
            milliseconds = int(seconds_parts[1])
            
            return hours * 3600 + minutes * 60 + seconds + milliseconds / 1000.0
        except (ValueError, IndexError) as e:
            raise ValueError(f"タイムスタンプの解析に失敗しました: {timestamp_str} - {e}")
    
    def seconds_to_timestamp(self, seconds: float) -> str:
        """秒をSRTタイムスタンプに変換"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        milliseconds = int((seconds % 1) * 1000)
        
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{milliseconds:03d}"
    
    def parse_srt_file(self, file_path: Path) -> List[Dict]:
        """SRTファイルを解析してセグメントリストを返す"""
        print(f"[INFO] ファイルを読み込み中: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"ファイルが見つかりません: {file_path}")
        except Exception as e:
            raise Exception(f"ファイルの読み込みに失敗しました: {e}")
        
        # JavaScriptエスケープ文字を処理
        content = content.replace('\\\\n', '\\n')
        content = content.replace('\\n', '\n')
        content = content.strip('\"').strip("'")
        
        # セグメントを分割
        segments = []
        current_segment = ""
        
        for line in content.split('\n'):
            line = line.strip()
            if not line:
                if current_segment:
                    segments.append(current_segment)
                    current_segment = ""
            else:
                current_segment += line + "\n"
        
        if current_segment:
            segments.append(current_segment)
        
        # セグメントを解析
        parsed_segments = []
        failed_segments = 0
        
        for i, segment in enumerate(segments):
            try:
                lines = segment.strip().split('\n')
                if len(lines) >= 3:
                    # セグメント番号のクリーンアップ（JavaScriptエラー対応）
                    segment_num_str = lines[0].strip()
                    # 不正な文字（バックスラッシュ等）を削除
                    segment_num_str = re.sub(r'[^\d]', '', segment_num_str)
                    if not segment_num_str:
                        raise ValueError(f"セグメント番号が無効: '{lines[0]}'")
                    segment_num = int(segment_num_str)
                    
                    timestamp_line = lines[1].strip()
                    # タイムスタンプラインのクリーンアップ
                    timestamp_line = re.sub(r'[^\d:,\->\s]', '', timestamp_line)
                    
                    text_lines = lines[2:]
                    
                    # タイムスタンプを解析
                    timestamp_match = re.match(
                        r'(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2},\d{3})', 
                        timestamp_line
                    )
                    if timestamp_match:
                        start_time = self.parse_timestamp(timestamp_match.group(1))
                        end_time = self.parse_timestamp(timestamp_match.group(2))
                        
                        text = ' '.join(text_lines).strip()
                        
                        parsed_segments.append({
                            'number': segment_num,
                            'start': start_time,
                            'end': end_time,
                            'text': text,
                            'duration': end_time - start_time
                        })
                    else:
                        failed_segments += 1
                        print(f"[WARNING] セグメント {i+1}: タイムスタンプの解析失敗")
                else:
                    failed_segments += 1
                    print(f"[WARNING] セグメント {i+1}: 不正な形式")
            except (ValueError, IndexError) as e:
                failed_segments += 1
                print(f"[WARNING] セグメント {i+1}: 解析エラー - {e}")
        
        print(f"[SUCCESS] 解析完了: {len(parsed_segments)}セグメント（失敗: {failed_segments}）")
        return parsed_segments
    
    def fix_segments(self, segments: List[Dict]) -> List[Dict]:
        """セグメントを品質修正"""
        print(f"[INFO] 品質修正を開始（目標: {self.target_duration}秒、完結閾値: {self.completion_threshold:.0%}）")
        
        fixed_segments = []
        current_group = []
        current_group_start = None
        current_group_end = None
        
        for i, segment in enumerate(segments):
            if not current_group:
                # 新しいグループ開始
                current_group = [segment]
                current_group_start = segment['start']
                current_group_end = segment['end']
            else:
                # 現在のグループに追加するかどうか判断
                potential_duration = segment['end'] - current_group_start
                
                # 文完結性を確認
                last_text = current_group[-1]['text'].rstrip()
                is_sentence_complete = last_text.endswith(('.', '!', '?'))
                
                # グループ終了条件
                should_end_group = (
                    potential_duration >= self.target_duration or
                    (is_sentence_complete and 
                     potential_duration >= self.target_duration * self.completion_threshold)
                )
                
                if should_end_group:
                    # 現在のグループを完成させる
                    combined_text = ' '.join([seg['text'] for seg in current_group])
                    combined_text = self._normalize_text(combined_text)
                    
                    fixed_segments.append({
                        'start': current_group_start,
                        'end': current_group_end,
                        'text': combined_text,
                        'duration': current_group_end - current_group_start,
                        'original_count': len(current_group)
                    })
                    
                    # 新しいグループ開始
                    current_group = [segment]
                    current_group_start = segment['start']
                    current_group_end = segment['end']
                else:
                    # 現在のグループに追加
                    current_group.append(segment)
                    current_group_end = segment['end']
            
            # 進捗表示
            if (i + 1) % 10 == 0:
                print(f"   進捗: {i+1}/{len(segments)} ({(i+1)/len(segments)*100:.1f}%)")
        
        # 最後のグループを処理
        if current_group:
            combined_text = ' '.join([seg['text'] for seg in current_group])
            combined_text = self._normalize_text(combined_text)
            
            fixed_segments.append({
                'start': current_group_start,
                'end': current_group_end,
                'text': combined_text,
                'duration': current_group_end - current_group_start,
                'original_count': len(current_group)
            })
        
        print(f"[SUCCESS] 品質修正完了: {len(segments)} → {len(fixed_segments)}セグメント")
        return fixed_segments
    
    def _normalize_text(self, text: str) -> str:
        """テキストを正規化"""
        text = text.strip()
        
        # 複数スペースを単一スペースに
        text = re.sub(r'\s+', ' ', text)
        
        # 文末にピリオドを追加（必要に応じて）
        if text and not text.endswith(('.', '!', '?')):
            text += '.'
        
        return text
    
    def write_srt_file(self, segments: List[Dict], output_path: Path) -> None:
        """修正されたセグメントをSRTファイルに書き出し"""
        print(f"[INFO] ファイルを書き込み中: {output_path}")
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                for i, segment in enumerate(segments, 1):
                    f.write(f"{i}\n")
                    f.write(f"{self.seconds_to_timestamp(segment['start'])} --> {self.seconds_to_timestamp(segment['end'])}\n")
                    f.write(f"{segment['text']}\n\n")
            
            print(f"[SUCCESS] 書き込み完了: {output_path}")
        except Exception as e:
            raise Exception(f"ファイルの書き込みに失敗しました: {e}")
    
    def calculate_stats(self, original_segments: List[Dict], fixed_segments: List[Dict]) -> None:
        """統計情報を計算"""
        self.stats['original_segments'] = len(original_segments)
        self.stats['fixed_segments'] = len(fixed_segments)
        
        if original_segments:
            self.stats['avg_original_duration'] = sum(seg['duration'] for seg in original_segments) / len(original_segments)
        
        if fixed_segments:
            self.stats['avg_fixed_duration'] = sum(seg['duration'] for seg in fixed_segments) / len(fixed_segments)
    
    def print_stats(self) -> None:
        """統計情報を表示"""
        print(f"処理完了: {self.stats['original_segments']} → {self.stats['fixed_segments']}セグメント")
    
    def fix_srt_quality(self, input_path: Path, output_path: Path) -> bool:
        """SRTファイルの品質修正を実行"""
        start_time = datetime.now()
        
        try:
            # ファイル存在確認
            if not input_path.exists():
                raise FileNotFoundError(f"入力ファイルが見つかりません: {input_path}")
            
            # 出力ディレクトリが存在しない場合は作成
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 処理実行
            original_segments = self.parse_srt_file(input_path)
            fixed_segments = self.fix_segments(original_segments)
            self.write_srt_file(fixed_segments, output_path)
            
            # 統計計算
            self.calculate_stats(original_segments, fixed_segments)
            self.stats['processing_time'] = (datetime.now() - start_time).total_seconds()
            
            # 結果表示
            self.print_stats()
            
            return True
            
        except Exception as e:
            print(f"[ERROR] エラー: {e}")
            return False


def main():
    """メイン処理"""
    parser = argparse.ArgumentParser(
        description="Vimeo翻訳ワークフロー - SRT品質修正ツール",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  python srt_quality_fixer.py input.srt output.srt
  python srt_quality_fixer.py input.srt output.srt --target-duration 30
  python srt_quality_fixer.py input.srt output.srt --completion-threshold 0.9
        """
    )
    
    parser.add_argument('input_file', help='入力SRTファイルパス')
    parser.add_argument('output_file', help='出力SRTファイルパス')
    parser.add_argument('--target-duration', type=int, default=40,
                        help='目標セグメント時間（秒）（デフォルト: 40）')
    parser.add_argument('--completion-threshold', type=float, default=0.8,
                        help='文完結時の早期終了閾値（0.0-1.0）（デフォルト: 0.8）')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='詳細な出力を表示')
    
    args = parser.parse_args()
    
    # 引数検証
    if not 0.0 <= args.completion_threshold <= 1.0:
        print("[ERROR] エラー: completion-threshold は 0.0-1.0 の範囲で指定してください")
        sys.exit(1)
    
    if args.target_duration <= 0:
        print("[ERROR] エラー: target-duration は正の数で指定してください")
        sys.exit(1)
    
    # パス処理
    input_path = Path(args.input_file)
    output_path = Path(args.output_file)
    
    print("=== Vimeo翻訳ワークフロー - SRT品質修正ツール ===")
    print(f"入力: {input_path}")
    print(f"出力: {output_path}")
    print(f"設定: 目標時間={args.target_duration}秒, 完結閾値={args.completion_threshold:.0%}")
    print()
    
    # 修正実行
    fixer = SRTQualityFixer(
        target_duration=args.target_duration,
        completion_threshold=args.completion_threshold
    )
    
    success = fixer.fix_srt_quality(input_path, output_path)
    
    if success:
        print("\n[SUCCESS] 処理が正常に完了しました！")
        sys.exit(0)
    else:
        print("\n[FAILED] 処理に失敗しました")
        sys.exit(1)


if __name__ == "__main__":
    main()