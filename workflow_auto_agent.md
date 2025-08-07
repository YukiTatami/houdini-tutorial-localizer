# Vimeo動画翻訳ワークフロー - ファイル操作可能AIエージェント用

## 🤖 AIエージェントが把握すべき前提（必須）
このファイルはAIエージェントが理解しやすい形式で書かれています。編集する場合はこのルールを守る必要があります。

## 🤖 AIエージェント実行指示

**対象**: Write/Edit/Read/LS toolが使用可能なAIエージェント

### 🎯 ワークフロー概要
Houdiniチュートリアルシリーズ（複数動画・Vimeo埋め込み）から日本語学習支援資料を自動作成

**成果物**:
- 各チャプター用日本語翻訳字幕（SRT形式）
- チャプター別動画同期型学習ガイド（MD + HTML形式、初出ノード詳細解説付き）

**所要時間**: 1チャプターあたり約15分（2段階翻訳による安全性向上）

**ワークフローの特徴**:
- 🚀 **英語優先処理**: AIの英語理解力を最大活用
- 📦 **2段階翻訳**: 構造化データ翻訳による高品質・安全性確保
- ⚡ **効率的処理**: 重複処理の排除・段階的品質管理

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
📽️ 複数動画シリーズ → 📚 体系的日本語学習資料の自動生成

成果物:
✅ 各チャプター日本語翻訳字幕（SRT形式）
✅ チャプター別動画同期型学習ガイド（MD + HTML形式、初出ノード詳細解説付き）

所要時間: 1チャプターあたり約12分
```

**🔄 処理の流れ**:
```
STEP 1: 環境準備（シリーズ全体フォルダ構造自動作成）
STEP 2: チャプター選択・字幕取得準備
STEP 3: JavaScript字幕取得（英語）
STEP 4: 英語ベース包括分析・構造化データ準備
STEP 5: 2段階翻訳実行（構造化データ翻訳 + 日本語ガイド生成）
STEP 6: 日本語版統合・HTML生成
STEP 7: 次チャプター処理（STEP 2に戻る）
```

**⚠️ ユーザー作業が必要な箇所**:
- STEP 1: 各動画URL等の情報提供
- STEP 3: 各チャプターでブラウザJavaScript実行（字幕取得）
- STEP 7: 次チャプター処理継続の意思確認

#### 0-3: 自動状態診断
1. **LS tool**で現在フォルダスキャン
2. **自動判定**:
   ```
   ├── SRTファイル存在確認 → 進捗推定
   └── 何も存在しない → 新規開始
   ```

### STEP 1: 環境準備

#### 1-1: シリーズ情報収集
ユーザーに以下のみを確認：
- チュートリアルURL（シリーズページ）

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
├── 02_english_analysis/          # 英語分析専用
│   ├── chapter_01_analysis.json
│   ├── chapter_01_guide_en.md
│   └── ... (チャプター数分)
├── 03_learning_guide/            # 日本語版学習ガイド
│   └── chapters/
├── 04_progress/                  # 進捗管理
│   └── progress_tracker.json
└── 05_translation_batch/         # 翻訳用一時データ
    └── translation_queue.json
```

**1-3-2. 進捗管理ファイル作成**
- file_path: "tutorials/[シリーズ名]/04_progress/progress_tracker.json"
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
10. プレースホルダーファイル（transcript_placeholder_intro_en.srt）を直接開き、内容を削除してSRTデータを貼り付け
11. ⚠️ 重要: ファイルをUTF-8エンコーディングで保存（文字化け防止）
12. 「SRTファイル保存完了」と報告

#### 3-3: 英語SRTデータの品質チェック
```
**Python品質修正スクリプト使用（推奨）**:
- Bash tool でsrt_quality_fixer.pyを実行：
  python srt_quality_fixer.py "tutorials/[シリーズ名]/01_raw_data/chapter_{章番号}_{チャプター名}/transcript_{videoId}_{title}_en.srt" "tutorials/[シリーズ名]/01_raw_data/chapter_{章番号}_{チャプター名}/transcript_{videoId}_{title}_en_fixed.srt"
- 30秒セグメント化と文末統一が自動で実行される
```

#### 3-4: 進捗管理更新
```
Edit tool で進捗ファイル更新：
- file_path: "tutorials/[シリーズ名]/04_progress/progress_tracker.json"
- 該当チャプターの字幕取得ステータスを"completed"に更新
```

### STEP 4: 英語ベース包括分析・学習ガイド作成

#### 4-1: 英語字幕読み込み
```
Read tool で以下を実行：
- file_path: "tutorials/[シリーズ名]/01_raw_data/chapter_{章番号}_{チャプター名}/transcript_{videoId}_{title}_en_fixed.srt"
```

#### 4-2: 英語ベース包括分析実行
```
共通情報ファイルの「英語包括分析プロンプト」を使用
- Houdiniノード抽出 & 初出タイムスタンプ特定（英語）
- 技術的文脈の深い理解と分析（英語）
- シリーズ全体でのノード関連性マッピング（英語）
- チャプター学習目標・前提条件の明確化（英語）

出力: 構造化JSON形式で分析結果を保存
```

#### 4-3: 分析結果保存
```
Write tool で以下を実行：
- file_path: "tutorials/[シリーズ名]/02_english_analysis/chapter_{章番号}_{チャプター名}_analysis.json"
- content: 構造化された英語分析データ（JSON形式）
```

#### 4-4: 翻訳用データ準備
```
翻訳効率化のため、英語分析結果から構造化データを作成：
- 字幕セグメント一覧（英語）
- 学習セグメント詳細（英語）
- ノード解説データ（英語）
- メタデータ・専門用語集（英語）
- 文脈情報・タイムスタンプ情報

Write tool で保存：
- file_path: "tutorials/[シリーズ名]/05_translation_batch/chapter_{章番号}_translation_queue.json"

⚠️ 注意: guide_en.mdは作成しません（2段階翻訳フローでは不要）
```

#### 4-5: 進捗管理更新
```
Edit tool で進捗ファイル更新：
- file_path: "tutorials/[シリーズ名]/04_progress/progress_tracker.json"
- 英語分析ステータスを"completed"に更新
```

### STEP 5: 2段階翻訳実行

#### 5-1: 第1段階翻訳（analysis.json翻訳）
```
Read tool で以下を実行：
- file_path: "tutorials/[シリーズ名]/02_english_analysis/chapter_{章番号}_analysis.json"

共通情報ファイルの「第1段階翻訳プロンプト」を使用
- analysis.json構造化データ翻訳
- Houdiniノード情報・技術概念の翻訳
- 専門用語一貫性確保

Write tool で保存：
- file_path: "tutorials/[シリーズ名]/05_translation_batch/chapter_{章番号}_analysis_jp.json"

Edit tool で進捗更新：
- file_path: "tutorials/[シリーズ名]/04_progress/progress_tracker.json"
- analysis_translation: "completed"
```

#### 5-2: 第2段階翻訳（translation_queue.json翻訳）
```
Read tool で以下を実行：
- file_path: "tutorials/[シリーズ名]/05_translation_batch/chapter_{章番号}_translation_queue.json"

共通情報ファイルの「第2段階翻訳プロンプト」を使用
- translation_queue.json構造化データ翻訳
- SRT字幕データ・学習セグメント翻訳
- 文脈保持による高品質翻訳

Write tool で保存：
- file_path: "tutorials/[シリーズ名]/05_translation_batch/chapter_{章番号}_translation_queue_jp.json"
- file_path: "tutorials/[シリーズ名]/01_raw_data/chapter_{章番号}_{チャプター名}/transcript_{videoId}_{title}_jp.srt"

Edit tool で進捗更新：
- file_path: "tutorials/[シリーズ名]/04_progress/progress_tracker.json"
- queue_translation: "completed"
```

#### 5-3: 第3段階（日本語学習ガイド生成）
```
Read tool で翻訳済みデータ読み込み：
- file_path: "tutorials/[シリーズ名]/05_translation_batch/chapter_{章番号}_analysis_jp.json"
- file_path: "tutorials/[シリーズ名]/05_translation_batch/chapter_{章番号}_translation_queue_jp.json"
- file_path: "tutorials/[シリーズ名]/01_raw_data/chapter_{章番号}_{チャプター名}/transcript_{videoId}_{title}_jp.srt"

共通情報ファイルの「日本語ガイド生成プロンプト」を使用
- 翻訳済み構造化データから日本語学習ガイド完全版作成
- タイムスタンプ付き完全カバレッジ
- 初出ノード詳細解説付き
- 自然な日本語技術文書スタイル

Write tool で保存：
- file_path: "tutorials/[シリーズ名]/03_learning_guide/chapters/chapter_{章番号}_{チャプター名}_学習ガイド.md"

Edit tool で進捗更新：
- file_path: "tutorials/[シリーズ名]/04_progress/progress_tracker.json"
- japanese_guide_generation: "completed"
```

### STEP 6: 日本語版統合・HTML生成

#### 6-1: 日本語学習ガイド(MD)読み込み
```
Read tool で以下を実行：
- file_path: "tutorials/[シリーズ名]/03_learning_guide/chapters/chapter_{章番号}_{チャプター名}_学習ガイド.md"
```

#### 6-2: HTML変換実行
```
**Python変換スクリプト使用**:
- Bash tool でmd_to_html_converter.pyを実行：
  python md_to_html_converter.py "tutorials/[シリーズ名]/03_learning_guide/chapters/chapter_{章番号}_{チャプター名}_学習ガイド.md"
- 自動でHTMLファイルが生成される
- 全セクション一括処理、高速・高品質な出力
```

#### 6-3: 一時ファイルクリーンアップ
```
翻訳用一時ファイルの整理:
- tutorials/[シリーズ名]/05_translation_batch/ フォルダ内の翻訳済みファイル（*_jp.json）削除
- tutorials/[シリーズ名]/02_english_analysis/ フォルダ内：
  - analysis.json は保持（シリーズ参照用）
  - guide_en.md は削除（2段階翻訳フローでは不要）

⚠️ 注意: 既存のguide_en.mdファイルがある場合は削除推奨
```

#### 6-4: 進捗管理最終更新
```
Edit tool で進捗ファイル更新：
- file_path: "tutorials/[シリーズ名]/04_progress/progress_tracker.json"
- 学習ガイド(HTML版)生成ステータスを"completed"に更新
- チャプター全体完了ステータスを"completed"に更新
- 英語ノード情報とシリーズ用語集を更新
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
2. **英語優先処理**: STEP 4まで英語で処理し、STEP 5で一括翻訳
3. **ユーザー連携**: STEP 3は必ずユーザー実行が必要
4. **エラー対応**: 問題発生時は進捗ファイルで状態確認後、適切なステップから再開
5. **品質管理**: 各ステップ完了時に必ず進捗更新とファイル保存確認

## 📂 参照ファイル

- **共通情報**: `workflow_common_resources.md`
  - 英語分析プロンプト
  - 一括翻訳プロンプト
  - JavaScriptコード
  - フォルダ構造・命名規則
  - トラブルシューティング

## 🚀 ワークフロー効果

- **処理時間**: 1チャプターあたり約12分
- **翻訳品質**: 文脈保持による一貫性確保
- **専門性**: 英語での深い技術分析
- **保守性**: 構造化データによる管理