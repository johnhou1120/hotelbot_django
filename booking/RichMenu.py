import os
import requests
from linebot import LineBotApi
from linebot.models import *
from django.conf import settings

class rich_mene():
    id_first = ""
    id_second = ""

    def __init__(self):
        self.id_first = self.get_rich_menu_id_first()
        self.id_second = self.get_rich_menu_id_second()

    def get_rich_menu_id_first(self):
        line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
        # create rich menu
        # from https://developers.line.biz/en/reference/messaging-api/#create-rich-menu
        rich_menu_to_create = RichMenu(
            size=RichMenuSize(width=1200, height=810), #2500x1686, 2500x843, 1200x810, 1200x405, 800x540, 800x270
            selected=True,
            name="NextPage",
            chat_bar_text="See Menu",
            areas=[
                RichMenuArea(
                    bounds=RichMenuBounds(x=20, y=40, width=1160, height=360),
                    action=URIAction(label='關於我們', uri='https://liff.line.me/1657480937-RKGxkoqY')),
                RichMenuArea(
                    bounds=RichMenuBounds(x=20, y=420, width=475, height=250),
                    action=MessageAction(label='訂房服務', text='@訂房服務')),
                RichMenuArea(
                    bounds=RichMenuBounds(x=510, y=420, width=210, height=250),
                    action=URIAction(label='加值服務', uri='https://liff.line.me/1657480937-m69MAkzl')),
                RichMenuArea(
                    bounds=RichMenuBounds(x=750, y=420, width=210, height=250),
                    action=MessageAction(label='周邊景點', text='@周邊景點')),
                RichMenuArea(
                    bounds=RichMenuBounds(x=970, y=420, width=210, height=250),
                    action=MessageAction(label='專人客服', text='@專人客服')),
                RichMenuArea(
                    bounds=RichMenuBounds(x=20, y=690, width=1160, height=80),
                    action=PostbackAction(label='Next Page', data='action=nextpage')),
                ]
        )
        rich_menu_id = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create)
        print("rich_menu_id", rich_menu_id)
        # upload image and link it to richmenu
        # from https://developers.line.biz/en/reference/messaging-api/#upload-rich-menu-image
        with open(os.path.join(settings.STATICFILES_DIRS[0], 'img', 'firstpage.png'), 'rb') as f:
            line_bot_api.set_rich_menu_image(rich_menu_id, 'image/png', f)
        # set as default image
        url = "https://api.line.me/v2/bot/user/all/richmenu/" + rich_menu_id
        requests.post(url, headers={"Authorization": "Bearer " + settings.LINE_CHANNEL_ACCESS_TOKEN})

        return rich_menu_id

    def get_rich_menu_id_second(self):
        line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
        # create rich menu
        # from https://developers.line.biz/en/reference/messaging-api/#create-rich-menu
        rich_menu_to_create = RichMenu(
            size=RichMenuSize(width=1200, height=810), #2500x1686, 2500x843, 1200x810, 1200x405, 800x540, 800x270
            selected=True,
            name="Controller",
            chat_bar_text="Controller",
            areas=[
                RichMenuArea(
                    bounds=RichMenuBounds(x=20, y=40, width=1160, height=360),
                    action=URIAction(label='IG', uri='https://liff.line.me/1657480937-rEM96eB8')),
                RichMenuArea(
                    bounds=RichMenuBounds(x=20, y=420, width=570, height=250),
                    action=URIAction(label='優惠劵', uri='https://lin.ee/WxSmwrc')),
                RichMenuArea(
                    bounds=RichMenuBounds(x=610, y=420, width=570, height=250),
                    action=URIAction(label='集點卡', uri='https://lin.ee/qBg0ZX0')),
                RichMenuArea(
                    bounds=RichMenuBounds(x=20, y=690, width=1160, height=80),
                    action=PostbackAction(label='Previous Page', data='action=previouspage')),
                ]
        )
        rich_menu_id = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create)
        print("rich_menu_id", rich_menu_id)
        # upload image and link it to richmenu
        # from https://developers.line.biz/en/reference/messaging-api/#upload-rich-menu-image
        with open(os.path.join(settings.STATICFILES_DIRS[0], 'img', 'secondpage.png'), 'rb') as f:
            line_bot_api.set_rich_menu_image(rich_menu_id, 'image/png', f)

        return  rich_menu_id

    