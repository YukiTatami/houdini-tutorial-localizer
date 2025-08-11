# Vimeo動画翻訳ワークフロー - 共通リソース

## 🤖 AIエージェントが把握すべき前提（必須）
このファイルはAIエージェントが理解しやすい形式で書かれています。編集する場合はこのルールを守る必要があります。

## 🗂️ 1. プロジェクト仕様

### 📁 フォルダ構造
```
tutorials/[SeriesName]/
├── 01_raw_data/                       # 生データ（チャプター別）
│   ├── chapter_01_introduction/
│   │   ├── transcript_{videoId}_{title}_en.srt      # 英語字幕（原本）
│   │   ├── transcript_{videoId}_{title}_en_fixed.srt # 品質修正版
│   │   └── transcript_{videoId}_{title}_jp.srt      # 翻訳字幕（最終版）
│   ├── chapter_02_basic_logic/
│   │   ├── transcript_{videoId}_{title}_en.srt
│   │   ├── transcript_{videoId}_{title}_en_fixed.srt
│   │   └── transcript_{videoId}_{title}_jp.srt
│   └── ... (チャプター数分)
├── 02_analysis_data/                  # 分析・ノードデータ
│   ├── chapter_01_analysis.json      # 基本分析データ
│   ├── chapter_01_node_insertions.json # ノード挿入指示
│   ├── chapter_02_analysis.json
│   ├── chapter_02_node_insertions.json
│   └── ... (チャプター数分)
├── 03_learning_guide/                 # 日本語版学習資料
│   └── chapters/                      # チャプター別ガイド
│       ├── chapter_01_introduction_学習ガイド.md
│       ├── chapter_01_introduction_学習ガイド.html
│       ├── chapter_02_basic_logic_学習ガイド.md
│       ├── chapter_02_basic_logic_学習ガイド.html
│       └── ... (チャプター数分、MD + HTML)
└── progress_tracker.json              # シリーズ進捗ファイル（シリーズ直下）
```

### 📝 命名規則

**変数フォーマット定義**:
- `{章番号}`: 01, 02, 03... の2桁ゼロ埋め
- `{チャプター名}`: 英語小文字、単語はアンダースコア区切り (例: introduction, basic_logic)
- `{シリーズ名}`: アンダースコア区切り (例: Project_Skylark_Bridges)

| ファイル種類 | 命名パターン | 例 |
|------------|-------------|---|
| チャプターフォルダ | `chapter_{章番号}_{チャプター名}/` | `chapter_01_introduction/` |
| 英語字幕（原本） | `transcript_{videoId}_{title}_en.srt` | `transcript_1096045116_intro_en.srt` |
| 英語字幕（修正版） | `transcript_{videoId}_{title}_en_fixed.srt` | `transcript_1096045116_intro_en_fixed.srt` |
| 翻訳字幕 | `transcript_{videoId}_{title}_jp.srt` | `transcript_1096045116_intro_jp.srt` |
| 基本分析データ | `chapter_{章番号}_analysis.json` | `chapter_01_analysis.json` |
| ノード挿入指示 | `chapter_{章番号}_node_insertions.json` | `chapter_01_node_insertions.json` |
| 日本語学習ガイド(MD) | `chapter_{章番号}_{チャプター名}_学習ガイド.md` | `chapter_01_introduction_学習ガイド.md` |
| 日本語学習ガイド(HTML) | `chapter_{章番号}_{チャプター名}_学習ガイド.html` | `chapter_01_introduction_学習ガイド.html` |
| 進捗管理ファイル | `progress_tracker.json` | `progress_tracker.json`（シリーズ直下） |

### 📄 進捗管理ファイル構造
```json
{
  "series_info": {
    "name": "Project_Skylark_Bridges",
    "total_chapters": 6,
    "workflow_version": "3.0"
  },
  "chapters": [
    {
      "chapter_number": "01",
      "chapter_name": "introduction",
      "title": "導入",
      "status": {
        "subtitle_extraction": "completed",
        "english_analysis": "completed", 
        "translation": "completed",
        "markdown_generation": "completed",
        "html_conversion": "completed"
      },
      "nodes_encountered": ["Box SOP", "Add SOP", "Merge SOP"]
    },
    {
      "chapter_number": "02",
      "chapter_name": "basic_logic",
      "title": "基本ロジック",
      "status": {
        "subtitle_extraction": "pending",
        "english_analysis": "pending",
        "translation": "pending",
        "markdown_generation": "pending",
        "html_conversion": "pending"
      },
      "nodes_encountered": []
    }
  ],
  "series_nodes_list": ["Box SOP", "Add SOP", "Merge SOP"]
}
```

## 💻 2. JavaScript字幕取得コード

### 🔧 実行環境要件
| 項目 | 要件 | 詳細 |
|------|------|------|
| 対象ページ | Vimeo埋め込みページ | ✅ SideFXチュートリアル / ❌ 直接VimeoURL |
| 事前準備 | 字幕有効化 + 再生 | API初期化のため一度再生→停止 |
| 実行環境 | ブラウザ開発者ツール | F12 → Console |

### 📜 実行コード

#### ステップ1: Player初期化・字幕収集
**実行手順**：
1. Vimeo埋め込みページで開発者ツール（F12）を開く
2. Consoleタブに移動
3. プロジェクトフォルダ内の `scripts/vimeo_subtitle_extractor_step1.js` を開く
4. ファイル内容を全選択してコピー（Ctrl+A → Ctrl+C）
5. ブラウザのConsoleにペーストして実行（Ctrl+V → Enter）

#### ステップ2: SRT形式変換
**実行手順**：
1. ステップ1の実行完了を確認
2. プロジェクトフォルダ内の `scripts/vimeo_subtitle_extractor_step2.js` を開く
3. ファイル内容を全選択してコピー（Ctrl+A → Ctrl+C）
4. ブラウザのConsoleにペーストして実行（Ctrl+V → Enter）
5. Console出力の「===== COPY THE TEXT BELOW =====」以下のSRTデータをコピー

## 📝 3. AIプロンプトテンプレート

### 📌 重要な設計原則

**シリーズ一貫性の確保**:
- 各プロンプトでseries_glossary.jsonを参照し、専門用語の一貫性を維持
- progress_tracker.jsonでシリーズ全体の進捗と既出ノードを管理
- ノード初出判定は"series_first_appearance"フラグで厳密に管理

**品質保証のための要件**:
- 全タイムスタンプセグメントの完全カバレッジ（欠落なし）
- 技術用語の正確性とシリーズ間一貫性の維持
- 学習目標と内容の論理的整合性の確保

**データフロー**:
1. 英語分析 → analysis.json（シリーズ継続性データ含む）
2. 第1段階翻訳 → analysis_jp.json + 用語集更新
3. 第2段階翻訳 → translation_queue_jp.json + 日本語字幕
4. 日本語ガイド生成 → 全データ統合による完全版ガイド


### 🔍 英語分析プロンプト
```
Analyze this English Houdini tutorial subtitle for basic node identification.

Analysis Requirements:
1. **Houdini Node Identification**:
   - Extract all Houdini node names mentioned in subtitles
   - Record the timestamp where each node is mentioned
   - Generate Japanese official documentation links

Output Format (JSON):
{
  "houdini_nodes": [
    {
      "node_name": "Box SOP",
      "mention_timestamps": ["00:02:15", "00:05:30"]
    },
    {
      "node_name": "Merge SOP",
      "mention_timestamps": ["00:02:45"]
    }
  ]
}

[SRT subtitle content here]
```

### 📚 英語学習ガイド生成プロンプト
```
Create a comprehensive English learning guide for this Houdini tutorial chapter using the provided analysis data and subtitles.

Input Data:
- Analysis JSON: [分析結果JSON - includes series continuity data]
- English Subtitles: [英語字幕データ]
- Series Node History: [既出ノードリスト from previous chapters]
- Chapter Number: [章番号]
- Total Chapters: [総チャプター数]

Requirements:
1. **Complete Timestamp Coverage**: Include all subtitle segments, no omissions
2. **Technical Accuracy**: Maintain precise Houdini terminology
3. **Learning Structure**: Organize by logical learning progression based on analysis segments
4. **Node Documentation**: 
   - Include detailed explanations ONLY for nodes NOT present in previously identified nodes list from progress_tracker.json
   - For previously introduced nodes, do not add any node documentation
5. **Cross-references**: 
   - Link to related concepts from previous chapters
   - Note when building upon earlier material
   - Include "See Chapter X" references where appropriate
6. **Selective Commentary**: 
   - Add explanations only when subtitle content requires clarification
   - Skip redundant commentary for self-explanatory sections
   - Focus on technical insights that enhance understanding

Guide Structure:
# [Series Name] - Chapter {number}: [Chapter Title] Learning Guide (English)

**Series Information**:
- Series: [Series Name]
- Chapter: {number} / {total chapters}
- Video URL: [URL](URL)
- Duration: [duration]
- Prerequisites: [List chapters that should be completed first]

**Overview**:
[Concise chapter overview from analysis data, 2-3 sentences]

**New Concepts & Nodes**:
[List new nodes introduced in this chapter]
[List key concepts building on previous chapters]

---

## [timestamp]
"[Subtitle text]"

[For series-first appearance nodes only:]
📝 **[Node Name] [Node Type]** *(First appearance in series)*
- **Documentation**: [Official docs link]
- **Function**: [Node function description]
- **Key Parameters**: [Important parameters]
- **Common Use Cases**: [Typical scenarios]
- **Beginner Tips**: [Important notes for beginners]

[For previously introduced nodes: No additional documentation needed]

[Continue for all segments...]

Important Guidelines:
- Check progress_tracker.json series_glossary.houdini_nodes list before adding node documentation
- Reference learning_segments from analysis for structure
- Maintain continuity with previous chapters using series_continuity data
- Only document nodes on their FIRST appearance in the entire series
- Keep explanations concise and practical

Generate the complete guide covering all subtitle segments with appropriate technical commentary.

[Provide analysis JSON and subtitle data]
```

### 🔄 翻訳・ノード情報生成プロンプト
```
Translate English subtitles to Japanese and generate node insertion data.

Input Data:
- English Analysis JSON: [analysis.json内容]
- English Subtitles SRT: [英語字幕データ]

Requirements:
1. **Subtitle Translation**:
   - Translate all subtitle segments to natural Japanese
   - Maintain precise timing and sequence numbers
   - Preserve technical node names in English (e.g., "Box SOP")

2. **Node Insertion Data Generation**:
   - For each node mentioned in subtitles, create insertion instruction
   - Generate Japanese official documentation links in format: https://www.sidefx.com/ja/docs/houdini/nodes/{type}/{nodename}.html
   - Specify exact timestamp for insertion

Output Structure:
{
  "subtitle_translation": "[Complete SRT format with Japanese text]",
  "node_insertions": [
    {
      "node_name": "Box SOP",
      "doc_link_ja": "https://www.sidefx.com/ja/docs/houdini/nodes/sop/box.html",
      "insert_after_timestamp": "00:02:15"
    }
  ]
}

[Provide analysis.json and English SRT content]
```

### 🐍 Python機械処理（マークダウン生成）
```bash
# markdown_generator.py 使用方法
python scripts/markdown_generator.py \
  --subtitle-file "tutorials/[Series]/01_raw_data/chapter_01/transcript_jp.srt" \
  --node-data "tutorials/[Series]/02_analysis_data/chapter_01_node_insertions.json" \
  --output "tutorials/[Series]/03_learning_guide/chapters/chapter_01_学習ガイド.md"
```

**機能**:
- 字幕ファイルとノードデータの統合
- タイムスタンプマッチング自動化
- マークダウン形式自動生成
- ノードリンク自動挿入


### ✂️ 字幕品質修正プロンプト
```
Improve this English SRT subtitle file quality for optimal translation preparation.

Quality Requirements:
1. **Optimal Segment Length**: Target ~30 seconds per segment for translation efficiency
2. **Sentence Completion**: Always end segments at complete sentences with periods
3. **Context Preservation**: Maintain technical context within segments
4. **Timestamp Accuracy**: Adjust timestamps when combining segments
5. **Sequential Numbering**: Renumber segments after consolidation

Processing Guidelines:
- **Incomplete Phrases**: Always combine with next segment
- **Technical Descriptions**: Keep related technical content together
- **Sentence Fragments**: Combine until reaching natural sentence boundaries
- **Introductory Phrases**: Merge with following context

Output: Clean, translation-ready SRT file with improved segment structure.

[Provide SRT content for quality improvement]
```

## 🔧 4. 自動化ツール

### 🐍 Python自動化スクリプト

#### マークダウン生成スクリプト
**markdown_generator.py**:
```bash
# 使用方法
python scripts/markdown_generator.py \
  --subtitle-file "<日本語字幕ファイル>" \
  --node-data "<ノード挿入データ>" \
  --output "<出力マークダウンファイル>"

# 例
python scripts/markdown_generator.py \
  --subtitle-file "tutorials/Project_Skylark_Bridges/01_raw_data/chapter_01_intro/transcript_jp.srt" \
  --node-data "tutorials/Project_Skylark_Bridges/02_analysis_data/chapter_01_node_insertions.json" \
  --output "tutorials/Project_Skylark_Bridges/03_learning_guide/chapters/chapter_01_intro_学習ガイド.md"
```

**機能**:
- 字幕データとノード挿入データの統合
- タイムスタンプマッチング自動化
- マークダウン形式自動生成
- ノードリンク自動挿入

#### SRT品質修正スクリプト
**srt_quality_fixer.py**:
```bash
# 使用方法
python scripts/srt_quality_fixer.py <入力SRTファイル> <出力SRTファイル> [オプション]

# 例
python scripts/srt_quality_fixer.py "tutorials/[シリーズ名]/01_raw_data/chapter_01_intro/transcript_en.srt" "tutorials/[シリーズ名]/01_raw_data/chapter_01_intro/transcript_en_fixed.srt"
```

**機能**:
- 30秒セグメント化と文末統一自動化
- 技術用語を考慮した最適分割
- 翻訳処理効率化対応

#### MD→HTML変換スクリプト
**md_to_html_converter.py**:
```bash
# 使用方法
python scripts/md_to_html_converter.py <MDファイルパス> [出力HTMLファイルパス]

# 日本語版学習ガイド
python scripts/md_to_html_converter.py "tutorials/[シリーズ名]/03_learning_guide/chapters/chapter_01_学習ガイド.md"
```

**機能**:
- 日本語レイアウト最適化
- 技術用語リンク自動生成
- シンプルなHTML出力


## 🔧 5. トラブルシューティング

| 問題カテゴリ | 具体的問題 | 解決方法 | 予防策 |
|------------|-----------|----------|---------|
| **JavaScript実行** | "Don't paste code" セキュリティ警告 | コンソールに `allow pasting` と入力 | セキュリティ警告の事前説明 |
| **字幕取得** | 字幕が取得できない | 埋め込みページで実行（直接VimeoURL避ける） | 事前のページ確認 |
| **字幕取得** | 一部セグメントが抜ける | 再生速度を下げて再実行 | 安定したネットワーク環境 |
| **SRT形式** | タイムスタンプ形式エラー | HH:MM:SS,mmm形式確認・修正 | 品質修正スクリプト使用 |
| **翻訳品質** | 専門用語が不適切 | シリーズ用語集との整合性確認 | 用語集の事前準備 |
| **ファイル処理** | エンコーディングエラー | UTF-8で保存・文字化け時は削除後再作成 | エンコーディング設定確認 |
| **進捗管理** | JSON構文エラー | 進捗ファイルの構文検証・修復 | 定期的なバックアップ |
| **英語分析** | ノード識別エラー | Houdini公式ドキュメントとの照合 | ノード名辞書の更新 |

### 💡 6. 品質向上チェックリスト

#### 英語分析段階
- [ ] Houdiniノード名の正確な抽出
- [ ] タイムスタンプ記録の正確性
- [ ] 日本語公式ドキュメントリンクの有効性

#### 翻訳・ノード情報生成段階
- [ ] 字幕内容の自然な日本語表現
- [ ] タイムスタンプとシーケンス番号の保持
- [ ] ノード名の英語保持（例："Box SOP"）
- [ ] ノード挿入データの正確性

#### Python機械処理段階
- [ ] ファイル読み込み成功確認
- [ ] タイムスタンプマッチング精度
- [ ] マークダウン形式の正確性
- [ ] ノードリンク挿入のタイミング

#### HTML変換段階
- [ ] Markdown内容の完全変換
- [ ] 日本語レイアウト最適化
- [ ] リンク動作確認

#### 全体品質
- [ ] ファイル構造の確認
- [ ] 進捗管理の確認
- [ ] 処理時間の確認（8-10分/チャプター）
