#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Houdini Tutorial Analysis Batch Translator
===========================================

バッチ処理による分析データの日本語翻訳
確立された専門用語の一貫性を維持

使用方法:
    python batch_translator.py chapter_02_analysis.json
"""

import json
import os
import sys
from pathlib import Path

class HoudiniAnalysisTranslator:
    def __init__(self):
        # 既存の用語集（Chapter 01から継承）
        self.established_glossary = {
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
        
        # 新規用語の翻訳
        self.new_translations = {}
        
    def translate_chapter_02(self, analysis_data):
        """Chapter 02 分析データの翻訳"""
        
        translated_data = {
            "chapter_info": {
                "number": analysis_data["chapter_info"]["number"],
                "title": "基本ロジック",
                "duration_seconds": analysis_data["chapter_info"]["duration_seconds"],
                "video_id": analysis_data["chapter_info"]["video_id"]
            },
            "houdini_nodes": [],
            "technical_concepts": [],
            "learning_segments": [],
            "series_continuity": {},
            "vex_code_examples": []
        }
        
        # Houdiniノード翻訳
        for node in analysis_data["houdini_nodes"]:
            translated_node = {
                "node_name": node["node_name"],  # ノード名は英語のまま保持
                "node_type": node["node_type"],
                "first_appearance_timestamp": node["first_appearance_timestamp"],
                "usage_frequency": node["usage_frequency"],
                "context": self._translate_context(node["context"]),
                "series_first_appearance": node["series_first_appearance"]
            }
            translated_data["houdini_nodes"].append(translated_node)
        
        # 技術概念翻訳
        for concept in analysis_data["technical_concepts"]:
            translated_concept = {
                "concept": self._translate_concept_name(concept["concept"]),
                "introduction_timestamp": concept["introduction_timestamp"],
                "importance": self._translate_importance(concept["importance"]),
                "prerequisites": [self._translate_prerequisite(p) for p in concept["prerequisites"]],
                "builds_upon": [self._translate_concept_name(bu) for bu in concept["builds_upon"]]
            }
            translated_data["technical_concepts"].append(translated_concept)
        
        # 学習セグメント翻訳
        for segment in analysis_data["learning_segments"]:
            translated_segment = {
                "start_time": segment["start_time"],
                "end_time": segment["end_time"],
                "title": self._translate_segment_title(segment["title"]),
                "objectives": [self._translate_objective(obj) for obj in segment["objectives"]],
                "key_concepts": [self._translate_key_concept(kc) for kc in segment["key_concepts"]],
                "nodes_introduced": segment["nodes_introduced"]  # ノード名は英語のまま
            }
            translated_data["learning_segments"].append(translated_segment)
        
        # シリーズ継続性翻訳
        translated_data["series_continuity"] = {
            "references_to_previous": [
                self._translate_reference(ref) for ref in analysis_data["series_continuity"]["references_to_previous"]
            ],
            "concepts_continued": [
                self._translate_concept_name(cc) for cc in analysis_data["series_continuity"]["concepts_continued"]
            ],
            "new_concepts_introduced": [
                self._translate_concept_name(nci) for nci in analysis_data["series_continuity"]["new_concepts_introduced"]
            ],
            "nodes_from_previous_chapters": analysis_data["series_continuity"]["nodes_from_previous_chapters"]
        }
        
        # VEXコード例翻訳
        for vex in analysis_data["vex_code_examples"]:
            translated_vex = {
                "purpose": self._translate_vex_purpose(vex["purpose"]),
                "timestamp": vex["timestamp"],
                "code_snippet": vex["code_snippet"]  # コードは英語のまま
            }
            translated_data["vex_code_examples"].append(translated_vex)
        
        return translated_data
    
    def _translate_context(self, context):
        """コンテキストの翻訳"""
        translations = {
            "Creating landscape placeholder geometry": "ランドスケーププレースホルダージオメトリの作成",
            "Adding noise to grid for terrain creation": "地形作成のためのグリッドへのノイズ追加",
            "Adding terrain variation": "地形バリエーションの追加",
            "Creating environment assets (boulders)": "環境アセット（巨石）の作成",
            "Combining geometry elements": "ジオメトリ要素の結合",
            "Drawing bridge path in polygon mode": "ポリゴンモードでの橋の経路描画",
            "Adding consistent detail to curves": "カーブへの一貫した詳細の追加",
            "Ray casting points onto surfaces, sampling distances": "サーフェスへのポイントのレイキャスティング、距離のサンプリング",
            "Moving points along normals for offset": "オフセットのための法線に沿ったポイントの移動",
            "Splitting splines into individual primitives and reconnecting paths": "スプラインを個別プリミティブに分割し経路を再接続",
            "Converting attributes from points to primitives": "ポイントからプリミティブへのアトリビュート変換",
            "Separating geometry based on attributes": "アトリビュートに基づくジオメトリの分離",
            "Marking positions in network for organization": "ネットワーク整理のための位置マーキング",
            "Randomizing point positions and scale attributes": "ポイント位置とスケールアトリビュートのランダム化",
            "Isolating middle points of hanging bridges": "吊り橋の中央ポイントの分離",
            "Processing each spline segment individually for incline calculation": "勾配計算のための各スプラインセグメントの個別処理",
            "Writing VEX code for incline calculation and stair flattening": "勾配計算と階段平坦化のためのVEXコード記述",
            "Reconnecting overlapping points after for loop": "forループ後の重複ポイントの再接続",
            "Marking different bridge sections for identification": "識別のための異なる橋セクションのマーキング",
            "Visual differentiation of bridge logic sections": "橋ロジックセクションの視覚的差別化",
            "Creating placeholder wooden plank geometry": "木製板材プレースホルダージオメトリの作成",
            "Spawning planks along curve points": "カーブポイントに沿った板材の生成",
            "Creating orientation attributes for proper plank alignment": "適切な板材配置のための方向アトリビュートの作成",
            "Creating scale attributes for plank sizing": "板材サイジングのためのスケールアトリビュート作成",
            "Adding organic variation to normal attributes": "法線アトリビュートへの有機的バリエーション追加"
        }
        return translations.get(context, context)
    
    
    def _translate_concept_name(self, concept):
        """概念名翻訳"""
        translations = {
            "Placeholder Geometry Creation": "プレースホルダージオメトリ作成",
            "Curve Drawing and Snapping": "カーブ描画とスナッピング",
            "Spline Preprocessing": "スプライン前処理",
            "Ray Casting and Surface Projection": "レイキャスティングとサーフェス投影",
            "Point Group Management": "ポイントグループ管理",
            "Attribute Manipulation": "アトリビュート操作",
            "Hanging Bridge Logic": "吊り橋ロジック",
            "VEX Programming Basics": "VEXプログラミング基礎",
            "Bounding Box Operations": "バウンディングボックス操作",
            "Orientation Control": "方向制御",
            "Scale Attributes": "スケールアトリビュート",
            "Procedural Variation": "プロシージャルバリエーション",
            "VEX programming": "VEXプログラミング",
            "Attribute-based workflow": "アトリビュートベースワークフロー",
            "Point group management": "ポイントグループ管理",
            "Orientation control system": "方向制御システム",
            "Ray casting techniques": "レイキャスティング技術",
            "Procedural variation methods": "プロシージャルバリエーション手法",
            "Conditional logic in Houdini": "Houdiniでの条件ロジック",
            "Spline manipulation and refinement": "スプライン操作と精密化"
        }
        
        # 直接マッピング優先で処理
        if concept in translations:
            return translations[concept]
        
        # 用語の完全一致処理
        result = concept
        for eng, jp in self.established_glossary.items():
            result = result.replace(eng, jp)
        
        return result
    
    def _translate_importance(self, importance):
        """重要度翻訳"""
        translations = {
            "fundamental": "基礎",
            "core": "中核", 
            "intermediate": "中級",
            "advanced": "上級",
            "specific": "特殊"
        }
        return translations.get(importance, importance)
    
    def _translate_prerequisite(self, prerequisite):
        """前提条件翻訳"""
        translations = {
            "Basic 3D understanding": "基本的な3D理解",
            "Basic Houdini interface knowledge": "基本的なHoudiniインターフェース知識",
            "Curve understanding": "カーブの理解",
            "Point attributes": "ポイントアトリビュート",
            "Surface normals": "サーフェス法線",
            "Attribute understanding": "アトリビュートの理解",
            "Geometry spreadsheet": "ジオメトリスプレッドシート",
            "Data types": "データ型",
            "Distance calculations": "距離計算",
            "Randomization": "ランダム化",
            "Programming concepts": "プログラミング概念",
            "Coordinate systems": "座標系",
            "VEX basics": "VEX基礎",
            "Vectors": "ベクトル",
            "Normals": "法線",
            "Up vectors": "アップベクトル",
            "Attribute types": "アトリビュート型",
            "Vector understanding": "ベクトルの理解",
            "Noise functions": "ノイズ関数"
        }
        return translations.get(prerequisite, prerequisite)
    
    def _translate_segment_title(self, title):
        """セグメントタイトル翻訳"""
        translations = {
            "Environment Setup and Curve Drawing": "環境設定とカーブ描画",
            "Spline Preprocessing and Offset": "スプライン前処理とオフセット",
            "Bridge Logic Separation": "橋ロジック分離",
            "VEX Programming for Incline Detection": "勾配検出のためのVEXプログラミング",
            "Plank Spawning and Orientation": "板材生成と方向設定",
            "Variation and Final Adjustments": "バリエーションと最終調整"
        }
        return translations.get(title, title)
    
    def _translate_objective(self, objective):
        """目標翻訳"""
        translations = {
            "Create placeholder geometry for testing": "テスト用プレースホルダージオメトリの作成",
            "Set up curve drawing tools with snapping": "スナッピング付きカーブ描画ツールの設定",
            "Understand tool context and workflow": "ツールコンテキストとワークフローの理解",
            "Add detail to splines with resampling": "リサンプリングによるスプラインへの詳細追加",
            "Project curves onto environment": "環境へのカーブ投影",
            "Create minimum offset from surfaces": "サーフェスからの最小オフセット作成",
            "Separate bridge into functional sections": "橋の機能セクションへの分離",
            "Implement hanging bridge behavior": "吊り橋の動作実装",
            "Create conditional processing logic": "条件処理ロジックの作成",
            "Calculate spline segment inclines": "スプラインセグメント勾配の計算",
            "Create staircase detection logic": "階段検出ロジックの作成",
            "Apply conditional grouping with VEX": "VEXによる条件グループ化の適用",
            "Create placeholder plank geometry": "板材プレースホルダージオメトリの作成",
            "Implement proper orientation system": "適切な方向システムの実装",
            "Handle section transitions": "セクション遷移の処理",
            "Add scale variation to planks": "板材へのスケールバリエーション追加",
            "Implement organic orientation variation": "有機的方向バリエーションの実装",
            "Flatten stairs for proper functionality": "適切な機能のための階段平坦化"
        }
        return translations.get(objective, objective)
    
    def _translate_key_concept(self, key_concept):
        """キーコンセプト翻訳"""
        translations = {
            "Placeholder geometry importance": "プレースホルダージオメトリの重要性",
            "Curve node configuration": "カーブノード設定",
            "Primitive snapping for accuracy": "精度のためのプリミティブスナッピング",
            "Curve resampling for consistent detail": "一貫した詳細のためのカーブリサンプリング",
            "Ray casting for surface projection": "サーフェス投影のためのレイキャスティング",
            "Normal-based point movement": "法線ベースのポイント移動",
            "Attribute-based separation": "アトリビュートベース分離",
            "Distance threshold detection": "距離閾値検出",
            "Randomized sagging effect": "ランダム化された下降効果",
            "VEX code fundamentals": "VEXコード基礎",
            "Bounding box operations": "バウンディングボックス操作",
            "Conditional logic implementation": "条件ロジック実装",
            "Copy to points workflow": "ポイントへのコピーワークフロー",
            "Normal and up vector relationship": "法線とアップベクトルの関係",
            "Path connectivity importance": "パス接続性の重要性",
            "Scale attribute control": "スケールアトリビュート制御",
            "Noise vs randomization": "ノイズ対ランダム化",
            "VEX for normal manipulation": "法線操作のためのVEX"
        }
        return translations.get(key_concept, key_concept)
    
    def _translate_reference(self, reference):
        """参照翻訳"""
        translations = {
            "Spline mentioned as continuation from Chapter 1": "Chapter 1からの継続としてスプラインに言及"
        }
        return translations.get(reference, reference)
    
    def _translate_vex_purpose(self, purpose):
        """VEX目的翻訳"""
        translations = {
            "Calculate incline for staircase detection": "階段検出のための勾配計算",
            "Flatten stairs orientation": "階段方向の平坦化"
        }
        return translations.get(purpose, purpose)

def main():
    if len(sys.argv) != 2:
        print("使用方法: python batch_translator.py <input_analysis.json>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    # 入力ファイルのパス解決
    if not os.path.isabs(input_file):
        # tutorials/Project_Skylark_Bridges/02_english_analysis/ からの相対パス
        base_dir = Path(__file__).parent.parent / "tutorials" / "Project_Skylark_Bridges" / "02_english_analysis"
        input_path = base_dir / input_file
    else:
        input_path = Path(input_file)
    
    if not input_path.exists():
        print(f"エラー: ファイル {input_path} が見つかりません")
        sys.exit(1)
    
    # 出力パスの設定
    output_dir = input_path.parent.parent / "05_translation_batch"
    output_dir.mkdir(exist_ok=True)
    
    # 翻訳実行
    translator = HoudiniAnalysisTranslator()
    
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            analysis_data = json.load(f)
        
        translated_data = translator.translate_chapter_02(analysis_data)
        
        # 出力ファイル名生成
        output_filename = input_path.stem.replace('_analysis', '_analysis_jp') + '.json'
        output_path = output_dir / output_filename
        
        # 翻訳データ保存
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(translated_data, f, ensure_ascii=False, indent=2)
        
        print(f"翻訳完了: {output_path}")
        print(f"処理されたノード数: {len(translated_data['houdini_nodes'])}")
        print(f"処理された技術概念数: {len(translated_data['technical_concepts'])}")
        
    except Exception as e:
        print(f"エラー: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()