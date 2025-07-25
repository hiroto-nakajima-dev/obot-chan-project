# obot-chan-project/modules/voice_synthesizer.py

import requests
import json
from config import AIVIS_API_KEY

class VoiceSynthesizer:
    """
    Aivis Cloud APIと通信し、テキストから音声を生成するクラス。
    """
    API_BASE_URL = "https://api.aivis-project.com/v1/tts/synthesize"
    MODEL_UUID = "a670e6b8-0852-45b2-8704-1bc9862f2fe6"
    SPEAKER_UUID = "b1ca560f-f212-4e67-ab7d-0a4f5afb75a8"

    def __init__(self):
        if not AIVIS_API_KEY or AIVIS_API_KEY == "aivis_eKctQWQsxVenfQxaz3ZQfNnEgb4xfSyI":
            print("警告: Aivis APIキーが初期値のままの可能性があります。本番運用前にご確認ください。")
        self.headers = {
            "Authorization": f"Bearer {AIVIS_API_KEY}",
            "Content-Type": "application/json"
        }
        self.session = requests.Session()

    def synthesize_voice(self, text: str, filepath: str) -> bool:
        payload = {
            "model_uuid": self.MODEL_UUID,
            "speaker_uuid": self.SPEAKER_UUID,
            "text": text,
            "output_format": "mp3",
            "output_sampling_rate": 44100
        }
        print(f"Aivis Cloud APIに音声合成をリクエスト中 (モデル: {self.MODEL_UUID})...")
        try:
            response = self.session.post(
                self.API_BASE_URL,
                headers=self.headers,
                data=json.dumps(payload),
                stream=True,
                timeout=30
            )
            if response.status_code == 200:
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"音声ファイルを '{filepath}' として正常に保存しました。")
                return True
            else:
                error_details = response.json()
                print(f"エラー: Aivis Cloud APIでの音声合成に失敗しました。ステータスコード: {response.status_code}")
                print(f"詳細: {error_details}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"エラー: Aivis Cloud APIとの通信に失敗しました。")
            print(f"詳細: {e}")
            return False
        except Exception as e:
            print(f"予期せぬエラーが発生しました: {e}")
            return False