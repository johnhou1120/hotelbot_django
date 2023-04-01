from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, Http404, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from django.forms.models import model_to_dict
from linebot import LineBotApi, WebhookParser, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import *

import googlemaps

from booking.models import * 
import os

from booking.RichMenu import *
from .MyLib.MyDateTime import MyDateTime

from qrcode import QRCode
import qrcode

# Create your views here.

# region Linebot

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

richmenu = rich_mene()

# handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)
# @handler.add(PostbackEvent)
# def handle_postback(event):
#     line_id = event.source.user_id
#     if event.postback.data == "action=nextpage":
#         line_bot_api.link_rich_menu_to_user(line_id, get_rich_menu_id_second())
#     elif event.postback.data == "action=previouspage":
#         line_bot_api.link_rich_menu_to_user(line_id, get_rich_menu_id_first())

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            uid=event.source.user_id
            if isinstance(event, MessageEvent):
                mtext=event.message.text
                
                profile=line_bot_api.get_profile(uid)
                name=profile.display_name
                pic_url=profile.picture_url

                message=[]
                user = Users.objects.filter(lineid=uid).first()
                if not user:
                    Users.objects.create(lineid=uid,nick_name=name,image_url=pic_url)
                    # message.append(TextSendMessage(text='會員資料新增完畢'))
                else:
                    user.nick_name = name
                    user.image_url = pic_url
                    # message.append(TextSendMessage(text='已經有建立會員資料囉'))

                msgtext = event.message.text
                
                # region 訊息判斷

                if '@訂房服務' in msgtext:
                    message.append(list_all_RoomTypes())

                elif '@加值服務' in msgtext:
                    message.append(TextSendMessage(text='建置中，謝謝您的耐心等待！！'))

                elif '@專人客服' in msgtext:
                    message.append(one2oneService())

                elif '@週邊活動' in msgtext or '@周邊景點' in msgtext:
                    message.append(list_all_activities())

                elif 'GET MAP' in msgtext:
                    strLocationName = msgtext.split(':')[1] 
                    message = GetMapMessage(strLocationName)

                # endregion

                line_bot_api.reply_message(event.reply_token, message)

            elif isinstance(event, FollowEvent):
                print('加入好友')
                line_bot_api.reply_message(event.reply_token,message)

            elif isinstance(event, UnfollowEvent):
                print('取消好友')

            elif isinstance(event, JoinEvent):
                print('進入群組')
                line_bot_api.reply_message(event.reply_token,message)

            elif isinstance(event, LeaveEvent):
                print('離開群組')
                line_bot_api.reply_message(event.reply_token,message)

            elif isinstance(event, MemberJoinedEvent):
                print('有人入群')
                line_bot_api.reply_message(event.reply_token,message)

            elif isinstance(event, MemberLeftEvent):
                print('有人退群')
                line_bot_api.reply_message(event.reply_token,message)

            elif isinstance(event, PostbackEvent):
                print('PostbackEvent')
                if event.postback.data == "action=nextpage":
                    line_bot_api.link_rich_menu_to_user(uid, richmenu.id_second)
                elif event.postback.data == "action=previouspage":
                    line_bot_api.link_rich_menu_to_user(uid, richmenu.id_first)

        return HttpResponse()
    else:
        return HttpResponseBadRequest()

def one2oneService():
    flex_message = FlexSendMessage(
        alt_text="專人服務",
        contents={
            "type": "bubble",
            "size": "kilo",
            "hero": {
                "type": "image",
                "url": "https://i.imgur.com/YsAAuxy.png", ##待換
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": [
                {
                    "type": "text",
                    "text": "專人客服",
                    "size": "xl",
                    "weight": "bold"
                }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                {
                    "type": "button",
                    "style": "primary",
                    "color": "#905c44",
                    "margin": "md",
                    "action": {
                    "type": "uri",
                    "label": "專人聊天室",
                    "uri": "https://lin.ee/gXfrl0X"
                    }
                },
                {
                    "type": "button",
                    "style": "primary",
                    "color": "#905c44",
                    "margin": "sm",
                    "action": {
                    "type": "uri",
                    "label": "Call me",
                    "uri":'tel://0800270008'
                    }
                }
                ]
            }
        }
    )
    return flex_message

def list_all_RoomTypes():
    #抓取資料庫中所有產品的資料
    RoomTypes = RoomType.objects.all()
    bubbles = []

    for type in RoomTypes:
        struri = "https://6884-2001-b400-e73d-1b00-4042-ed47-71f5-f5e3.ap.ngrok.io/booking/" + type.rt_name + "/"
        print(struri)
        bubble = {
            "type": "bubble",
            "hero": {
                "type": "image",
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover",
                "url": type.rt_image
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "xs",
                "contents": [
                {
                    "type": "text",
                    "text": type.rt_name,
                    "wrap": True,
                    "weight": "bold",
                    "size": "xl",
                    "color": "#1A3852"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                    {
                        "type": "text",
                        "text": "$" + str(type.rt_price),
                        "wrap": True,
                        "weight": "bold",
                        "size": "xl",
                        "color": "#1A3852"
                    },
                    {
                        "type": "text",
                        "text": "限定" + str(type.rt_limit) + "人",
                        "wrap": True,
                        "weight": "bold",
                        "size": "md",
                        "color": "#1A3852",
                        "gravity": "center",
                        "align": "end"
                    }
                    ]
                },
                {
                    "type": "separator",
                    "margin": "sm"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "xl",
                    "contents": [
                    {
                        "type": "text",
                        "text": type.rt_description,
                        "wrap": True,
                        "weight": "bold",
                        "flex": 0,
                        "size": "md"
                    }
                    ]
                }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": [
                {
                    "type": "button",
                    "style": "primary",
                    "height": "sm",
                    "action": {
                        "type": "uri",
                        "label": "我要訂房",
                        "uri": "https://reurl.cc/O4aGl7"
                    },
                    "color": "#D5A07E"
                }]
            }
        }
        bubbles.append(bubble)
    print(bubbles)
    flex_message = FlexSendMessage(
        alt_text="房型選擇",
        contents={
            "type": "carousel",
            "contents": bubbles
        }
    )
    return flex_message

def list_all_activities():
    #抓取資料庫中所有週邊活動
    allactivities = Activities.objects.all()
    bubbles = []

    for activity  in allactivities:
        bubble = {
            "type": "bubble",
            "hero": {
                "type": "image",
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover",
                "url": activity.a_img,
                "action": {
                "type": "uri",
                "label": "活動網址",
                "uri": activity.a_url,
                }
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "xs",
                "contents": [
                {
                    "type": "text",
                    "text": activity.a_name,
                    "size": "xl",
                    "weight": "bold",
                    "wrap": True
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "margin": "md",
                    "contents": [
                    {
                        "type": "text",
                        "text": "活動日期",
                        "weight": "bold",
                        "align": "start",
                        "wrap": True,
                        "size": "md",
                        "flex": 0
                    },
                    {
                        "type": "text",
                        "text": activity.a_date,
                        "size": "sm",
                        "wrap": True,
                        "gravity": "center",
                        "offsetStart": "10px"
                    }
                    ]
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                    {
                        "type": "text",
                        "text": "活動地點",
                        "weight": "bold",
                        "align": "start",
                        "wrap": True,
                        "size": "md",
                        "flex": 0
                    },
                    {
                        "type": "text",
                        "text": activity.a_address,
                        "size": "sm",
                        "wrap": True,
                        "gravity": "center",
                        "offsetStart": "10px"
                    }
                    ],
                    "margin": "md"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                    {
                        "type": "text",
                        "text": "主辦單位",
                        "weight": "bold",
                        "align": "start",
                        "wrap": True,
                        "size": "md",
                        "flex": 0
                    },
                    {
                        "type": "text",
                        "text": activity.a_organizer,
                        "size": "sm",
                        "wrap": True,
                        "gravity": "center",
                        "offsetStart": "10px"
                    }
                    ],
                    "margin": "md"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                    {
                        "type": "text",
                        "text": "費用",
                        "weight": "bold",
                        "align": "start",
                        "wrap": True,
                        "size": "md",
                        "flex": 0
                    },
                    {
                        "type": "text",
                        "text": activity.a_price,
                        "size": "sm",
                        "wrap": True,
                        "gravity": "center",
                        "offsetStart": "43px"
                    }
                    ],
                    "margin": "md"
                }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                    "type": "message",
                    "label": "取得地圖",
                    "text": "GET MAP:" + activity.a_name,
                    }
                }
                ]
            }
        } 
        bubbles.append(bubble)

    flex_message = FlexSendMessage(
        alt_text="週邊活動",
        contents={
            "type": "carousel",
            "contents": bubbles
        }
    )
    return flex_message

def GetMapMessage(strLocationName):
    map = Activities.objects.filter(a_name=strLocationName).first()
    message = None

    if map is None:
        message = TextSendMessage(text = '抱歉系統錯誤暫時無法查到您所指定的地點...')
    else:
        if map.comments != None:
            x,y = map.comments.split(',') 
            message = LocationSendMessage(title=strLocationName, address=map.a_address if map.a_address is not None else strLocationName,
                        latitude= float(x), longitude= float(y))
        else:
            gmaps = googlemaps.Client(key=settings.GOOGLE_API)

            # Geocoding an address
            geocode_result = gmaps.geocode(map.Address)
            f_lat = float(geocode_result[0]['geometry']['location']['lat'])
            f_lng = float(geocode_result[0]['geometry']['location']['lng'])
            message = LocationSendMessage(title=strLocationName, address=map.Address if map.Address is not None else strLocationName,
                        latitude= f_lat, longitude= f_lng)

    return message

# endregion


# region 房間查詢Class

class EmptyRoomTypeHistogram:
    def __total_room_num(self):
        target_room_type = models.RoomType.objects.filter(rt_name=self.room_type_name).first()
        return len(models.Room.objects.filter(room_type=target_room_type))

    def __curr_booking_room_list(self):
        target_room_type = models.RoomType.objects.get(rt_name=self.room_type_name)
        target_rooms = models.Room.objects.filter(room_type=target_room_type)
        from_datetime = self.from_date.date_time()
        to_datetime = self.to_date.date_time()
        return models.BookingRoom.objects.filter(room__in=target_rooms, over_night_date__range=(self.from_date.date_time(), self.to_date.date_time()))

    def __init__(self, room_type, str_from_date='', str_to_date=''):
        self.limit_days = 100
        if str_from_date and not str_to_date:
            self.room_type_id = room_type.id
            self.room_type_name = room_type.rt_name
            self.from_date = MyDateTime(str_from_date)
            self.to_date = MyDateTime(str_from_date)

            self.histogram = 0
            self.histogram = self.__total_room_num()

            for curr_booking in self.__curr_booking_room_list():
                self.histogram -= 1
                if self.histogram < 0:
                    self.histogram = 0

        elif str_from_date and str_to_date:
            self.room_type_id = room_type.id
            self.room_type_name = room_type.rt_name
            self.from_date = MyDateTime(str_from_date)
            self.to_date = MyDateTime(str_to_date)

            self.curr_range_days = abs(self.from_date.comprise_between(self.to_date))
            if self.curr_range_days > self.limit_days:
                return
            #initial
            range_days = self.from_date.comprise_everyday(self.to_date)

            self.histogram = {}
            for everyday in range_days:
                self.histogram[everyday.year] = {}

            for everyday in range_days:
                self.histogram[everyday.year][everyday.month] = {}

            for everyday in range_days:
                self.histogram[everyday.year][everyday.month][everyday.day] = self.__total_room_num()

            #set value
            for curr_booking in self.__curr_booking_room_list():
                year  = curr_booking.over_night_date.year
                month = curr_booking.over_night_date.month
                day   = curr_booking.over_night_date.day

                if year in self.histogram and month in self.histogram[year] and day in self.histogram[year][month]:
                    self.histogram[year][month][day] -= 1
                    if self.histogram[year][month][day] < 0:
                       self.histogram[year][month][day] = 0

class BookingUnit:
    #room:yyyy_mm_dd:yyyy_mm_dd
    def __init__(self, str_room_from_data_to_data):
        print(str_room_from_data_to_data)
        self.roomtype_id, from_date, to_date = str_room_from_data_to_data.split(':')
        self.from_datetime = MyDateTime(from_date)
        print(self.from_datetime)
        self.to_datetime = MyDateTime(to_date)
        print(self.to_datetime)

    def total_day(self):
        return self.from_datetime.comprise_between(self.to_datetime)

    def every_night(self):
        return self.from_datetime.comprise_everyday(self.to_datetime)

# endregion


# region WebSite

def index(request):
    template = get_template('index.html')
    html = template.render(locals())
    return HttpResponse(html)

def booking(request, room_type):
    rt = RoomType.objects.filter(rt_name = room_type).first()
    rt = model_to_dict(rt)
    template = get_template('booking_step1.html')
    html = template.render(locals())
    return HttpResponse(html)
    # print(rt)
    # return render(request, 'booking_step1.html', rt)

def enhanced(request):
    template = get_template('enhanced.html')
    html = template.render(locals())
    return HttpResponse(html)

def query_room(request):
    print("查詢空房")
    today_date = request.GET.get('today', '')
    from_date = request.GET.get('from', '')
    to_date = request.GET.get('to', '')

    if today_date:
        histogram=[]
        for room_type in list(models.RoomType.objects.all()):
            histogram_unit = EmptyRoomTypeHistogram(room_type, today_date)
            histogram.append(histogram_unit)

        return render(request, 'BookingList1.html', locals())
    elif from_date and to_date:
        histogram = []
        roomTypes = models.RoomType.objects.all()
        for room_type in list(roomTypes):
            histogram_unit = EmptyRoomTypeHistogram(room_type, from_date, to_date)
            histogram.append(histogram_unit)
        return render(request,'BookingList2.html', locals())
    else:
        return render(request,'BookingList1.html', locals())



# endregion