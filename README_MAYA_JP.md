# Maya Subtitler

Maya のビューポートに字幕を表示するプラグインです。SRT ファイルを読み込み、タイムラインと同期して字幕を表示します。

**[English](README_MAYA.md)** | **[Subtitler (Audio Tool)](README.md)** | **[Subtitler (日本語)](README_JP.md)**

## 機能

- SRT ファイルの直接読み込み
- タイムラインとの同期表示
- カメラごとの表示制御（メッセージアトリビュート接続）
- フォントサイズ・色・位置のカスタマイズ
- テキスト折り返し（文字単位/単語単位）
- Viewport 2.0 対応

## インストール

### モジュール方式（推奨）

1. このリポジトリを任意の場所にクローン
2. `maya_subtitler.mod` ファイルのパスを Maya のモジュールパスに追加

**方法 A**: 環境変数を設定
```
MAYA_MODULE_PATH=C:\path\to\maya-subtitler
```

**方法 B**: Maya の modules フォルダにコピー
```
# Windows
%USERPROFILE%\Documents\maya\modules\maya_subtitler.mod

# macOS / Linux
~/maya/modules/maya_subtitler.mod
```

### 手動インストール

1. `plug-ins/subtitleLocator.py` → Maya の plug-ins フォルダ
2. `scripts/maya_subtitler/` → Maya の scripts フォルダ
3. `scripts/AEsubtitleLocatorTemplate.mel` → Maya の scripts フォルダ

## 使用方法

### Python から

```python
import maya_subtitler
maya_subtitler.show_ui()
```

### UI

1. **Name**: ロケーターの名前
2. **SRT File**: 字幕ファイルのパス
3. **Start Frame**: 字幕開始フレーム（タイムライン上の位置）
4. **Font Size**: フォントサイズ
5. **Position**: 画面上の位置 (X: 左右, Y: 上下)
6. **Wrapping**: テキスト折り返し設定
   - Enable: 折り返しを有効化
   - Word Wrap: 単語単位で折り返し（日本語は文字単位推奨）
7. **Max Chars / Max Lines**: 1行の最大文字数と最大行数

### コマンドから

```python
import maya.cmds as cmds

# プラグインの読み込み
cmds.loadPlugin("subtitleLocator")

# ロケーターの作成
cmds.createSubtitleLocator(
    name="mySubtitle",
    subtitleFile="C:/path/to/subtitle.srt",
    startFrame=0,
    fontSize=24,
    positionX=0.0,
    positionY=-0.4,
)
```

## アトリビュート

| アトリビュート | 型 | 説明 | デフォルト |
|--------------|-----|------|-----------|
| `subtitleFile` | string | SRT ファイルパス | - |
| `targetCamera` | message | 表示対象カメラ（接続） | - |
| `startFrame` | int | 開始フレーム | 0 |
| `fontSize` | int | フォントサイズ | 18 |
| `fontColor` | float3 | フォント色 (RGB) | (1, 1, 1) |
| `positionX` | float | 水平位置 (-1〜1) | 0.0 |
| `positionY` | float | 垂直位置 (-1〜1) | -0.4 |
| `wrapText` | bool | 折り返し有効 | true |
| `wordWrap` | bool | 単語単位で折り返し | true |
| `maxCharsPerLine` | int | 1行最大文字数 | 80 |
| `maxLines` | int | 最大行数 | 3 |

## カメラへの接続

特定のカメラでのみ字幕を表示するには、カメラシェイプの message アトリビュートを接続します:

```python
cmds.connectAttr("perspShape.message", "subtitleLocatorShape1.targetCamera")
```

接続がない場合、すべてのカメラで表示されます。

## 複数言語の字幕

異なる言語の字幕を表示するには、複数のロケーターを作成し、表示/非表示を切り替えます:

```python
# 日本語字幕
cmds.createSubtitleLocator(name="subtitle_ja", subtitleFile="movie_ja.srt")

# 英語字幕
cmds.createSubtitleLocator(name="subtitle_en", subtitleFile="movie_en.srt")
cmds.setAttr("subtitle_en.visibility", 0)  # 非表示
```

## 対応 Maya バージョン

- Maya 2022 以降（Python 3、Viewport 2.0 対応）

## ライセンス

MIT License
