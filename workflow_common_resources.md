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
├── 02_english_analysis/               # 英語分析専用
│   ├── chapter_01_analysis.json      # 構造化分析データ
│   ├── chapter_01_guide_en.md        # 英語学習ガイド完全版
│   ├── chapter_02_analysis.json
│   ├── chapter_02_guide_en.md
│   └── ... (チャプター数分)
├── 03_learning_guide/                 # 日本語版学習資料
│   └── chapters/                      # チャプター別ガイド
│       ├── chapter_01_introduction_学習ガイド.md
│       ├── chapter_01_introduction_学習ガイド.html
│       ├── chapter_02_basic_logic_学習ガイド.md
│       ├── chapter_02_basic_logic_学習ガイド.html
│       └── ... (チャプター数分、MD + HTML)
├── 04_progress/                       # 進捗管理
│   └── progress_tracker.json          # シリーズ進捗ファイル
└── 05_translation_batch/              # 翻訳用一時データ
    ├── chapter_01_translation_queue.json
    ├── chapter_02_translation_queue.json
    └── translation_glossary.json      # 専門用語辞書
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
| 英語分析結果 | `chapter_{章番号}_analysis.json` | `chapter_01_analysis.json` |
| 英語学習ガイド | `chapter_{章番号}_guide_en.md` | `chapter_01_guide_en.md` |
| 翻訳キュー | `chapter_{章番号}_translation_queue.json` | `chapter_01_translation_queue.json` |
| 日本語学習ガイド(MD) | `chapter_{章番号}_{チャプター名}_学習ガイド.md` | `chapter_01_introduction_学習ガイド.md` |
| 日本語学習ガイド(HTML) | `chapter_{章番号}_{チャプター名}_学習ガイド.html` | `chapter_01_introduction_学習ガイド.html` |
| 進捗管理ファイル | `progress_tracker.json` | `progress_tracker.json` |

### 📄 進捗管理ファイル構造
```json
{
  "series_info": {
    "name": "Project_Skylark_Bridges",
    "total_chapters": 6,
    "created_date": "auto-generated",
    "last_updated": "auto-updated",
    "workflow_version": "2.0"
  },
  "chapters": [
    {
      "chapter_number": "01",
      "chapter_name": "introduction", 
      "title": "導入",
      "url": "https://example.com/chapter1",
      "status": {
        "subtitle_extraction": "completed",
        "english_analysis": "completed",
        "analysis_translation": "completed",
        "queue_translation": "completed",
        "japanese_guide_generation": "completed",
        "learning_guide_html": "completed"
      },
      "completion_date": "completed",
      "english_nodes_identified": [
        "Box SOP", "Add SOP", "Merge SOP"
      ],
      "processing_time_minutes": 12
    },
    {
      "chapter_number": "02",
      "chapter_name": "basic_logic",
      "title": "基本ロジック", 
      "url": "https://example.com/chapter2",
      "status": {
        "subtitle_extraction": "pending",
        "english_analysis": "pending",
        "analysis_translation": "pending",
        "queue_translation": "pending",
        "japanese_guide_generation": "pending",
        "learning_guide_html": "pending"
      },
      "completion_date": "pending",
      "english_nodes_identified": [],
      "processing_time_minutes": null
    }
  ],
  "series_glossary": {
    "houdini_nodes": ["Box SOP", "Add SOP", "Merge SOP"],
    "technical_terms": ["プロシージャルモデリング", "ジオメトリの散布"],
    "consistent_translations": {
      "Box SOP": "ボックスSOP",
      "Procedural Modeling": "プロシージャルモデリング",
      "Spline": "スプライン"
    }
  }
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


### 🔍 英語包括分析プロンプト
```
Analyze this English Houdini tutorial subtitle for comprehensive technical content analysis.

Series Context:
- Series Name: [シリーズ名]
- Target Chapter: [Chapter_{章番号}: チャプタータイトル]
- Previous chapters completed: [前チャプター数]
- Previously identified nodes: [既出ノードリスト]

Series Data Provided:
- progress_tracker.json content (for continuity tracking)
- series_glossary.json (established terminology)
- Previously analyzed chapters data (for cross-references)

Analysis Requirements:
1. **Houdini Node Identification**:
   - Extract all Houdini nodes mentioned
   - Identify first appearance timestamp for each node
   - Categorize by node type (SOP, DOP, VOP, etc.)
   - Note usage frequency and context
   - Check against previously identified nodes list to mark series-first appearances

2. **Technical Concept Mapping**:
   - Identify procedural workflows
   - Map relationships between concepts
   - Note learning prerequisites
   - Identify advanced vs beginner concepts
   - Track how concepts build upon previous chapters

3. **Learning Structure Analysis**:
   - Break content into logical learning segments
   - Identify key learning objectives
   - Note practical exercises or examples
   - Determine chapter prerequisites
   - Create clear segment boundaries for translation

4. **Series Continuity Tracking**:
   - Mark which nodes are series-first appearances (check against provided node list)
   - Track conceptual progression from previous chapters
   - Note explicit references to earlier chapters
   - Identify new concepts introduced in this chapter

Output Format (JSON):
{
  "chapter_info": {
    "number": "01",
    "title": "Introduction",
    "duration_seconds": 1200
  },
  "houdini_nodes": [
    {
      "node_name": "Box SOP",
      "node_type": "SOP",
      "first_appearance_timestamp": "00:02:15",
      "usage_frequency": 3,
      "context": "Creating placeholder geometry",
      "series_first_appearance": true,
      "difficulty_level": "beginner"
    }
  ],
  "technical_concepts": [
    {
      "concept": "Procedural Modeling",
      "introduction_timestamp": "00:01:30",
      "importance": "fundamental",
      "prerequisites": ["Basic 3D understanding"],
      "builds_upon": []
    }
  ],
  "learning_segments": [
    {
      "start_time": "00:00:00",
      "end_time": "00:02:30",
      "title": "Introduction and Setup",
      "objectives": ["Understanding the project scope", "Setting up placeholder geometry"],
      "key_concepts": ["Workflow planning", "Placeholder creation"],
      "nodes_introduced": ["Box SOP", "Merge SOP"]
    }
  ],
  "series_continuity": {
    "references_to_previous": [],
    "concepts_continued": [],
    "new_concepts_introduced": ["Procedural bridge building", "Environment asset placement"],
    "nodes_from_previous_chapters": []
  }
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
   - Include detailed explanations ONLY for nodes marked as "series_first_appearance": true
   - For previously introduced nodes, add brief context only if usage differs significantly
   - Reference previous chapter when node was first introduced
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

[For previously introduced nodes, only if context is significantly different:]
📝 **[Node Name]** *(Previously introduced in Chapter X)*
- New usage context: [Brief explanation of different usage]

[Continue for all segments...]

Important Guidelines:
- Check analysis JSON for "series_first_appearance" flag before adding node documentation
- Reference learning_segments from analysis for structure
- Maintain continuity with previous chapters using series_continuity data
- Only document nodes on their FIRST appearance in the entire series
- Keep explanations concise and practical

Generate the complete guide covering all subtitle segments with appropriate technical commentary.

[Provide analysis JSON and subtitle data]
```

### 🔄 第1段階翻訳プロンプト（analysis.json翻訳）
```
Translate this English Houdini tutorial analysis data to Japanese, maintaining technical accuracy and structural integrity.

Series Context:
- Series Name: [シリーズ名]
- Target Chapter: [Chapter_{章番号}: チャプタータイトル]
- Previous chapters completed: [前チャプター数]
- Previously established terminology: [確立された専門用語リスト]

Series Data Provided:
- series_glossary.json (established translations from previous chapters)
- progress_tracker.json (for terminology consistency tracking)

Focus: Technical analysis data translation

Content to Translate:
**Analysis JSON Data**: [analysis.json内容]

Translation Requirements:
1. **JSON Structure Preservation**: Maintain all keys, arrays, and object structures exactly
2. **Terminology Consistency**:
   - Use series_glossary.json for established translations:
     - Box SOP → ボックスSOP
     - procedural → プロシージャル
     - spline → スプライン
     - Blueprint → ブループリント
     - Material → マテリアル
   - Add new technical terms to terminology tracking
3. **Technical Accuracy**: 
   - Preserve ALL node names exactly as they appear in English (e.g., "Box SOP" stays "Box SOP")
   - Maintain timestamp formats unchanged (HH:MM:SS)
   - Keep all IDs and references intact
   - Preserve difficulty_level, node_type fields exactly
4. **Series Consistency**: 
   - Use established terminology from previous chapters
   - Maintain consistent translation style
   - Track new terminology for future chapters
5. **Cultural Adaptation**:
   - Natural Japanese technical documentation style
   - Appropriate level of formality for technical content

Special Instructions:
- Translate concept names, descriptions, and contextual information to Japanese
- Keep technical identifiers (node names, timestamps, URLs) in original format
- Update series glossary with any new translations introduced

Output Format:
Complete translated analysis_jp.json with identical structure + terminology_updates for series glossary

[Provide analysis.json content and series_glossary.json for translation]
```

### 🔄 第2段階翻訳プロンプト（translation_queue.json翻訳）
```
Translate this English Houdini tutorial structured data to Japanese, focusing on subtitle content and learning segments.

Series Context:
- Series Name: [シリーズ名]
- Target Chapter: [Chapter_{章番号}: チャプタータイトル]
- Previous chapters completed: [前チャプター数]
- Established terminology: [確立された専門用語リスト]

Series Data Provided:
- series_glossary.json (consistent translations)
- analysis_jp.json (translated technical concepts)

Focus: Subtitle and learning content translation

Content to Translate:
**Translation Queue JSON Data**: [translation_queue.json内容]

Translation Requirements:
1. **Structure Preservation**: Maintain all JSON structure integrity exactly
2. **SRT Content Translation**: 
   - Natural Japanese subtitle expressions suitable for video synchronization
   - Use established terminology from series_glossary.json:
     - Box SOP → ボックスSOP
     - procedural → プロシージャル
     - spline → スプライン
   - Maintain technical term consistency throughout
   - Keep ALL timing and formatting intact (timestamps, sequence numbers)
   - Preserve subtitle segment boundaries exactly as provided

3. **Learning Segment Translation**:
   - Clear instructional Japanese appropriate for technical tutorials
   - Maintain learning objectives clarity and actionable language
   - Preserve educational flow and logical progression
   - Ensure consistency with analysis_jp.json terminology

4. **Cultural Adaptation**:
   - Natural Japanese tutorial language (tutorial-appropriate keigo level)
   - Appropriate technical explanations for Japanese learners
   - Clear, direct instructional tone
   - Maintain technical precision while ensuring accessibility

5. **Quality Assurance**:
   - Cross-reference with analysis_jp.json for consistency
   - Verify all node names and technical terms match established translations
   - Ensure subtitle timing remains unchanged
   - Check that learning segment structure supports clear progression

Output Structure:
{
  "translation_queue_jp": {
    "chapter_info": {...},
    "learning_segments": [...],
    "technical_concepts": [...],
    "subtitle_segments": [...]
  },
  "srt_content_jp": "[完全な日本語SRT形式データ - all segments with correct numbering and timing]",
  "terminology_used": [...],
  "quality_checks": {
    "total_subtitle_segments": number,
    "technical_terms_verified": [...],
    "timing_preserved": boolean
  }
}

[Provide translation_queue.json content and series_glossary.json for translation]
```

### 🔄 日本語ガイド生成プロンプト
```
Create a comprehensive Japanese learning guide using these translated structured data sets.

Input Data:
- analysis_jp.json: [翻訳済み分析結果 - includes series continuity data]
- translation_queue_jp.json: [翻訳済み構造化データ - includes translated subtitles]
- transcript_jp.srt: [日本語字幕データ]
- series_glossary.json: [シリーズ全体の専門用語集]
- Chapter Number: [章番号]
- Total Chapters: [総チャプター数]

Generation Requirements:
1. **Complete Timestamp Coverage**: Use Japanese subtitles for ALL segments from transcript_jp.srt, no omissions
2. **Node Documentation**: 
   - Include detailed explanations ONLY for nodes marked as "series_first_appearance": true in analysis_jp.json
   - For previously introduced nodes, only add context if usage significantly differs
   - Reference the chapter where node was first introduced: "（チャプターX初出）"
3. **Learning Structure**: 
   - Use learning_segments from translation_queue_jp.json for structuring content sections
   - Organize by logical learning progression
   - Include clear learning objectives for each section
4. **Technical Writing Style**: 
   - Natural Japanese technical documentation style
   - Appropriate keigo level for educational content
   - Clear, precise terminology using series_glossary.json
5. **Series Consistency**: 
   - Maintain terminology consistency using established translations
   - Reference previous chapters where relevant using series_continuity data
   - Build upon concepts introduced in earlier chapters

Guide Structure:
# [Series Name] - Chapter {number}: [Chapter Title] 学習ガイド（日本語版）

**シリーズ情報**:
- シリーズ: [Series Name]
- チャプター: {number} / {total chapters}
- 動画URL: [URL](URL)
- 時間: [duration from analysis_jp.json]
- 前提条件: [Prerequisites from previous chapters]

## 学習内容

[Use learning_segments from translation_queue_jp.json:]
### [Section Title] ([start_time] - [end_time])
- **学習目標**: [Learning objectives in Japanese]
- **主要概念**: [Key concepts introduced]
- **使用ノード**: [Nodes introduced in this segment]

[Continue for all learning segments]

---

## [timestamp]
「[Japanese subtitle text from transcript_jp.srt]」

[For nodes with series_first_appearance: true ONLY:]
📝 **[Node Name] [Node Type]** *(シリーズ初出)*
- **参照**: [Official documentation link]
- **機能**: [Function description in Japanese from analysis_jp.json]
- **主要パラメータ**: [Key parameters in Japanese]
- **使用例**: [Common use cases]
- **初心者向け注意**: [Beginner notes in Japanese]

[For previously introduced nodes, if context differs:]
📝 **[Node Name]** *(チャプターX初出)*
- **新しい使用方法**: [New usage context in Japanese]

[Continue for ALL segments from transcript_jp.srt...]

Important Guidelines:
- Verify node documentation against "series_first_appearance" flag in analysis_jp.json
- Cross-reference all technical terms with series_glossary.json
- Include ALL subtitle segments with appropriate timestamps
- Maintain educational flow using learning_segments structure
- Only document nodes on their FIRST appearance in the entire series
- Add chapter cross-references where concepts build upon previous material

Quality Assurance:
- Ensure all timestamps from transcript_jp.srt are included
- Verify technical terminology consistency with series glossary
- Check that learning objectives align with content coverage
- Confirm series continuity references are accurate

Output: Complete Japanese learning guide with integrated learning content overview at the beginning

[Provide all translated structured data: analysis_jp.json, translation_queue_jp.json, transcript_jp.srt, and series_glossary.json]
```

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

#### SRT品質修正スクリプト
**srt_quality_fixer.py**:
```bash
# 使用方法
python scripts/srt_quality_fixer.py <入力SRTファイル> <出力SRTファイル> [オプション]

# 例
python scripts/srt_quality_fixer.py "tutorials/[シリーズ名]/01_raw_data/chapter_01_intro/transcript_1096045116_intro_en.srt" "tutorials/[シリーズ名]/01_raw_data/chapter_01_intro/transcript_1096045116_intro_en_fixed.srt"

# オプション指定
python scripts/srt_quality_fixer.py input_en.srt output_en_fixed.srt --target-duration 30 --optimize-for-translation
```

**機能**:
- `--optimize-for-translation`: 翻訳効率に特化した最適化
- `--preserve-technical-terms`: 技術用語の境界を考慮した分割
- `--context-awareness`: 文脈を考慮した自然な分割点選択

#### MD→HTML変換スクリプト
**md_to_html_converter.py**:
```bash
# 使用方法
python scripts/md_to_html_converter.py <MDファイルパス> [出力HTMLファイルパス]

# 英語版学習ガイド
python scripts/md_to_html_converter.py "tutorials/[シリーズ名]/02_english_analysis/chapter_01_guide_en.md"

# 日本語版学習ガイド
python scripts/md_to_html_converter.py "tutorials/[シリーズ名]/03_learning_guide/chapters/chapter_01_学習ガイド.md"
```

**機能**:
- 英語・日本語レイアウト自動判定・最適化
- 技術用語の自動リンク生成
- シリーズナビゲーション生成


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
- [ ] 全Houdiniノードの正確な識別・分類
- [ ] 技術的文脈の完全な理解
- [ ] シリーズ全体での位置づけ明確化

#### 第1段階翻訳（analysis.json）
- [ ] Houdiniノード情報の正確な翻訳
- [ ] 技術概念の適切な日本語化
- [ ] JSON構造の完全保持
- [ ] 専門用語一貫性確保

#### 第2段階翻訳（translation_queue.json）
- [ ] 字幕内容の自然な日本語表現
- [ ] 学習セグメントの明確性
- [ ] 文脈保持による品質確保
- [ ] シリーズ全体での用語統一

#### 日本語ガイド生成段階
- [ ] 翻訳済みデータの適切な統合
- [ ] タイムスタンプの完全カバレッジ
- [ ] 技術文書スタイルの維持
- [ ] 初出ノード解説の適切な配置

#### 学習ガイド
- [ ] タイムスタンプの完全性確認
- [ ] ノード初出マークの適切な配置
- [ ] 英語版との内容一致確認
- [ ] 学習進行の論理性確認

#### HTML版
- [ ] Markdown内容の完全保持確認
- [ ] 全セグメントの変換確認
- [ ] 日本語レイアウトの最適化
- [ ] ナビゲーション機能の動作確認

#### 全体品質
- [ ] ファイル構造の整合性確認
- [ ] 進捗管理の正確性確認
- [ ] シリーズ一貫性の維持
- [ ] 処理時間の記録・分析
