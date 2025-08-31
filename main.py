import json
import os
import random
import threading
import time
import sys
from typing import List, Dict, Any, Deque, Tuple
from collections import deque

from dotenv import load_dotenv

from character_manager import load_characters
from gemini_client import GeminiClient
from speech_recognition_module import SpeechToText
from ui import ChatUI


def log(message: str) -> None:
	"""コンソールにログを出力する（コンソールがない場合は何もしない）。"""
	# pyinstallerの--windowedモードではsys.stdoutがNoneになるため、存在チェックを行う
	if sys.stdout:
		timestamp = time.strftime("%H:%M:%S")
		log_message = f"[{timestamp}] {message}"
		print(log_message)
		sys.stdout.flush()


def _get_base_dir() -> str:
	"""実行環境（スクリプト or .exe）に応じてリソースファイルの基準パスを返す。"""
	if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
		# PyInstallerにバンドルされた.exeとして実行中
		return os.path.dirname(sys.executable)
	else:
		# 通常の.pyスクリプトとして実行中
		return os.path.dirname(os.path.abspath(__file__))


def _choose_should_respond(probability: float) -> bool:
	"""確率に基づき応答するか決定する。"""
	return random.random() < max(0.0, min(1.0, probability))


class AppController:
	"""音声→テキスト→AI応答→UI までのメイン制御。"""

	def __init__(self) -> None:
		log("=== AI音声チャットアプリ起動 ===")
		base_dir = _get_base_dir()
		self._characters_path = os.path.join(base_dir, "characters.json")
		log(f"キャラクターファイルパス: {self._characters_path}")

		self.characters: List[Dict[str, Any]] = load_characters(self._characters_path)
		log(f"キャラクターデータ読み込み完了: {len(self.characters)}件")

		log("音声認識モジュール初期化中...")
		self.s2t = SpeechToText()
		log("音声認識モジュール初期化完了")

		self.gemini = None
		self.ui = ChatUI()
		log("UI初期化完了")

		self._init_gemini_safe()
		self._report_characters_status()

		# 直近2ターン分の履歴: (role, text) role ∈ {"user","ai:name"}
		self.history: Deque[Tuple[str, str]] = deque(maxlen=6)  # 複数AIなので最大6件程度
		# Gemini の同時実行数を制限してレート超過を避ける
		self._gen_sema = threading.Semaphore(3)

		log("音声認識ループ開始...")
		# 自動連続リッスン開始
		threading.Thread(target=self._listen_loop, daemon=True).start()
		log("=== 初期化完了、音声認識待機中 ===")

	def _report_characters_status(self) -> None:
		"""キャラクターデータの検出状況をステータスにのみ反映する。"""
		try:
			exists = os.path.exists(self._characters_path)
			if not exists:
				self.ui.set_status("characters.json 未検出")
				return
			with open(self._characters_path, "r", encoding="utf-8") as f:
				raw = json.load(f)
			count = len(raw) if isinstance(raw, list) else 0
			self.ui.set_status(f"キャラ読込: 生 {count} / 有効 {len(self.characters)}")
		except Exception:
			self.ui.set_status("characters.json 読込情報の取得に失敗")

	def _init_gemini_safe(self) -> None:
		try:
			log("Gemini API初期化中...")
			self.gemini = GeminiClient()
			self.ui.set_status("Gemini 初期化完了")
			log("✅ Gemini API初期化完了")
		except Exception as e:
			error_msg = f"Gemini 初期化エラー: {e}"
			self.ui.set_status(error_msg)
			log(f"❌ {error_msg}")

	def _listen_loop(self) -> None:
		"""UI 起動後に自動で繰り返し音声を取得し応答する。"""
		log("音声認識ループ開始")
		while True:
			try:
				self._run_once()
				# 会話の間を少し空ける
				time.sleep(0.2)
			except Exception as e:
				log(f"❌ 音声認識ループでエラー: {e}")
				time.sleep(1.0)  # エラー時は少し待機

	def _run_once(self) -> None:
		self.ui.set_status("聞き取り中…")
		log("🎤 音声聞き取り開始...")

		text = self.s2t.listen_once(timeout=5, phrase_time_limit=10)
		if not text:
			self.ui.set_status("聞き取り失敗または無音")
			log("❌ 音声聞き取り失敗または無音")
			return

		log(f"✅ 音声認識成功: 「{text}」")
		# 履歴にユーザー発話を追加
		self.history.append(("user", text))
		self.ui.set_status("AI 応答生成中…")
		log("🤖 AI応答生成開始...")

		if not self.characters:
			log("⚠️ キャラクターデータなし、デフォルトキャラクターで代替")
			# 情報はステータスのみ
			# デフォルト 1 キャラで代替
			self.characters = [
				{"id": 0, "name": "デフォルト", "personality": "丁寧で落ち着いた", "response_chance": 1.0, "delay_range": [0, 0]}
			]

		# Gemini 未初期化ならスキップ理由を明示
		if not self.gemini:
			self.ui.set_status("Gemini 未初期化: 応答スキップ")
			log("❌ Gemini未初期化のため応答スキップ")
			self.ui.set_status("待機中")
			return

		threads: List[threading.Thread] = []
		response_count = 0
		for ch in self.characters:
			if not _choose_should_respond(ch.get("response_chance", 0.5)):
				continue
			response_count += 1
			low, high = ch.get("delay_range", [0, 0])
			delay = random.uniform(float(low), float(high))
			log(f"🎭 キャラクター「{ch.get('name', 'N/A')}」応答予定 (遅延: {delay:.1f}秒)")
			thr = threading.Thread(target=self._respond_after_delay, args=(ch, text, list(self.history), delay), daemon=True)
			threads.append(thr)
			thr.start()

		if response_count == 0:
			log("⚠️ 応答するキャラクターなし")
		else:
			log(f"🎭 {response_count}人のキャラクターが応答予定")

		# 遅延最大値が大きいキャラもいるため余裕を持って待機
		for thr in threads:
			thr.join(timeout=25)
		self.ui.set_status("待機中")
		log("⏳ 待機状態に戻りました")

	def _respond_after_delay(self, character: Dict[str, Any], user_text: str, history_snapshot: List[Tuple[str, str]], delay: float) -> None:
		time.sleep(max(0.0, delay))
		if not self.gemini:
			return

		name = character.get("name", "AI")
		log(f"🎭 キャラクター「{name}」応答生成開始")

		# レート超過を避けるため同時実行を制限
		acquired = self._gen_sema.acquire(timeout=30)
		if not acquired:
			log(f"❌ キャラクター「{name}」: セマフォ取得タイムアウト")
			return

		try:
			reply = self.gemini.generate_reply_with_history(user_text, history_snapshot, character)
		except Exception as e:
			log(f"❌ キャラクター「{name}」応答生成エラー: {e}")
			return
		finally:
			self._gen_sema.release()

		# エラー文字列は表示しない
		if not reply or reply.startswith("(エラー"):
			log(f"⚠️ キャラクター「{name}」: 無効な応答内容")
			return

		log(f"✅ キャラクター「{name}」応答完了: {reply}")
		self.ui.append_message(f"{name}: {reply}")


def main() -> None:
	"""エントリーポイント。"""
	# .envファイルを明示的なパスで読み込む
	base_dir = _get_base_dir()
	dotenv_path = os.path.join(base_dir, '.env')
	if os.path.exists(dotenv_path):
		load_dotenv(dotenv_path=dotenv_path, override=False)
		log(f"Loaded .env file from: {dotenv_path}")
	else:
		log(f".env file not found at: {dotenv_path}")

	controller = AppController()
	try:
		controller.ui.mainloop()
	except KeyboardInterrupt:
		# コンソールからの Ctrl+C で静かに終了
		pass


if __name__ == "__main__":
	main()
