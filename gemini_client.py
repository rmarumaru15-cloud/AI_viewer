import os
from typing import Dict, Any, List, Tuple

from dotenv import load_dotenv

import google.generativeai as genai


class GeminiClient:
	"""Gemini API を用いてキャラクター応答を生成するクライアント。"""

	def __init__(self, api_key: str | None = None, model_name: str = "gemini-2.5-flash-preview-05-20") -> None:
		# .env を読み込んでから環境変数参照
		load_dotenv(override=False)
		api_key = api_key or os.environ.get("GOOGLE_API_KEY")
		if not api_key:
			raise RuntimeError("GOOGLE_API_KEY が設定されていません。")
		self.model = genai.GenerativeModel(model_name)

	def build_prompt(self, user_text: str, character: Dict[str, Any]) -> str:
		"""設計書の方針に従ってプロンプト文を組み立てる。"""
		name = character.get("name", "キャラクター")
		personality = character.get("personality", "")
		return (
			f"あなたは『{name}』というキャラクターです。\n"
			f"性格: {personality}\n"
			"口調と一貫性を保ち、日本語で、短く一言で応答してください。\n"
			f"ユーザーの言葉: 「{user_text}」"
		)

	def generate_reply(self, user_text: str, character: Dict[str, Any]) -> str:
		"""ユーザー発話とキャラクター設定から短い応答を生成する。"""
		prompt = self.build_prompt(user_text, character)
		# print(f"[Gemini Prompt] {prompt}")  # プロンプト内容をログ出力（コメントアウト）
		try:
			resp = self.model.generate_content(prompt)
			text = resp.text or ""
		except Exception as e:
			text = f"(エラー: {e.__class__.__name__})"
		return text.strip()

	def generate_reply_with_history(self, user_text: str, history: List[Tuple[str, str]], character: Dict[str, Any]) -> str:
		"""直近履歴（user/ai）を含めて応答を生成する。"""
		name = character.get("name", "キャラクター")
		personality = character.get("personality", "")
		lines = [
			f"あなたは『{name}』というキャラクターです。",
			f"性格: {personality}",
			"口調と一貫性を保ち、日本語で、短く一言で応答してください。",
			"これまでの会話の抜粋:",
		]
		for role, text in history[-4:]:
			if role == "user":
				lines.append(f"ユーザー: {text}")
			else:
				lines.append(f"{role}: {text}")
		lines.append(f"今回のユーザーの言葉: 「{user_text}」")
		prompt = "\n".join(lines)
		# print(f"[Gemini Prompt] {prompt}")  # プロンプト内容をログ出力（コメントアウト）
		try:
			resp = self.model.generate_content(prompt)
			text = resp.text or ""
		except Exception as e:
			text = f"(エラー: {e.__class__.__name__})"
		return text.strip()
		return text.strip()
