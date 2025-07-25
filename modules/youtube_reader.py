# obot-chan-project/modules/youtube_reader.py

import pytchat
import time
from typing import Dict, Optional

class YouTubeReader:
    """
    pytchatを使用して、指定されたYouTube Liveのコメントをリアルタイムで取得するクラス。
    """
    # 【修正】__init__メソッドが、正しく`video_id`を受け取れるように引数を追加
    def __init__(self, video_id: str):
        """
        YouTubeReaderのインスタンスを初期化し、チャットの監視を開始します。

        Args:
            video_id (str): 監視対象のYouTubeライブのビデオID。
        """
        if not video_id or video_id == "YOUR_VIDEO_ID_HERE":
            raise ValueError("YouTubeのビデオIDが指定されていません。")
        
        print(f"YouTube Reader (本番モード) が起動しました。")
        print(f"ビデオID: {video_id} のコメント監視を開始します...")
        
        try:
            # 受け取った`video_id`を使って、pytchatを初期化
            self.chat = pytchat.create(video_id=video_id)
            self.video_id = video_id
        except Exception as e:
            print(f"エラー: pytchatの初期化に失敗しました。ビデオID「{video_id}」が正しいか、ライブが配信中か確認してください。")
            # pytchatの例外をそのまま投げることで、より詳細なエラーが分かるようにする
            raise e

    def get_new_comments(self) -> list:
        """
        新しいコメントを複数件まとめて取得します。

        Returns:
            list: 新しいコメントの著者とメッセージを含む辞書のリスト。
        """
        comments = []
        if self.chat.is_alive():
            try:
                for c in self.chat.get().items:
                    comment_data = {"author": c.author.name, "message": c.message}
                    comments.append(comment_data)
                    print(f"新着コメント受信: [{c.author.name}] {c.message}")
            except Exception as e:
                print(f"コメントの取得中にエラーが発生しました: {e}")

        return comments

    def terminate(self):
        """
        チャットの監視を終了します。
        """
        if hasattr(self, 'chat') and self.chat.is_alive():
            print("YouTube Readerの監視を終了します。")
            self.chat.terminate()