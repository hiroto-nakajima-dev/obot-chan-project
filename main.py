# obot-chan-project/main.py

import os
import sys
import time
import random
import pygame

from modules.youtube_reader import YouTubeReader
from modules.ai_responder import AIResponder
from modules.voice_synthesizer import VoiceSynthesizer

TEMP_VOICE_FILE = "temp_voice.mp3"
SOLILOQUY_TIMER_SECONDS = 20.0

def main():
    if len(sys.argv) < 2:
        print("エラー: 起動時にYouTubeのビデオIDを指定してください。")
        return
    
    video_id = sys.argv[1]
    print(f"彩ちゃん☆わくわく配信システム (最終完成版) を起動します...")
    print(f"ターゲットビデオID: {video_id}")

    pygame.mixer.init()

    try:
        reader = YouTubeReader(video_id=video_id)
        responder = AIResponder()
        synthesizer = VoiceSynthesizer()
        print("全てのモジュールの準備が完了しました。")
    except Exception as e:
        print(f"モジュールの初期化中にエラーが発生しました: {e}")
        return

    last_comment_time = time.time()
    used_soliloquy_themes = []

    try:
        while True:
            new_comments = reader.get_new_comments()
            if new_comments:
                last_comment_time = time.time()
                for comment in new_comments:
                    user_name = comment["author"]
                    user_comment = comment["message"]
                    response_text = responder.generate_response(user_comment=user_comment, user_name=user_name)
                    if response_text:
                        success = synthesizer.synthesize_voice(text=response_text, filepath=TEMP_VOICE_FILE)
                        if success:
                            try:
                                pygame.mixer.music.load(TEMP_VOICE_FILE)
                                pygame.mixer.music.play()
                                while pygame.mixer.music.get_busy(): time.sleep(0.1)
                            finally:
                                pygame.mixer.music.unload()
                                if os.path.exists(TEMP_VOICE_FILE): os.remove(TEMP_VOICE_FILE)
            else:
                if time.time() - last_comment_time > SOLILOQUY_TIMER_SECONDS:
                    print(f"{SOLILOQUY_TIMER_SECONDS}秒コメントがありません。独り言モードを開始します。")
                    
                    # 独り言の命令は、シンプルに「テーマ」だけを渡す
                    soliloquy_prompt = "視聴者が誰もいないみたい。何か面白いことでも喋って、場を繋いでください。"
                    
                    soliloquy_text = responder.generate_response(user_comment=soliloquy_prompt, user_name="システム")
                    
                    if soliloquy_text:
                        success = synthesizer.synthesize_voice(text=soliloquy_text, filepath=TEMP_VOICE_FILE)
                        if success:
                            try:
                                pygame.mixer.music.load(TEMP_VOICE_FILE)
                                pygame.mixer.music.play()
                                while pygame.mixer.music.get_busy(): time.sleep(0.1)
                            finally:
                                pygame.mixer.music.unload()
                                if os.path.exists(TEMP_VOICE_FILE): os.remove(TEMP_VOICE_FILE)
                    
                    last_comment_time = time.time()

                time.sleep(1)
    except KeyboardInterrupt:
        print("\n終了コマンドを受け取りました。")
    finally:
        if 'reader' in locals(): reader.terminate()
        pygame.quit()
        print("配信システム、おつかれさまでしたー！")

if __name__ == "__main__":
    main()