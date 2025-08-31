# AI音声応答ツール（Python / tkinter）

## 概要
このアプリは、マイクから取得したユーザー音声をテキスト化し、複数のAIキャラクターが短文でバラバラに応答するデスクトップアプリケーションです。

## 主な機能
- 音声認識（SpeechRecognition + マイク）
- Gemini API を用いた応答生成
- 複数キャラクターの応答（確率・遅延）
- tkinter でのチャット表示
- リアルタイムログ表示

## 必要要件
- Python 3.10+
- マイク入力が可能な環境（Windows）
- Google API キー（Gemini 用）

## セットアップ

### 1. 依存関係のインストール
```bash
pip install -r requirements.txt
```

### 2. APIキーの設定（推奨）
本アプリケーションの使用には、Google の API キー（Gemini用）が必要です。

1. `.env.example` ファイルをコピーして、同じ階層に `.env` という名前のファイルを作成します。
2. 作成した `.env` ファイルを開き、`YOUR_API_KEY_HERE` の部分を自分のAPIキーに書き換えます。

```ini
# .env ファイルの例
GOOGLE_API_KEY="ここにあなたのAPIキーを貼り付け"
```

APIキーは [Google AI Studio](https://aistudio.google.com/app/apikey) から取得できます。

### (代替) 環境変数による設定
`.env` ファイルを使用しない場合、従来通り環境変数に `GOOGLE_API_KEY` を設定することでも動作します。

## 実行方法

### 推奨方法（ログ表示付き）
```bash
# バッチファイルで起動（推奨）
start_app.bat
```

### 通常の起動
```bash
python main.py
```

## 実行可能ファイル(EXE)のビルド
このアプリケーションは、`PyInstaller` を使って単一の実行可能ファイル（`.exe`）に変換することができます。

1. **PyInstallerのインストール** (未導入の場合)
   ```bash
   pip install pyinstaller
   ```
2. **ビルドスクリプトの実行**
   プロジェクトのルートにある `build.bat` を実行します。
   ```bash
   build.bat
   ```
3. **成果物の確認**
   ビルドが成功すると、`dist` フォルダ内に `main.exe` が生成されます。このファイルを単体で他の場所に移動して実行することも可能です。

## 使用方法

1. **起動**: `start_app.bat` をダブルクリック、または `dist/main.exe` を実行
2. **音声認識**: マイクに向かって話す
3. **AI応答**: 複数のキャラクターが順次応答
4. **ログ確認**: コマンドプロンプトでリアルタイムログを確認

## トラブルシューティング

### 音声認識が動作しない場合
- マイクが正しく接続されているか確認
- マイクの権限が許可されているか確認
- PyAudioが正しくインストールされているか確認

### AI応答が来ない場合
- コマンドプロンプトのログを確認
- `.env` ファイルまたは環境変数で `GOOGLE_API_KEY` が正しく設定されているか確認
- インターネット接続を確認

### エラーログの確認方法
- コマンドプロンプトに表示されるログを確認
- エラーメッセージの内容を確認
- ステータスバーの表示を確認

## ファイル構成
- main.py: メイン制御（音声→テキスト→AI応答→UI表示）
- speech_recognition_module.py: 音声認識
- gemini_client.py: Gemini API クライアント
- character_manager.py: キャラクター管理（JSON 読み込み）
- ui.py: tkinter ベースのチャット UI
- characters.json: キャラクターデータ
- start_app.bat: ログ表示付き起動用バッチファイル
- build.bat: EXEビルド用バッチファイル
- .env.example: APIキー設定用のテンプレートファイル

## 注意事項
- `characters.json` は別途提供ファイルを `python-app/` 直下に配置してください。
- マイクドライバや PyAudio のインストールが必要です（エラー時は `pip install pipwin && pipwin install pyaudio` を検討）。
- ログを確認するには `start_app.bat` を使用してください。
