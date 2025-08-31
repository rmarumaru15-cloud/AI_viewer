import json
import re
import os
from typing import List, Dict, Any


def load_characters(json_path: str) -> List[Dict[str, Any]]:
	"""キャラクターデータ JSON を読み込み、整形済みリストを返す。

	- ファイルが無い場合は空リストを返す。
	- 必須キー欠損や型不正はスキップして続行する。
	"""
	if not os.path.exists(json_path):
		return []

	try:
		# UTF-8 BOM 対応
		with open(json_path, "r", encoding="utf-8-sig") as f:
			text = f.read()
		try:
			data = json.loads(text)
		except Exception:
			# 末尾カンマなど軽微なエラーを自動修正して再試行
			fixed = _try_lenient_json(text)
			if fixed is None:
				return []
			data = fixed
	except Exception:
		return []

	validated: List[Dict[str, Any]] = []
	if not isinstance(data, list):
		return validated

	for item in data:
		try:
			if not isinstance(item, dict):
				continue
			_id = item.get("id")
			name = item.get("name")
			personality = item.get("personality")
			response_chance = float(item.get("response_chance", 0.0))
			delay_range = item.get("delay_range", [2, 8])

			if _id is None or name is None or personality is None:
				continue
			if not isinstance(delay_range, list) or len(delay_range) != 2:
				delay_range = [2, 8]
			low, high = delay_range
			try:
				low = float(low)
				high = float(high)
			except Exception:
				low, high = 2.0, 8.0
			if low < 0:
				low = 0.0
			if high < low:
				high = low

			validated.append(
				{
					"id": _id,
					"name": str(name),
					"personality": str(personality),
					"response_chance": max(0.0, min(1.0, response_chance)),
					"delay_range": [low, high],
				}
			)
		except Exception:
			# 一件不正でも全体は止めない
			continue

	return validated


def _try_lenient_json(text: str) -> Any | None:
	"""よくある JSON フォーマット誤り（末尾カンマ）を補正して parse を試みる。"""
	try:
		# オブジェクト/配列の末尾カンマを除去
		no_trailing_commas = re.sub(r",\s*(\]|\})", r"\1", text)
		return json.loads(no_trailing_commas)
	except Exception:
		return None
