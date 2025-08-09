#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Terminology Tracker for Houdini Tutorial Series
================================================

シリーズ全体での用語一貫性管理

使用方法:
    python terminology_tracker.py chapter_02_analysis_jp.json
"""

import json
import os
import sys
from pathlib import Path

class TerminologyTracker:
    def __init__(self):
        # Chapter 02で新たに追加された用語
        self.new_chapter_02_terms = {
            # Technical Concepts
            "Placeholder Geometry Creation": "プレースホルダージオメトリ作成",
            "Curve Drawing and Snapping": "カーブ描画とスナッピング",
            "Spline Preprocessing": "スプライン前処理",
            "Ray Casting and Surface Projection": "レイキャスティングとサーフェス投影",
            "Point Group Management": "ポイントグループ管理",
            "Attribute Manipulation": "アトリビュート操作", 
            "Hanging Bridge Logic": "吊り橋ロジック",
            "VEX Programming Basics": "VEXプログラミング基礎",
            "Bounding Box Operations": "バウンディングボックス操作",
            "Scale Attributes": "スケールアトリビュート",
            "Procedural Variation": "プロシージャルバリエーション",
            
            # Node Contexts
            "Landscape placeholder geometry": "ランドスケーププレースホルダージオメトリ",
            "Terrain creation": "地形作成", 
            "Terrain variation": "地形バリエーション",
            "Environment assets": "環境アセット",
            "Bridge path": "橋の経路",
            "Curve resampling": "カーブリサンプリング",
            "Surface projection": "サーフェス投影",
            "Normal offset": "法線オフセット",
            "Spline segment": "スプラインセグメント",
            "Attribute conversion": "アトリビュート変換",
            "Geometry separation": "ジオメトリ分離",
            "Network organization": "ネットワーク整理",
            "Point randomization": "ポイントランダム化",
            "Hanging bridge": "吊り橋",
            "Incline calculation": "勾配計算",
            "Stair flattening": "階段平坦化",
            "Point reconnection": "ポイント再接続",
            "Bridge sections": "橋セクション",
            "Visual differentiation": "視覚的差別化",
            "Wooden plank": "木製板材",
            "Plank spawning": "板材生成",
            "Plank alignment": "板材配置",
            "Scale attribute": "スケールアトリビュート",
            "Organic variation": "有機的バリエーション",
            
            # Learning Objectives & Concepts
            "Environment Setup": "環境設定",
            "Tool Context": "ツールコンテキスト",
            "Minimum Offset": "最小オフセット",
            "Functional Sections": "機能セクション",
            "Conditional Processing": "条件処理",
            "Staircase Detection": "階段検出",
            "Conditional Grouping": "条件グループ化",
            "Section Transitions": "セクション遷移",
            "Scale Variation": "スケールバリエーション",
            "Orientation Variation": "方向バリエーション",
            
            # VEX Related
            "Incline Detection": "勾配検出",
            "Stair Detection Logic": "階段検出ロジック",
            "Normal Manipulation": "法線操作",
            
            # Workflow Terms
            "Copy to Points Workflow": "ポイントへのコピーワークフロー",
            "Up Vector": "アップベクトル",
            "Path Connectivity": "パス接続性",
            "Distance Threshold": "距離閾値",
            "Randomized Sagging": "ランダム化された下降",
            "Consistent Detail": "一貫した詳細",
            "Primitive Snapping": "プリミティブスナッピング"
        }
        
        # 既存用語集（Chapter 01から継承）
        self.established_terms = {
            "Spline": "スプライン",
            "Procedural Modeling": "プロシージャルモデリング",
            "Geometry Scattering": "ジオメトリの散布",
            "Transform": "トランスフォーム",
            "Attribute": "アトリビュート", 
            "Orientation Control": "方向制御",
            "Ray Casting": "レイキャスティング",
            "VEX Programming": "VEXプログラミング",
            "Bounding Box": "バウンディングボックス",
            "Point Group": "ポイントグループ",
            "Normal": "法線",
            "Scale Attribute": "スケール属性",
            "Noise": "ノイズ",
            "Randomization": "ランダム化"
        }
    
    def generate_updated_glossary(self):
        """Chapter 02完了後の更新された用語集を生成"""
        
        updated_glossary = {
            "series_info": {
                "name": "Project_Skylark_Bridges",
                "completed_chapters": 2,
                "last_updated_chapter": "chapter_02_basic_logic"
            },
            "consistent_translations": {
                **self.established_terms,
                **self.new_chapter_02_terms
            },
            "chapter_specific_additions": {
                "chapter_02": {
                    "focus_areas": [
                        "VEX Programming Introduction",
                        "Advanced Attribute Workflows", 
                        "Procedural Bridge Logic",
                        "Ray Casting Techniques",
                        "Conditional Processing"
                    ],
                    "key_new_terms": list(self.new_chapter_02_terms.keys())[:10]
                }
            },
            "node_specific_contexts": {
                "Grid": "ランドスケーププレースホルダージオメトリの作成",
                "Mountain": "地形作成のためのグリッドへのノイズ追加",
                "Noise": "地形バリエーションの追加",
                "Sphere": "環境アセット（巨石）の作成",
                "Merge": "ジオメトリ要素の結合",
                "Curve": "ポリゴンモードでの橋の経路描画",
                "Resample": "カーブへの一貫した詳細の追加",
                "Ray": "サーフェスへのポイントのレイキャスティング",
                "Peak": "オフセットのための法線に沿ったポイントの移動",
                "Convert Line": "スプラインを個別プリミティブに分割し経路を再接続",
                "Attribute Promote": "ポイントからプリミティブへのアトリビュート変換",
                "Split": "アトリビュートに基づくジオメトリの分離",
                "Null": "ネットワーク整理のための位置マーキング",
                "Attribute Randomize": "ポイント位置とスケールアトリビュートのランダム化",
                "Group by Range": "吊り橋の中央ポイントの分離",
                "For Each Primitive Loop": "勾配計算のための各スプラインセグメントの個別処理",
                "Attribute Wrangle": "勾配計算と階段平坦化のためのVEXコード記述",
                "Fuse": "forループ後の重複ポイントの再接続",
                "Group": "識別のための異なる橋セクションのマーキング",
                "Color": "橋ロジックセクションの視覚的差別化",
                "Box": "木製板材プレースホルダージオメトリの作成",
                "Copy to Points": "カーブポイントに沿った板材の生成",
                "Orient Along Curve": "適切な板材配置のための方向アトリビュートの作成",
                "Attribute Create": "板材サイジングのためのスケールアトリビュート作成",
                "Attribute Noise": "法線アトリビュートへの有機的バリエーション追加"
            }
        }
        
        return updated_glossary
    
    def save_updated_glossary(self, output_path):
        """更新された用語集を保存"""
        glossary = self.generate_updated_glossary()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(glossary, f, ensure_ascii=False, indent=2)
        
        return glossary

def main():
    tracker = TerminologyTracker()
    
    # 出力先ディレクトリの設定
    base_dir = Path(__file__).parent.parent / "tutorials" / "Project_Skylark_Bridges" / "05_translation_batch"
    base_dir.mkdir(exist_ok=True)
    
    # 更新された用語集を保存
    glossary_path = base_dir / "series_glossary_updated.json"
    updated_glossary = tracker.save_updated_glossary(glossary_path)
    
    print(f"更新された用語集を保存: {glossary_path}")
    print(f"確立された用語数: {len(updated_glossary['consistent_translations'])}")
    print(f"Chapter 02新規追加用語数: {len(tracker.new_chapter_02_terms)}")
    
    # 用語の統計表示
    print("\n== Chapter 02 重要新規用語 ==")
    for i, (eng, jp) in enumerate(tracker.new_chapter_02_terms.items()):
        if i < 10:  # 最初の10個のみ表示
            print(f"{eng} → {jp}")
        else:
            break
    
    if len(tracker.new_chapter_02_terms) > 10:
        print(f"... および他 {len(tracker.new_chapter_02_terms) - 10} 用語")

if __name__ == "__main__":
    main()