# coding: UTF-8
import requests, os, re
from bs4 import BeautifulSoup
import pathlib
from datetime import date, datetime
import pytz
from linebot.models import MessageEvent, TextMessage, FollowEvent, UnfollowEvent, TextSendMessage, ImageMessage, \
    AudioMessage
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import LineBotApiError

from dotenv import load_dotenv
load_dotenv()


def tweetinfo():
    url = "https://twitter.com/rev84"
    ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) ' \
         'AppleWebKit/537.36 (KHTML, like Gecko) ' \
         'Chrome/55.0.2883.95 Safari/537.36 '
    req = requests.get(url, headers={'User-Agent': ua})
    soup = BeautifulSoup(req.content, "html.parser")
    #find_allでdiv>content全て取得
    all_contents = soup.find_all('div', attrs={'class': 'content'})

    for i in all_contents:
        topicsindex = i.find('small', attrs={'class': 'time'})
        unixtime = int(topicsindex.find('span').get('data-time'))
        today_unixtime = datetime.fromtimestamp(unixtime, tz=pytz.timezone('Asia/Tokyo')).replace(hour=0, minute=0,
                                                                                                  second=0,
                                                                                                  microsecond=0)
        # 今日の日付をタイムゾーン付きの年月日のみで取得
        today_tzone = datetime.now(pytz.timezone('Asia/Tokyo')).replace(hour=0, minute=0, second=0, microsecond=0)

        #ツイート本文を取得
        topicsindex2 = i.find('p', attrs={'class': 'TweetTextSize'})


        # twitterの投稿日が今日 & 対象の言葉が含まれてたら、テキスト本文取得
        if today_unixtime == today_tzone and "配信を開始しました" in topicsindex2.text:
            with open("aaa.txt", "r+", encoding="utf-8",newline=None)as f:
                #対象ツイートのunixtimeを以て、一度実行済みならスルー
                if str(unixtime) == f.read().rstrip("\n"):
                    # print("一回スクレイピング済み")
                    break
                elif str(unixtime) != f.read().rstrip("\n"):
                    #ファイルをr+で開いていると追記になるので、w+で開き直して上書きの上、unixtimeを追加
                    with open("aaa.txt", "w+", encoding="utf-8",newline='\n')as ff:
                        ff.write(str(unixtime) + '\n')
                        # print("はじまった")
                        return True
                else:
                    pass
                    # print("それ以外")
        else:
            # print("該当なし")
            pass



# import pathlib
from socket import gethostname
from os import environ

HOSTNAME = gethostname()

if 'DESKTOP' in HOSTNAME:
    # current_dir = pathlib.Path(__file__).resolve().parent
    # sys.path.append(str(current_dir) + '/..../')
    from config import local_settings

    channel_access_token = local_settings.LINE_CHANNEL_ACCESS_TOKEN
else:
    channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)


def handle(*args, **options):
    line_bot_api = LineBotApi(channel_access_token)
    if tweetinfo():
        try:
            line_bot_api.push_message("Uc148172028f01d4635bdb232e6b00920", TextSendMessage(text="はじまったで！"))
        except LineBotApiError as e:
            return e
print(handle())

def callback():
    pass

def follow():
    pass


