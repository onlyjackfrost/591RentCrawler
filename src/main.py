# -*- coding: utf-8 -*-

#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.
from functools import lru_cache
import os
import sys
import time
import threading
import schedule
from dotenv import load_dotenv

from argparse import ArgumentParser
from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage,
)

load_dotenv()
app = Flask(__name__)

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)
#
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)
userId = ""


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
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    msg = ""
    global userId
    if event.message.text == "start":
        userId = event.source.user_id
        msg = "Start app for " + userId
    elif event.message.text == "stop":
        msg = "Stop app now"
        userId = ""
    else:
        msg = "Not recognized"
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=msg))


def sendNewRentPost():
    from sqlite.command import addPosts
    from logger.logger import logCrawlProgress
    from newPost import getNewRentPost
    if userId != "":
        messages, new_post_ids = getNewRentPost()
        try:
            queue = []
            for idx, message in enumerate(messages):
                if len(queue) <= 5:
                    queue.append(f'{idx+1}. \n\r' + message)
                    continue
                textMessage = '\n\r'.join(queue)
                line_bot_api.push_message(userId,
                                          TextSendMessage(text=textMessage))
                queue = []
            if queue:
                textMessage = '\n\r'.join(queue)
                line_bot_api.push_message(userId,
                                          TextSendMessage(text=textMessage))
            addPosts(new_post_ids)
            logCrawlProgress('push message and record succeed.')
        except Exception as e:
            print(e)
            logCrawlProgress('send message or insert database failed')
    else:
        print("userId is empty")


def crawlAndPush(interval: int):
    from sqlite.command import make_table
    make_table()
    schedule.every(interval).seconds.do(sendNewRentPost)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    arg_parser = ArgumentParser(usage='Usage: python ' + __file__ +
                                ' [--port <port>] [--help]')
    port = os.getenv('PORT', 8000)
    host = '0.0.0.0' if not os.getenv('HOST') else os.getenv('HOST')
    arg_parser.add_argument('-p', '--port', default=port, help='port')
    arg_parser.add_argument('-H', '--host', default=host, help='host')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')

    # crawler argument
    interval_value = 60 * 5 if not os.getenv(
        'CRAW_INTERVAL_VALUE_IN_SEC') else os.getenv(
            'CRAW_INTERVAL_VALUE_IN_SEC')
    arg_parser.add_argument(
        '-i',
        '--interval',
        default=interval_value,
        help='interval time to crawl data and push (Unit: seconds)',
        type=int)
    options = arg_parser.parse_args()

    # crawling and push
    t1 = threading.Thread(target=crawlAndPush,
                          args=(options.interval, ),
                          daemon=True)
    t1.start()

    # line app
    t2 = threading.Thread(target=app.run,
                          kwargs={
                              'debug': options.debug,
                              'port': options.port,
                              'host': options.host,
                              'use_reloader': False
                          },
                          daemon=True)
    t2.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("exiting")
        exit(0)
    # app.run(host='0.0.0.0', port=os.getenv('PORT'))