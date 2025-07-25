# obot-chan-project/modules/ai_responder.py

import openai
from config import OPENAI_API_KEY
from prompts import AYACHAN_PROMPT

class AIResponder:
    def __init__(self):
        self.client = openai.OpenAI(api_key=OPENAI_API_KEY)
        self.system_prompt = AYACHAN_PROMPT

    def generate_response(self, user_comment: str, user_name: str) -> str:
        # 【重要】システムからの命令か、視聴者からのコメントかを判断
        if user_name == "システム":
            # 独り言モードの場合は、特別な命令文をそのまま渡す
            full_comment = user_comment
        else:
            # 通常のコメントの場合は、「〇〇さん」という形式で情報を渡す
            full_comment = f"{user_name}さんからのコメント:「{user_comment}」"

        try:
            print(f"思考中...: {full_comment}")
            completion = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": full_comment}
                ],
                temperature=0.9,
                max_tokens=300
            )
            response_text = completion.choices[0].message.content
            print(f"応答生成完了: {response_text}")
            return response_text
        except Exception as e:
            print(f"OpenAI APIでエラーが発生しました: {e}")
            return "ごめーん！ちょっと頭がパンクしちゃったみたい！"