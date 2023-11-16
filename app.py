from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('+CxtyG18ZUz1Y8J9p6h3DpBhEckt3VpFpO7CHrZhqIvZtPMNRgEcYRFLdaKcivBYWuIeMWH1zG5dB3aVK2XjF17tQuD/+vKmp/GL4kv+sRKNSh6Awgi//6VdXIHZj9a/rBe1oT4fIFDG6lrpB3J83AdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('9792df5d3386f64f2f7ca907f1a2c1bc')

# ファイルのパスを指定
file_path = 'C:\Users\note142\Desktop\takeyama\memo.txt'

# ファイルを読み込む
with open(file_path, 'r') as file:
    # ファイルの内容を読み込む
    file_content = file.read()

# 読み込んだ内容を表示
# print(file_content)

#回答文を設定するマップ
answers = {}
#1が入力された場合の回答を定義
answers["9"] = (print(file_content))

@app.route("/")
def test():
    return "OK TEST"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    #ユーザ入力値から前後の改行を削除
    input_message = event.message.text.strip()

   #入力値に合わせた回答文を編集
    if input_message in answers:
        reply_message = answers[input_message]
    else:
        #入力対象外は番号を選択させる文を回答
        reply_message = "エラー" 
    

    #回答文を返信
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_message))


if __name__ == "__main__":
    app.run()
