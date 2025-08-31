import queue
import tkinter as tk
from tkinter import ttk, scrolledtext
from typing import Optional


class ChatUI:
	"""tkinter ベースのチャット UI。"""

	def __init__(self) -> None:
		self.root = tk.Tk()
		self.root.title("AI音声チャット")
		self.root.geometry("800x600")

		# スレッドセーフなUI更新のためのキュー
		self.ui_queue = queue.Queue()

		# メインフレーム
		main_frame = ttk.Frame(self.root, padding="10")
		main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

		# チャット履歴表示エリア
		self.chat_area = scrolledtext.ScrolledText(
			main_frame,
			width=80,
			height=30,
			wrap=tk.WORD,
			state=tk.DISABLED
		)
		self.chat_area.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))

		# ステータス表示エリア
		self.status_label = ttk.Label(main_frame, text="待機中", font=("Arial", 10))
		self.status_label.grid(row=1, column=0, sticky=tk.W)

		# グリッドの重み設定
		self.root.columnconfigure(0, weight=1)
		self.root.rowconfigure(0, weight=1)
		main_frame.columnconfigure(0, weight=1)
		main_frame.rowconfigure(0, weight=1)

		# キューのポーリングを開始
		self.root.after(100, self._process_ui_queue)

	def _process_ui_queue(self) -> None:
		"""UI キューを処理して、スレッドセーフに UI を更新する。"""
		try:
			while not self.ui_queue.empty():
				# キューからタスクを取得: (command, value)
				task, value = self.ui_queue.get_nowait()

				if task == "append_message":
					self._append_message_unsafe(value)
				elif task == "set_status":
					self._set_status_unsafe(value)
		finally:
			# 100ms ごとに再度呼び出し
			self.root.after(100, self._process_ui_queue)

	def _append_message_unsafe(self, message: str) -> None:
		"""チャット履歴にメッセージを追加する（UIスレッド専用）。"""
		self.chat_area.config(state=tk.NORMAL)
		self.chat_area.insert(tk.END, message + "\n")
		self.chat_area.see(tk.END)
		self.chat_area.config(state=tk.DISABLED)

	def _set_status_unsafe(self, status: str) -> None:
		"""ステータス表示を更新する（UIスレッド専用）。"""
		self.status_label.config(text=status)

	def append_message(self, message: str) -> None:
		"""チャット履歴にメッセージを追加する（スレッドセーフ）。"""
		self.ui_queue.put(("append_message", message))

	def set_status(self, status: str) -> None:
		"""ステータス表示を更新する（スレッドセーフ）。"""
		self.ui_queue.put(("set_status", status))

	def mainloop(self) -> None:
		"""メインループを開始する。"""
		self.root.mainloop()
