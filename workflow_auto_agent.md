# Vimeo動画翻訳ワークフロー - ファイル操作可能AIエージェント用

## 🤖 AIエージェントが把握すべき前提（必須）
このファイルはAIエージェントが理解しやすい形式で書かれています。編集する場合はこのルールを守る必要があります。

## 🤖 AIエージェント実行指示

**対象**: Write/Edit/Read/LS toolが使用可能なAIエージェント

### 🎯 ワークフロー概要
Houdiniチュートリアルシリーズ（複数動画・Vimeo埋め込み）からシンプルな日本語学習資料を自動作成

**成果物**:
- 各チャプター用日本語翻訳字幕（SRT形式）
- チャプター別動画同期型学習ガイド（MD + HTML形式、ノード名 + 日本語公式ドキュメントリンク付き）

**所要時間**: 1チャプターあたり約8-10分

**ワークフローの特徴**:
- 🚀 **処理フロー**: ノード抽出 + 翻訳 + Python機械処理のみ
- 📦 **Python自動化**: markdown_generator.pyによる完全機械化
- ⚡ **高速処理**: ストリームライン化された処理

### STEP 0: 初期診断・ワークフロー開始

#### 0-1: エージェント能力確認
```
必要ツール: Write, Edit, LS, Read
確認結果: AUTO（自動実行可能）
```

#### 0-2: ワークフロー概要説明
ユーザーに以下の概要を説明：

**🎯 このワークフローで実現すること**:
```
📽️ 複数動画シリーズ → 📚 シンプルな日本語学習資料の自動生成

成果物:
✅ 各チャプター日本語翻訳字幕（SRT形式）
✅ チャプター別動画同期型学習ガイド（MD + HTML形式、ノード名 + 日本語公式ドキュメントリンク付き）

所要時間: 1チャプターあたり約8-10分
```

**🔄 処理の流れ**:
```
STEP 1: 環境準備（シリーズ全体フォルダ構造自動作成）
STEP 2: チャプター選択・字幕取得準備
STEP 3: JavaScript字幕取得（英語）
STEP 4: 英語ノード分析（簡素化）
STEP 5: 翻訳・ノード情報生成
STEP 6: Python機械処理・マークダウン生成・HTML変換
STEP 7: 次チャプター処理（STEP 2に戻る）
```

**⚠️ ユーザー作業が必要な箇所**:
- STEP 1: チュートリアルURLの情報提供
- STEP 2: 各チャプターでブラウザJavaScript実行（字幕取得）
- STEP 3: 次チャプター処理継続の意思確認

#### 0-3: 自動状態診断
1. **LS tool**で現在フォルダスキャン
2. **自動判定**:
   ```
   ├── SRTファイル存在確認 → 進捗推定
   └── 何も存在しない → 新規開始
   ```

### STEP 1: 環境準備

#### 1-1: シリーズ情報収集
1. ユーザーにチュートリアルURL（シリーズページ）の情報提供を依頼
2. AIエージェントがURLにアクセスし、注意して以下を確認：
   - シリーズ全体のタイトル
   - 全チャプターのタイトルと番号
   - チャプター数の合計

#### 1-2: LS tool実行
```
パラメータ: {"path": "tutorials/ディレクトリの絶対パス"}
目的: tutorials/内の既存シリーズフォルダの有無確認
```

#### 1-3: Write tool実行（並列可能）

**1-3-1. シリーズフォルダ構造作成**
```
tutorials/[シリーズ名]/
├── 01_raw_data/
│   ├── chapter_01_[チャプター名]/
│   ├── chapter_02_[チャプター名]/
│   └── ... (チャプター数分)
├── 02_analysis_data/             # 分析・ノードデータ
│   ├── chapter_01_analysis.json
│   ├── chapter_01_node_insertions.json
│   └── ... (チャプター数分)
├── 03_learning_guide/            # 日本語版学習ガイド
│   └── chapters/
└── progress_tracker.json         # 進捗管理ファイル（シリーズ直下）
```

**1-3-2. 進捗管理ファイル作成**
- file_path: "tutorials/[シリーズ名]/progress_tracker.json"
- content: チャプター進捗管理データ（JSON形式）

#### 1-4: Read tool で作成確認

### STEP 2: チャプター選択・字幕取得準備

#### 2-1: 処理チャプター選択
進捗管理ファイルを確認し、ユーザーに選択肢を提示：
1. 次の未処理チャプターを自動選択
2. 特定チャプターを指定

#### 2-2: 選択チャプターの前提条件確認
ユーザーに以下を確認：
1. 英語字幕の存在確認
2. 動画再生・一時停止の動作確認
3. 開発者ツール（F12）の利用可能性

### STEP 3: JavaScript字幕取得実行

**⚠️ 重要**: ユーザーがブラウザで実行する作業

#### 3-1: チャプター字幕ファイル保存準備
次のファイルが存在するか確認し、なければ空の状態で作成しユーザーに告知
file_path: "tutorials/[シリーズ名]/01_raw_data/chapter_{章番号}_{チャプター名}/transcript_{videoId}_{title}_en.srt"

#### 3-2: ユーザー実行指示
以下の手順をユーザーに指示：
1. 動画ページで字幕を有効化 → 一度再生 → 一時停止
2. F12 → Console を開く
3. プロジェクトフォルダ内の `scripts/vimeo_subtitle_extractor_step1.js` をテキストエディタで開く
4. ファイル内容を全選択してコピー（Ctrl+A → Ctrl+C）
5. ブラウザのConsoleにペーストして実行（Ctrl+V → Enter）
6. プロジェクトフォルダ内の `scripts/vimeo_subtitle_extractor_step2.js` をテキストエディタで開く
7. ファイル内容を全選択してコピー（Ctrl+A → Ctrl+C）
8. ブラウザのConsoleにペーストして実行（Ctrl+V → Enter）
9. Console出力の「===== COPY THE TEXT BELOW =====」以下のSRTデータを手動選択・コピー
10. プレースホルダーファイル（`tutorials/[シリーズ名]/01_raw_data/chapter_{章番号}_{チャプター名}/transcript_placeholder_{チャプター名}_en.srt`）を直接開き、内容を削除してSRTデータを貼り付け
11. ⚠️ 重要: ファイルをUTF-8エンコーディングで保存（文字化け防止）
12. 「SRTファイル保存完了」と報告

#### 3-3: 英語SRTデータの品質修正
```
**必須-Python品質修正スクリプト使用(ファイル読み込み不要)**:
- Bash tool でsrt_quality_fixer.pyを実行：
  python scripts/srt_quality_fixer.py "tutorials/[シリーズ名]/01_raw_data/chapter_{章番号}_{チャプター名}/transcript_{videoId}_{title}_en.srt" "tutorials/[シリーズ名]/01_raw_data/chapter_{章番号}_{チャプター名}/transcript_{videoId}_{title}_en_fixed.srt"
- 30秒セグメント化と文末統一が自動で実行される
```

#### 3-4: 進捗管理更新
```
Edit tool で進捗ファイル更新：
- file_path: "tutorials/[シリーズ名]/progress_tracker.json"
- "subtitle_extraction": "completed" に更新
```

### STEP 4: 英語ノード分析（簡素化）

#### 4-1: 英語字幕読み込み
```
Read tool で以下を実行：
- file_path: "tutorials/[シリーズ名]/01_raw_data/chapter_{章番号}_{チャプター名}/transcript_{videoId}_{title}_en_fixed.srt"
```

#### 4-2: 英語ノード分析実行
```
共通情報ファイルの「英語分析プロンプト（簡素化版）」を使用
- Houdiniノード名の抽出
- 各ノードの言及タイムスタンプ記録
- 日本語公式ドキュメントリンク生成

出力: 基本ノード情報のJSON形式で保存
```

#### 4-3: 分析結果保存
```
Write tool で以下を実行：
- file_path: "tutorials/[シリーズ名]/02_analysis_data/chapter_{章番号}_analysis.json"
- content: ノード情報のJSONデータ
```

#### 4-4: 進捗管理更新
```
Edit tool で進捗ファイル更新：
- file_path: "tutorials/[シリーズ名]/progress_tracker.json"
- "english_analysis": "completed" に更新
```

### STEP 5: 翻訳・ノード情報生成

#### 5-1: 英語分析データ読み込み
```
Read tool で以下を実行：
- file_path: "tutorials/[シリーズ名]/02_analysis_data/chapter_{章番号}_analysis.json"
- file_path: "tutorials/[シリーズ名]/01_raw_data/chapter_{章番号}_{チャプター名}/transcript_{videoId}_{title}_en_fixed.srt"
```

#### 5-2: 翻訳・ノード情報生成実行
```
共通情報ファイルの「翻訳・ノード情報生成プロンプト」を使用
- 英語字幕の日本語翻訳
- タイムスタンプとシーケンス番号の維持
- ノード名の英語保持（例: "Box SOP"）
- ノード挿入指示データ生成

出力構造:
{
  "subtitle_translation": "[日本語SRTフォーマットデータ]",
  "node_insertions": [
    {
      "node_name": "Box SOP",
      "doc_link_ja": "https://docs.sidefx.com/vex/lang/ja/sop/box",
      "insert_after_timestamp": "00:02:15"
    }
  ]
}
```

#### 5-3: 出力ファイル保存
```
Write tool で以下を保存：
- file_path: "tutorials/[シリーズ名]/01_raw_data/chapter_{章番号}_{チャプター名}/transcript_{videoId}_{title}_jp.srt"
  content: 日本語翻訳字幕
- file_path: "tutorials/[シリーズ名]/02_analysis_data/chapter_{章番号}_node_insertions.json"
  content: ノード挿入指示データ
```

#### 5-4: 進捗管理更新
```
Edit tool で進捗ファイル更新：
- file_path: "tutorials/[シリーズ名]/progress_tracker.json"
- translation: "completed"
```

### STEP 6: Python機械処理・マークダウン生成

#### 6-1: 入力ファイル確認
```
以下のファイルの存在を確認：
- 日本語字幕: "tutorials/[シリーズ名]/01_raw_data/chapter_{章番号}_{チャプター名}/transcript_{videoId}_{title}_jp.srt"
- ノード挿入データ: "tutorials/[シリーズ名]/02_analysis_data/chapter_{章番号}_node_insertions.json"
```

#### 6-2: Python機械処理実行
```
**markdown_generator.pyを使用した自動マークダウン生成**:

Bash tool で以下を実行：
python scripts/markdown_generator.py \
  --subtitle-file "tutorials/[シリーズ名]/01_raw_data/chapter_{章番号}_{チャプター名}/transcript_{videoId}_{title}_jp.srt" \
  --node-data "tutorials/[シリーズ名]/02_analysis_data/chapter_{章番号}_node_insertions.json" \
  --output "tutorials/[シリーズ名]/03_learning_guide/chapters/chapter_{章番号}_{チャプター名}_学習ガイド.md"

**機能**:
- 字幕データとノードデータの自動統合
- タイムスタンプマッチング自動化
- マークダウン形式自動生成
- ノードリンク自動挿入

**出力形式**:
```markdown
## 00:02:15
「ここでBox SOPを使用してプレースホルダーを作成します」

📝 **Box SOP** - [日本語公式ドキュメント](https://docs.sidefx.com/vex/lang/ja/sop/box)
```
```

#### 6-3: HTML変換実行
```
**Python変換スクリプト使用**:
Bash tool でmd_to_html_converter.pyを実行：
python scripts/md_to_html_converter.py "tutorials/[シリーズ名]/03_learning_guide/chapters/chapter_{章番号}_{チャプター名}_学習ガイド.md"

- 自動でHTMLファイルが生成される
- 日本語レイアウト最適化
- シンプルな出力
```

#### 6-4: 進捗管理最終更新
```
Edit tool で進捗ファイル更新：
- file_path: "tutorials/[シリーズ名]/progress_tracker.json"
- "markdown_generation": "completed" に更新
- "html_conversion": "completed" に更新
- "nodes_encountered": [チャプターで遇遇したノードリスト] に更新
- "series_nodes_list": [シリーズ全体のノードリスト] に更新
- チャプター全体完了ステータスを"completed"に更新
```

### STEP 7: 次チャプター処理・完了判定

#### 7-1: 処理継続確認
進捗ファイルを確認し、ユーザーに選択肢を提示：
1. 次チャプターの処理を継続（STEP 2に戻る）
2. 処理を一時停止
3. シリーズ完了処理

#### 7-2: シリーズ完了時の最終処理
```
全チャプター完了時：
- 進捗ファイルの完了ステータス更新
- 全チャプター学習ガイドの品質チェック
- シリーズサマリー作成（オプション）
- 最終ファイル構造確認
```

#### 7-3: エラー処理・回復手順
各ステップで問題が発生した場合：
1. 進捗ファイルで現在状態を確認
2. 失敗したステップから再開
3. 必要に応じてバックアップファイルから復旧
4. 共通情報ファイルのトラブルシューティングを参照

## 📋 実行時の注意事項

1. **共通情報参照**: プロンプト、コード等は workflow_common_resources.md を参照
2. **処理フロー**: STEP 4でノード抽出、STEP 5で翻訳、STEP 6でPython機械処理
3. **ユーザー連携**: STEP 3は必ずユーザー実行が必要
4. **エラー対応**: 問題発生時は進捗ファイルで状態確認後、適切なステップから再開
5. **品質管理**: 各ステップ完了時に必ず進捗更新とファイル保存確認

## 📂 参照ファイル

- **共通情報**: `workflow_common_resources.md`
  - 英語分析プロンプト
  - 翻訳・ノード情報生成プロンプト
  - JavaScriptコード
  - フォルダ構造・命名規則
  - Python自動化ツール
  - トラブルシューティング

## 🚀 ワークフロー効果

- **処理時間**: 1チャプターあたり約8-10分
- **処理範囲**: ノード名 + 日本語公式ドキュメントリンク
- **自動化**: Pythonスクリプトによる自動化
- **保守性**: シンプルなファイル構造と管理