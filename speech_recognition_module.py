import threading
from typing import Optional

import speech_recognition as sr


class SpeechToText:
	"""マイク入力をテキスト化する音声認識ラッパー。"""

	def __init__(self) -> None:
		self.recognizer = sr.Recognizer()
		# マイクは遅延生成（PyAudio 未導入でも起動は可能に）
		self._microphone = None
		# 短めの無音検出でテンポよく区切る
		self.recognizer.pause_threshold = 0.6
		self._lock = threading.Lock()

	def listen_once(self, timeout: Optional[float] = None, phrase_time_limit: Optional[float] = None) -> Optional[str]:
		"""一度だけ発話を取得してテキスト化する。失敗時は None。"""
		with self._lock:
			try:
				if self._microphone is None:
					self._microphone = sr.Microphone()
				with self._microphone as source:
					self.recognizer.adjust_for_ambient_noise(source, duration=0.3)
					audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
			except Exception:
				return None
		try:
			# Google Web Speech API（無料枠）。ネット必須。
			text = self.recognizer.recognize_google(audio, language="ja-JP")
			return text.strip()
		except Exception:
			return None
