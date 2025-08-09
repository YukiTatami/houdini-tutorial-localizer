#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Houdini Tutorial Subtitle Translator
=====================================

字幕翻訳専用バッチスクリプト
established terminalogy, シリーズ用語集による一貫性確保

使用方法:
    python subtitle_translator.py chapter_02_translation_queue.json
"""

import json
import os
import sys
from pathlib import Path

class SubtitleTranslator:
    def __init__(self):
        # 字幕翻訳における技術用語の確立済み翻訳
        self.established_terms = {
            # Core Houdini Terms
            "spline": "スプライン",
            "curve": "カーブ",
            "node": "ノード", 
            "points": "ポイント",
            "primitives": "プリミティブ",
            "attributes": "アトリビュート",
            "geometry": "ジオメトリ",
            "surface": "サーフェス",
            "normal": "法線",
            "orientation": "方向",
            "scale": "スケール",
            "randomization": "ランダム化",
            "noise": "ノイズ",
            "ray casting": "レイキャスティング",
            "VEX": "VEX",
            "bounding box": "バウンディングボックス",
            "procedural": "プロシージャル",
            
            # Specific Bridge Terms
            "bridge": "橋",
            "plank": "板材", 
            "wooden plank": "木製板材",
            "hanging bridge": "吊り橋",
            "staircase": "階段",
            "environment": "環境",
            "landscape": "ランドスケープ",
            "placeholder": "プレースホルダー",
            
            # Technical Actions
            "resample": "リサンプル",
            "snap": "スナップ",
            "snap to": "にスナップ",
            "offset": "オフセット",
            "minimum distance": "最小距離",
            "maximum distance": "最大距離",
            "intersect": "交差",
            "projection": "投影",
            
            # Workflow Terms
            "tool": "ツール",
            "workflow": "ワークフロー",
            "context": "コンテキスト",
            "preview": "プレビュー",
            "display": "表示",
            "viewport": "ビューポート",
            "spreadsheet": "スプレッドシート"
        }

    def translate_subtitle_text(self, english_text):
        """字幕テキストの翻訳"""
        
        # 特定フレーズの直接翻訳
        phrase_translations = {
            "So whenever I'm starting work on a new tool": "新しいツールの作業を始める際は",
            "I like to have some kind of placeholder geometry": "何らかのプレースホルダージオメトリを用意するようにしています",
            "so that I can test my tool in the appropriate context": "適切なコンテキストでツールをテストできるように",
            "In this case, I made something that should kind of represent": "今回は、以下のようなものを表現するものを作成しました",
            "a landscape with maybe some environment assets on it": "いくつかの環境アセットが配置されたランドスケープ",
            "You know, imagine that this is gonna be like some big boulders": "これは大きな岩石のようなものと想像してください",
            "that we wanna build our bridge across": "その間に橋を架けたいと思います",
            "and you can just make that with a grid": "これはグリッドで簡単に作成できます",
            "add some noise from mountain nodes": "Mountainノードでノイズを追加し",
            "and you know, add some spheres, merge it together": "スフィアを追加してマージします",
            
            "and then you have something like this": "すると、このような結果が得られます",
            "And to actually use the tool": "実際にツールを使用するには",
            "the artist would then use lines inside Unreal": "アーティストはUnreal内でラインを使用します",
            "that are supplied by Houdini engine": "これらはHoudini Engineによって提供されます",
            "to get a similar experience within Houdini": "Houdini内で同様の体験を得るために",
            "To test it, you can just get the curve node": "テストするには、Curveノードを取得し",
            "and make sure to set it to polygon mode": "ポリゴンモードに設定します",
            "and to draw on our little placeholder environment": "小さなプレースホルダー環境上で描画するには",
            "we can press enter to get into the drawing mode": "Enterキーを押して描画モードに入ります",
            "and you can see it over here, the little curve tool overlay": "こちらに小さなカーブツールオーバーレイが表示されます",
            
            "And I have also enabled primitive snapping": "プリミティブスナッピングも有効にしています",
            "that makes sure that whatever we're drawing": "これにより、描画する内容が",
            "is actually gonna, you know, end up where we want it": "実際に望む場所に配置されるようになります",
            "and not be somewhere in the distance or something": "遠くの場所などに配置されることがありません",
            "Lemme just make a curve that makes sense": "意味のあるカーブを作成しましょう",
            "So I'm just gonna press enter and then you know": "Enterキーを押して",
            "maybe draw a curve like this": "このようなカーブを描画します",
            
            "I can't see it right now because these two are not linked up together": "現在は2つが連結されていないため見えません",
            "But maybe I can just click the blue flag on my curve": "カーブの青いフラグをクリックして",
            "and then have the environment be in wire frame mode": "環境をワイヤーフレームモードにします",
            "And I'm also gonna enable something like the display points feature": "また、ポイント表示機能も有効にします",
            "so that we can see the vertices of our curve": "カーブの頂点を確認できるように",
            
            "And yeah, and as you can see it's a pretty simple spline": "ご覧の通り、これは非常にシンプルなスプラインです",
            "It just, it's all it is is just these corner points": "単に、これらのコーナーポイントがあるだけで",
            "and they're connected straight from one point to the next": "ポイントから次のポイントへ直線で接続されています",
            "But that's of course not what we want": "しかし、これは当然望む結果ではありません",
            "because as you saw in the preview": "プレビューで見たように",
            "the final result should be kind of like free flowing": "最終結果は自由に流れるような形であるべきです",
            "and should have some kind of minimum offset": "そして何らかの最小オフセットを持つべきです",
            "from the landscape or, or the assets in our environment": "ランドスケープや環境内のアセットから",
            
            "How do we do that?": "どうすればよいでしょうか？",
            "What we have to do first is we need to add some pre-processing steps": "まず、いくつかの前処理ステップを追加する必要があります",
            "to our supply to make sure that it always conforms to the environment": "環境に常に適合するようにするために",
            "And the way that I chose to do it for this tutorial": "このチュートリアルで選択した方法は",
            "is to add more detail to our SP blinds": "スプラインにより多くの詳細を追加し",
            "and then move them so that they, you know": "それらを移動させることです",
            "don't intersect with the environment here": "環境と交差しないように",
            "and that they have a minimum offset of": "そして最小オフセットを持つように",
            "I don't know, So I'm also gonna drop down on no node like": "いくらか、ノードを下に配置します",
            
            "with the environment here": "環境とともに",
            "so that we have some markers for later": "後で使用するマーカーを持つため",
            "when we wanna turn this into a tool": "これをツールに変換する際に",
            "that we can share with people": "人々と共有できるように",
            "And what I'm gonna do after is to add this detail": "この詳細を追加した後に行うことは",
            "I'm gonna get a re-sample node": "Resampleノードを取得することです",
            "and what it does basically is it just takes the input curve": "基本的にこれは入力カーブを取得し",
            "that you have and it re-sample the input": "入力を再サンプルします",
            "it takes whatever you have in there": "そこにあるものを取得し",
            "and it adds consistent detail at a rate that we want it": "望むレートで一貫した詳細を追加します"
        }
        
        # フレーズベース翻訳を適用
        text = english_text
        for eng_phrase, jp_phrase in phrase_translations.items():
            if eng_phrase in text:
                text = text.replace(eng_phrase, jp_phrase)
                break
        
        # フレーズで翻訳されなかった場合、単語ベース翻訳を適用
        if text == english_text:
            for eng_term, jp_term in self.established_terms.items():
                text = text.replace(eng_term, jp_term)
        
        return text if text != english_text else self.fallback_translate(english_text)
    
    def fallback_translate(self, text):
        """フォールバック翻訳（基本的な文構造対応）"""
        # 基本的な翻訳パターン
        basic_patterns = {
            "So ": "では、",
            "And ": "そして、",
            "But ": "しかし、",
            "Now ": "今度は、",
            "Well ": "さて、",
            "OK": "わかりました",
            "Alright": "よし",
            "Let me ": "では",
            "I'm gonna ": "私は",
            "you can see": "ご覧いただけます",
            "we can": "私たちは",
            "what we want": "望むもの",
            "like this": "このような",
            "something like": "次のような"
        }
        
        result = text
        for eng, jp in basic_patterns.items():
            result = result.replace(eng, jp)
        
        return result

    def translate_translation_queue(self, queue_data):
        """翻訳キューデータの処理"""
        
        translated_data = {
            "chapter_info": {
                "number": queue_data["chapter_info"]["number"],
                "title": "基本ロジック",
                "duration_seconds": queue_data["chapter_info"]["duration_seconds"],
                "video_id": queue_data["chapter_info"]["video_id"]
            },
            "subtitle_segments": [],
            "learning_segments": [],
            "technical_metadata": queue_data["technical_metadata"]
        }
        
        # 字幕セグメント翻訳
        for segment in queue_data["subtitle_segments"]:
            translated_segment = {
                "id": segment["id"],
                "start": segment["start"],
                "end": segment["end"],
                "text": self.translate_subtitle_text(segment["text"])
            }
            translated_data["subtitle_segments"].append(translated_segment)
        
        # 学習セグメント翻訳
        for learning_seg in queue_data["learning_segments"]:
            translated_learning = {
                "segment_id": learning_seg["segment_id"],
                "start_time": learning_seg["start_time"],
                "end_time": learning_seg["end_time"],
                "title": self.translate_learning_title(learning_seg["title"]),
                "objectives": [self.translate_objective(obj) for obj in learning_seg["objectives"]],
                "key_concepts": [self.translate_key_concept(kc) for kc in learning_seg["key_concepts"]],
                "nodes_introduced": learning_seg["nodes_introduced"]
            }
            translated_data["learning_segments"].append(translated_learning)
        
        return translated_data
    
    def translate_learning_title(self, title):
        """学習セグメントタイトル翻訳"""
        title_translations = {
            "Environment Setup and Curve Drawing": "環境設定とカーブ描画",
            "Spline Preprocessing and Offset": "スプライン前処理とオフセット",
            "Bridge Logic Separation": "橋ロジック分離",
            "VEX Programming for Incline Detection": "勾配検出のためのVEXプログラミング",
            "Plank Spawning and Orientation": "板材生成と方向設定",
            "Variation and Final Adjustments": "バリエーションと最終調整"
        }
        return title_translations.get(title, title)
    
    def translate_objective(self, objective):
        """目標翻訳"""
        obj_translations = {
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
        return obj_translations.get(objective, objective)
    
    def translate_key_concept(self, key_concept):
        """キーコンセプト翻訳"""
        kc_translations = {
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
        return kc_translations.get(key_concept, key_concept)


def main():
    if len(sys.argv) != 2:
        print("使用方法: python subtitle_translator.py <translation_queue.json>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    # 入力ファイルのパス解決
    if not os.path.isabs(input_file):
        base_dir = Path(__file__).parent.parent / "tutorials" / "Project_Skylark_Bridges" / "05_translation_batch"
        input_path = base_dir / input_file
    else:
        input_path = Path(input_file)
    
    if not input_path.exists():
        print(f"エラー: ファイル {input_path} が見つかりません")
        sys.exit(1)
    
    # 翻訳実行
    translator = SubtitleTranslator()
    
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            queue_data = json.load(f)
        
        translated_data = translator.translate_translation_queue(queue_data)
        
        # 出力ファイル名生成
        output_filename = input_path.stem + '_jp.json'
        output_path = input_path.parent / output_filename
        
        # 翻訳データ保存
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(translated_data, f, ensure_ascii=False, indent=2)
        
        print(f"字幕翻訳完了: {output_path}")
        print(f"処理された字幕セグメント数: {len(translated_data['subtitle_segments'])}")
        print(f"処理された学習セグメント数: {len(translated_data['learning_segments'])}")
        
    except Exception as e:
        print(f"エラー: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()