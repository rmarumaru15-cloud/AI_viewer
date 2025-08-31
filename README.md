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
1. 依存関係のインストール
```bash
pip install -r requirements.txt
```

2. 環境変数に API キーを設定（PowerShell）
```bash
$Env:GOOGLE_API_KEY="YOUR_API_KEY"
```

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

## 使用方法

1. **起動**: `start_app.bat` をダブルクリック
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
- `GOOGLE_API_KEY` が正しく設定されているか確認
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

## 注意事項
- `characters.json` は別途提供ファイルを `python-app/` 直下に配置してください。
- マイクドライバや PyAudio のインストールが必要です（エラー時は `pip install pipwin && pipwin install pyaudio` を検討）。
- ログを確認するには `start_app.bat` を使用してください。
