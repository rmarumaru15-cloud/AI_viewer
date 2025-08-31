@echo off
chcp 65001 >nul
title AI音声チャット - ログ表示

echo ========================================
echo AI音声チャットアプリケーション
echo ========================================
echo.
echo このウィンドウにはリアルタイムログが表示されます
echo エラーや問題が発生した場合はここで確認できます
echo.
echo アプリを終了するには、このウィンドウを閉じてください
echo ========================================
echo.

REM 仮想環境をアクティベート
call venv\Scripts\activate.bat

REM アプリを起動
python main.py

echo.
echo アプリケーションが終了しました
pause
