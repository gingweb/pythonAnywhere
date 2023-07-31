
# A very simple Flask Hello World app for you to get started with...

from flask import Flask
from flask import request
import json
import time
import requests

from flask import abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextSendMessage, QuickReplyButton, MessageAction, QuickReply


from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)

app = Flask(__name__)

def searchdataset1(name, data_summary):
    return [element for element in data_summary if element['goodstype'] == name]

def mapgoodskey(goods):
    result = ''
    if ( goods == 'ข้าวเปลือก' ):
        result = 'paddy'
    elif ( goods == 'ข้าว'  or goods == 'ขาว'):
        result = 'rice'
    elif ( goods == 'อ้อย' ):
        result = 'sugarcane'
    elif ( goods == 'น้ำตาลทราย' ):
        result = 'sugar'
    elif ( goods == 'กากน้ำตาล' ):
        result = 'morash'
    elif ( goods == 'อาหารสัตว์' ):
        result = 'animalfeed'
    elif ( goods == 'ข้าวโพด' ):
        result = 'corn'
    elif ( goods == 'ผลิตภัณฑ์มันสำปะหลัง' ):
        result = 'tapioca'
    elif ( goods == 'ดิน' ):
        result = 'soil'
    elif ( goods == 'หิน' ):
        result = 'rock'
    elif ( goods == 'ทราย' ):
        result = 'sand'
    elif ( goods == 'ถ่านหิน' ):
        result = 'coal'
    elif ( goods == 'แร่ยิบซัม' ):
        result = 'gypsum'
    elif ( goods == 'ปูนซิเมนต์' ):
        result = 'cementplant'
    elif ( goods == 'คอนกรีตผสมเสร็จ' ):
        result = 'liqcement'
    elif ( goods == 'น้ำมันดิบ' ):
        result = 'crudeoil'
    elif ( goods == 'น้ำมันสำเร็จรูป' ):
        result = 'petrol'
    elif ( goods == 'ก๊าซปิโตรเลียม' ):
        result = 'lpg'
    elif ( goods == 'ก๊าซธรรมชาติ' ):
        result = 'cng'
    elif ( goods == 'กระดาษและผลิตภัณฑ์กระดาษ' ):
        result = 'paper'
    elif ( goods == 'รถยนต์' ):
        result = 'car'
    return result

def mapprovince(text_search):
    url = "https://dev.bigdata-report.otp.transcode.co.th/ext-api/get_province_amp_tam.php"
    d = {   'token': 'cf066aaed5c63a21998dd9f7abfd854e83b7a89d79f5f0b09a529a294dcc3f57',
            'text_search': text_search
            }
    response = requests.post(url, data=d)
    resp_dict = response.json()
    #print(resp_dict)

    provname = resp_dict[0].get('provname')
    provcode = resp_dict[0].get('provcode')
    amphoename = resp_dict[0].get('amphoename')
    amphoecode = resp_dict[0].get('amphoecode')
    tambonname = resp_dict[0].get('tambonname')
    tamboncode = resp_dict[0].get('tamboncode')
    id = resp_dict[0].get('id')

    result =    {
                    "provname": provname,
                    "provcode": provcode,
                    "amphoename": amphoename,
                    "amphoecode": amphoecode,
                    "tambonname": tambonname,
                    "tamboncode": tamboncode,
                    "id": id
                }
    return result

# ข้อมูลของ Channel ที่ได้จาก LINE Developer Console
CHANNEL_ACCESS_TOKEN = "VG2PaYC529yhNFOhjFkaFUlrarnFUkJ2ADP0lcvUMsu63st8XxfD/npt5nF9wKXgQoVdAuD9BR1mk1Q4tRr7e14X6ZOObLGKL7XP9B5O0EUyDhx4GZbxc+kufvbNm7mHfRwecO6Vx3RW5H6JInCu5wdB04t89/1O/w1cDnyilFU="
CHANNEL_SECRET = "826d6d14f3f30b49a7f4df115d9ef53d"

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

@app.route("/linewebhook", methods=["POST"])
def linewebhook():
    # รับข้อมูลที่ส่งมาจาก LINE server
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)

    try:
        # ตรวจสอบความถูกต้องของ signature
        print("start")
        handler.handle(body, signature)
        print("end try")

    except InvalidSignatureError:
        abort(400)

    return "OK"


@handler.add(MessageEvent, message=TextSendMessage)
#@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # ตรวจสอบว่าผู้ใช้ได้เลือก Quick Reply ประเภท Location หรือไม่
    if event.message.quick_reply and event.message.quick_reply['type'] == 'location':
        print("if yes location")

        # ดึงค่า latitude และ longitude ที่ผู้ใช้เลือกจาก Quick Reply ประเภท Location
        latitude = event.message.latitude
        longitude = event.message.longitude

        # ทำสิ่งที่คุณต้องการด้วยข้อมูล latitude และ longitude ที่ได้รับมา เช่น ค้นหาสถานที่ใกล้เคียง หรือแสดงผลแผนที่

        # ตัวอย่างการตอบกลับด้วยข้อความ
        reply_text = f"คุณเลือกตำแหน่งที่อยู่ที่ Latitude: {latitude}, Longitude: {longitude}"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))

    else:
        print("else not location")
        # ตัวอย่างการส่ง Quick Reply ประเภท Location ให้ผู้ใช้เลือก
        location_quick_reply = QuickReply(
            items=[
                QuickReplyButton(action=MessageAction(label="ส่งตำแหน่งที่อยู่", text="ส่งตำแหน่งที่อยู่", type="location"))
            ]
        )
        reply_text = "กรุณาเลือกตำแหน่งที่อยู่ด้วยค่ะ"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text, quick_reply=location_quick_reply))


# Default handler สำหรับเหตุการณ์ที่ไม่ได้รับการจัดการใน handler ที่กำหนดไว้
@handler.default()
def default(event):
    # ตอบกลับข้อความหากไม่มี handler ที่ตรงกับเหตุการณ์ที่เกิดขึ้น

    #ใช้งาน request ได้เลย
    print ( request)
    print (request.headers)
    req_str = request.get_json() #dictionary
    print ( req_str)

    print ("---event---")
    print (event)
    print ( type(event))

    req_body_json = ""

    if hasattr(event, 'postback') and hasattr(event.postback, 'data'):
        if (event.postback.data == "selected_date"):

            req_body_json = request.get_data(as_text=True)
            req_body = json.loads(req_body_json)  # แปลง JSON string เป็น Python Object

            print ("pre-req_body")
            print (req_body)

            req_to_dialog =  {}
             # เข้าถึง attribute ใน Python Object ได้และปรับปรุงค่าตามที่ต้องการ
            if 'events' in req_body and len(req_body['events']) > 0:
                eventdate = event.postback.params["date"]

                #req_to_dialog =    {
                #   "deliveryContext":req_body['events'][0]['deliveryContext'],
                #   "message":{
                #      "id": "465622370497855490",
                #      "text":"DATE : " + str(eventdate),
                #      "type":"text"
                #   },
                #   "mode":req_body['events'][0]['mode'],
                #   "replyToken":req_body['events'][0]['replyToken'],
                #   "source":req_body['events'][0]['source'],
                #   "timestamp":req_body['events'][0]['timestamp'],
                #   "type":"message",
                #   "webhookEventId":req_body['events'][0]['webhookEventId']
                #}

                #new_event = [{"type": "text" , "text" : "DATE : " + str(eventdate)}]
                #req_body['events'][0]['message']['type'] = 'text'
                #req_body['events'][0]['message']['text'] = "DATE : " + str(eventdate)

                #req_body["events"] = [{"type": "text" , "text" : "DATE : " + str(eventdate)}]

            req_to_dialog =     {
                               "events": [{
                                    "type":"message",
                                    "message":{
                                          "id": "465622370497855491",
                                          "text":"DATE : 2021-07-01",
                                          "type":"text"
                                    },
                                    "webhookEventId":"01H68RK9B35J29PCCVX2CSHQ93",
                                    "deliveryContext":{
                                          "isRedelivery":"false"
                                       },
                                    "timestamp":1690363863996,
                                    "source":{
                                          "type":"user",
                                          "userId":"Uc97188c81890dc69e1914ca6eb0d7582"
                                       },
                                    "replyToken":"f75742d16824498b9f807a22d54000ca",
                                    "mode":"active"
                                    }],
                                "destination": "U79f910f9fc119e983be269f5e11942ab"
                                }


            # แปลงกลับเป็น JSON string อีกครั้งก่อนส่ง
            req_body_json_updated = json.dumps(req_to_dialog)

            print ("after-req_body_json_updated")
            print (req_body_json_updated)

            #ปลง Location Message ไปเป็น Text Message ก่อน โดยแปลงให้อยู่ในรูปแบบที่ dialogflow ตั้ง training phase ไว้

            #ส่งค่าให้ dialogflow
            dialogflow_url = "https://dialogflow.cloud.google.com/v1/integrations/line/webhook/d2688abb-d35d-44b9-a843-f3b82f0f05fc"
            print (request.headers["host"])

            # สร้าง object ใหม่ที่มี headers ใหม่โดยกำหนดค่า host ใหม่
            req_headers = {
                "host": "dialogflow.cloud.google.com",
                "user-agent": request.headers.get("user-agent"),
                "x-forwarded-host": "dialogflow.cloud.google.com",
                "Content-Type": request.headers.get("Content-Type"),
                "Content-Length": request.headers.get("Content-Length"),
                "x-forwarded-for": request.headers.get("x-forwarded-for"),
                "x-forwarded-proto": request.headers.get("x-forwarded-proto"),
                "x-line-signature": request.headers.get("x-line-signature"),
                "accept-encoding": request.headers.get("accept-encoding")
            }

            print (req_headers)
            # ทำ HTTP POST request ไปยัง Dialogflow
            response = requests.post(dialogflow_url, headers=req_headers , data=req_body_json_updated.encode('utf-8'))

    elif (event.message.type == "image"):
        img_id = event.message.id


    elif (event.message.type == "location"):
        address = event.message.address
        location_id = event.message.id
        latitude = event.message.latitude
        longitude = event.message.longitude

        print ("pre-req_body_json")
        print (req_body_json)

        req_body_json = request.get_data(as_text=True)
        req_body = json.loads(req_body_json)  # แปลง JSON string เป็น Python Object

        # เข้าถึง attribute ใน Python Object ได้และปรับปรุงค่าตามที่ต้องการ
        if 'events' in req_body and len(req_body['events']) > 0:
            req_body['events'][0]['message']['type'] = 'text'
            req_body['events'][0]['message']['text'] = "LAT:"+str(latitude)+",LNG:"+str(longitude)

        # แปลงกลับเป็น JSON string อีกครั้งก่อนส่ง
        req_body_json_updated = json.dumps(req_body)

        print ("after-location-req_body_json_updated")
        print (req_body_json_updated)

        #ปลง Location Message ไปเป็น Text Message ก่อน โดยแปลงให้อยู่ในรูปแบบที่ dialogflow ตั้ง training phase ไว้

        #ส่งค่าให้ dialogflow
        dialogflow_url = "https://dialogflow.cloud.google.com/v1/integrations/line/webhook/d2688abb-d35d-44b9-a843-f3b82f0f05fc"
        print (request.headers["host"])

        # สร้าง object ใหม่ที่มี headers ใหม่โดยกำหนดค่า host ใหม่
        req_headers = {
            "host": "dialogflow.cloud.google.com",
            "user-agent": request.headers.get("user-agent"),
            "x-forwarded-host": "dialogflow.cloud.google.com",
            "Content-Type": request.headers.get("Content-Type"),
            "Content-Length": request.headers.get("Content-Length"),
            "x-forwarded-for": request.headers.get("x-forwarded-for"),
            "x-forwarded-proto": request.headers.get("x-forwarded-proto"),
            "x-line-signature": request.headers.get("x-line-signature"),
            "accept-encoding": request.headers.get("accept-encoding")
        }

        print (req_headers)
        # ทำ HTTP POST request ไปยัง Dialogflow
        response = requests.post(dialogflow_url, headers=req_headers , data=req_body_json_updated.encode('utf-8'))

        #reply_text = "ส่งไป dialogflow แล้วค่ะ"
        #line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))


    else:
        #elif (event.message.type == "text"):
        user_message = event.message.text

        req_body_json = request.get_data(as_text=True)
        print ("req_body_json")
        print (req_body_json)

        #ส่งค่าให้ dialogflow
        dialogflow_url = "https://dialogflow.cloud.google.com/v1/integrations/line/webhook/d2688abb-d35d-44b9-a843-f3b82f0f05fc"
        print (request.headers["host"])

        # สร้าง object ใหม่ที่มี headers ใหม่โดยกำหนดค่า host ใหม่
        req_headers = {
            "host": "dialogflow.cloud.google.com",
            "user-agent": request.headers.get("user-agent"),
            "x-forwarded-host": "dialogflow.cloud.google.com",
            "Content-Type": request.headers.get("Content-Type"),
            "Content-Length": request.headers.get("Content-Length"),
            "x-forwarded-for": request.headers.get("x-forwarded-for"),
            "x-forwarded-proto": request.headers.get("x-forwarded-proto"),
            "x-line-signature": request.headers.get("x-line-signature"),
            "accept-encoding": request.headers.get("accept-encoding")
        }

        print (req_headers)
        # ทำ HTTP POST request ไปยัง Dialogflow
        response = requests.post(dialogflow_url, headers=req_headers , data=req_body_json.encode('utf-8'))

        #reply_text = "ส่งไป dialogflow แล้วค่ะ"
        #line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))

@app.route('/dialogflow', methods = ['POST'])
def dialogflow():
    content_type = request.headers.get('Content-Type')

    if (content_type == 'application/json'):

        req_str = request.get_json() #dictionary

        intent_name = req_str.get('queryResult',{}).get('intent',{}).get('name',{})
        #['queryResult']["intent"]["name"]
        print (intent_name)

        jsonstr = 0


        if (intent_name == "projects/red-queen-v-1-vtgc/agent/intents/d7e90c6b-48b9-4a62-b3dc-625df6867569"):
            #ถามสภาพอากาศ
            print ('intent สภาพอากาศ')
            jsonstr = {
                          "fulfillmentMessages": [
                            {
                              "text": {
                                "text": [
                                  "ถามสินค้า response from Python Anywhere"
                                ]
                              }
                            }
                          ]
                        }

        elif (intent_name == "projects/red-queen-v-1-vtgc/agent/intents/2a513b9d-6c65-4c58-8f1f-10c8b113b9e2"):
            #ถามทาง
            print ('intent ถามทาง')
            jsonstr = {
                          "fulfillmentMessages": [
                            {
                              "text": {
                                "text": [
                                  "ถามสินค้า response from Python Anywhere"
                                ]
                              }
                            }
                          ]
                        }


        elif (intent_name == "projects/red-queen-v-1-vtgc/agent/intents/6dca66aa-da59-40bc-adcf-4a62e176b2d4" or intent_name == "projects/red-queen-v-1-vtgc/agent/intents/83ba14e5-a909-4b3f-b87a-0b9895279b71") :

            #ถามสินค้า
            #DialogFlow การขนส่งสินค้า "$any_goods" จาก $o_goods ไปยัง $d_goods ในปี $year_goods เดือน $month_goods
            print ('intent สินค้า')

            #ปั้น json
            #ปั้น json -  เดือน ปี
            year = req_str.get('queryResult',{}).get('outputContexts',{})[0].get('parameters',{}).get('year_goods.original',)
            month = req_str.get('queryResult',{}).get('parameters',{}).get('month_goods')

            #ปั้น json -ประเภท
            goods = req_str.get('queryResult',{}).get('parameters',{}).get('any_goods')
            print(goods)
            goods_key = mapgoodskey(goods)

            #ปั้น json - จังหวัดต้นทาง
            ori_txt = req_str.get('queryResult',{}).get('parameters',{}).get('o_goods')
            ori_dict = mapprovince(ori_txt)

            #ปั้น json - จังหวัดปลายทาง
            dest_txt = req_str.get('queryResult',{}).get('parameters',{}).get('d_goods')
            dest_dict = mapprovince(dest_txt)

            print(month)
            print(year)
            print(goods_key)
            print(ori_dict.get('provcode'))
            print(dest_dict.get('provcode'))

            #post json
            #headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            #response = requests.post(url, data=d, headers=headers)

            url = "https://dev.bigdata-report.otp.transcode.co.th/ext-api/truck_goods_1.php"
            d = {    'token': 'cf066aaed5c63a21998dd9f7abfd854e83b7a89d79f5f0b09a529a294dcc3f57',
                        'month': month,
                        'year': year,
                        'goods_type': goods_key,
                        'o_province': ori_dict.get('provcode'),
                        'd_province': dest_dict.get('provcode')
                    }
            print(d)

            response = requests.post(url, data=d)
            resp_dict = response.json()

            #ini ค่าจาก otp

            od_goodstype = "ไม่พบข้อมูล"
            od_tambonO = "-"
            od_amphoeO = "-"
            od_tambonD = "-"
            od_amphoeD = "-"
            od_year = "-"
            od_month = "-"
            od_tripspermonth = "-"
            od_tonpermonth = "-"
            od_avgdistance = "-"
            od_avgtraveltime = "-"
            od_avgspeed = "-"

            otp_goodstype = "ไม่พบข้อมูล"
            otp_year = "-"
            otp_month = "-"
            otp_tripspermonth = "-"
            otp_tonpermonth = "-"
            otp_avgdistance = "-"
            otp_avgtravelt = "-"
            otp_avgspeed = "-"
            otp_tonskm = "-"
            otp_vkt = "-"
            otp_vht = "-"
            otp_cost = "-"

            tblist = []

            #แกะ json

            if (resp_dict.get('data_od',{}).get('status') != 101):
                res_od = resp_dict.get('data_od',{}).get('results',{}).get('data_set1')
                print(res_od)

                i = 0
                for tb_detail in res_od :
                    od_goodstype = str(tb_detail.get('goodstype'))
                    od_year = str(tb_detail.get('year'))
                    od_month = str(tb_detail.get('month'))

                    od_tambonO = str(tb_detail.get('tambonO'))
                    od_amphoeO = str(tb_detail.get('amphoeO'))

                    od_tambonD = str(tb_detail.get('tambonD'))
                    od_amphoeD = str(tb_detail.get('amphoeD'))

                    od_tripspermonth = str(tb_detail.get('tripspermonth'))
                    od_tonpermonth = str(tb_detail.get('tonspermonth'))
                    od_avgdistance = str(tb_detail.get('avgdistance'))
                    od_avgtraveltime = str(tb_detail.get('avgtraveltime'))
                    od_avgspeed = str(tb_detail.get('avgspeed'))

                    tbjson = {
                                      "text": {
                                        "text": [
                                        "สินค้า:  " + od_goodstype
                                        +"\nเดือน:  " + od_month +" ปี:  " + od_year
                                        +"\n"
                                        +"\nจาก ตำบล" + od_tambonO +" อำเภอ" + od_amphoeO + " ไปยัง ตำบล" + od_tambonD +" อำเภอ" + od_amphoeD
                                        +"\nจำนวนเที่ยวต่อเดือน(เที่ยว):  " + od_tripspermonth
                                        +"\nปริมาณ(ตัน/เดือน):  "   + od_tonpermonth
                                        +"\nระยะทางเฉลี่ย(กม.):  " + od_avgdistance
                                        +"\nระยะเวลาเฉลี่ย(นาที):  " + od_avgtraveltime
                                        +"\nความเร็วเฉลี่ย(กม/ชม):  " + od_avgspeed
                                         ]
                                      }
                             }
                    print(tbjson)
                    print(type(tbjson))

                    print(i)
                    tblist.append(tbjson)
                    i=i+1


            else:
                tbjson = {
                                      "text": {
                                        "text": [
                                        "- ไม่พบข้อมูล -"
                                         ]
                                      }
                             }
                print(tbjson)
                print(type(tbjson))
                tblist.append(tbjson)

            #Line
            print(tblist)
            jsonstr =    {
                              "fulfillmentMessages": tblist
                            }



            #if (resp_dict.get('data_summary',{}).get('status') != 101):
            #    data_summary = resp_dict.get('data_summary',{}).get('results',{}).get('data_set1')

            #    res = searchdataset1(goods_key, data_summary)
                #print("data_summary")
                #print(type(res))        #<class 'list'>
            #    print(res)
            #    otp_goodstype = str(res[0].get('goodstype'))
            #    otp_year = str(res[0].get('year'))
            #    otp_month = str(res[0].get('month'))
            #    otp_tripspermonth = str(res[0].get('tripspermonth'))
            #    otp_tonpermonth = str(res[0].get('tonspermonth'))
            #    otp_avgdistance = str(res[0].get('avgdistance'))
            #    otp_avgtraveltime = str(res[0].get('avgtraveltime'))
            #    otp_avgspeed = str(res[0].get('avgspeed'))
            #    otp_tonskm = str(res[0].get('tonskm'))
            #    otp_vkt = str(res[0].get('vkt'))
            #    otp_vht = str(res[0].get('vht'))
            #    otp_cost = str(res[0].get('cost'))

            #Line
            #jsonstr = {
            #                  "fulfillmentMessages": [
            #                    {
            #                      "text": {
            #                        "text": [
            #                        "สินค้า:  " + otp_goodstype
            #                        +"\nเดือน:  " + otp_month +" ปี:  " + otp_year
            #                        +"\nจำนวนเที่ยวต่อเดือน(เที่ยว):  " + otp_tripspermonth
            #                        +"\nปริมาณ(ตัน/เดือน):  "  + otp_tonpermonth
            #                        +"\nระยะทางเฉลี่ย(กม.):  " + otp_avgdistance
            #                        +"\nระยะเวลาเฉลี่ย(นาที):  " + otp_avgtraveltime
            #                        +"\nความเร็วเฉลี่ย(กม/ชม):  " + otp_avgspeed
            #                        +"\nปริมาณการขนส่ง(คัน-กม.):  " + otp_tonskm
            #                        +"\nระยะการเดินทางรวม(คัน-กม.):  " + otp_vkt
            #                        +"\nระยะเวลาเดินทางรวม(คัน-ชม.):  " + otp_vht
            #                        +"\nค่าใช้จ่ายในการขนส่ง(บาท):  " + otp_cost
            #                         ]
            #                      }
            #                    }
            #                  ]
            #                }

            #แกะ json - วน loop
            #data_summary.results.data_ste1[].
            #ชนิดสินค้า                     goodstype
            #จำนวนเที่ยวต่อเดือน (เที่ยว        tripspermonth
            #ปริมาณ(ตัน/เดือน)              tonpermonth
            #ระยะทางเฉลี่ย   (กม.)          avgdistance
            #ระยะเวลาเฉลี่ย  (นาที)         avgtraveltime
            #ความเร็วเฉลี่ย (กม/ชม)         avgspeed
            #ปริมาณการขนส่ง (คัน-กม.)       tonskm
            #ระยะการเดินทางรวม   (คัน-กม.)  vkt
            #ระยะเวลาเดินทางรวม (คัน-ชม.)   vht
            #ค่าใช้จ่ายในการขนส่ง (บาท)         cost



            #ตอบ dialog flow

            #สร้างการ์ดไลน์สวยๆ

        elif (intent_name == "projects/red-queen-v-1-vtgc/agent/intents/1bb39eae-cfac-46a2-95df-0151f3ca9a19"):
            #แจ้งเหตุ
            print ('intent แจ้งเหตุ')
            print (req_str)
            jsonstr = {
                          "fulfillmentMessages": [
                            {
                              "text": {
                                "text": [
                                  req_str
                                ]
                              }
                            }
                          ]
                        }

        elif (intent_name == "projects/red-queen-v-1-vtgc/agent/intents/6ab548e4-abe9-4725-a306-5d21d24dbdd9"):
            #แจ้งเหต> สถานที่เกิดเหตุ
            print ('intent แจ้งเหตุ> สถานที่เกิดเหตุ')
            print (req_str)

            jsonstr = {
                          "fulfillmentMessages": [
                            {
                              "text": {
                                "text": [
                                  req_str
                                ]
                              }
                            }
                          ]
                        }

            #location
            # ตรวจสอบว่ามีค่าพิกัดที่ส่งมาจาก Dialogflow หรือไม่
            #if "queryResult" in req_str and "parameters" in req_str["queryResult"]:
            #    parameters = req_str["queryResult"]["parameters"]
            #    location = parameters["location"]

                # ทำสิ่งที่คุณต้องการด้วยค่า location ที่ได้รับมาจาก Dialogflow

                # ตัวอย่างการตอบกลับ Dialogflow ด้วยข้อความ
            #    fulfillment_text = f"คุณเลือก Location: {location['latitude']}, {location['longitude']}"
            #    response = {"fulfillmentText": fulfillment_text}
            #    return jsonify(response)
            #else:
            #    return jsonify({})

        else:

            jsonstr = {
                          "fulfillmentMessages": [
                            {
                              "text": {
                                "text": [
                                  "Case 0"
                                ]
                              }
                            }
                          ]
                        }

        jsonobj = jsonstr
        return jsonobj
    else:
        return 'Content-Type not supported!'



@app.route('/dialogflowtext', methods = ['POST'])
def dialogflowtext():
    content_type = request.headers.get('Content-Type')

    if (content_type == 'application/json'):

        req_str = request.get_json() #dictionary
        req_dict = json.dumps(req_str)

        intent_name = req_str.get('queryResult',{}).get('intent')  #['queryResult']["intent"]["name"]
        print (intent_name)

        jsonstr = 0

        if (intent_name == "projects/red-queen-v-1-vtgc/agent/intents/d7e90c6b-48b9-4a62-b3dc-625df6867569"):
            #ถามสภาพอากาศ
            print ('intent สภาพอากาศ')
            jsonstr = '''{
                          "fulfillmentMessages": [
                            {
                              "text": {
                                "text": [
                                  "ถามสภาพอากาศ response from Python Anywhere"
                                ]
                              }
                            }
                          ]
                        }'''
        elif (intent_name == "projects/red-queen-v-1-vtgc/agent/intents/2a513b9d-6c65-4c58-8f1f-10c8b113b9e2"):
            #ถามทาง
            print ('intent ถามทาง')
            jsonstr = '''{
                          "fulfillmentMessages": [
                            {
                              "card": {
                                "title": "ถามทาง",
                                "subtitle": "ทางไหนดี",
                                "imageUri": "https://cdn-icons-png.flaticon.com/512/854/854894.png",
                                "buttons": [
                                  {
                                    "text": "Navigator",
                                    "postback": "https://www.google.com/maps/dir/Transcode+Company+Thailand+Srivara+Road,+Phlabphla,+Wang+Thonglang,+Bangkok/ICONSIAM+PARK,+Khlong+Ton+Sai,+Khlong+San,+Bangkok/@13.735176,100.51231,13z/data=!3m1!4b1!4m14!4m13!1m5!1m1!1s0x30e29e0e33b5e4f3:0xc16c6d8ce49947ea!2m2!1d100.6053904!2d13.7667193!1m5!1m1!1s0x30e299e56e16167f:0xebb3fed7ec191c18!2m2!1d100.5110987!2d13.7264633!3e0?entry=ttu"
                                  }
                                ]
                              }
                            }
                          ]
                        }'''

        elif (intent_name == "projects/red-queen-v-1-vtgc/agent/intents/6dca66aa-da59-40bc-adcf-4a62e176b2d4" or intent_name == "projects/red-queen-v-1-vtgc/agent/intents/83ba14e5-a909-4b3f-b87a-0b9895279b71"):

            #ถามสินค้า
            print ('intent ถามสินค้า')
            jsonstr = '''{
                          "fulfillmentMessages": [
                            {
                              "text": {
                                "text": [
                                  "ถามสินค้า response from Python Anywhere"
                                ]
                              }
                            }
                          ]
                        }'''

        else:

            jsonstr = '''{
                          "fulfillmentMessages": [
                            {
                              "text": {
                                "text": [
                                  "Case 0"
                                ]
                              }
                            }
                          ]
                        }'''


        jsonobj = json.loads(jsonstr)
        return jsonobj
    else:
        return 'Content-Type not supported!'

@app.route('/logrequest', methods = ['POST'])
def logrequest():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        jsonstr = request.get_json()
        print(jsonstr)
        return 'server loged, visit https://www.pythonanywhere.com/'
    else:
        return 'Content-Type not supported!'

@app.route('/sayhi', methods = ['POST'])
def sayhi():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        request_json = request.get_json()
        name = request_json['name']
        return 'hello, '+ name
    else:
        return 'Content-Type not supported!'

@app.route('/textcount', methods = ['GET', 'POST'])
def handle_request():
    text = str(request.args.get('input')) # Requests the ?input= a
    character_count = len(text)

    data_set = {'input': text , 'timestamp':time.time(), 'character_count':character_count }
    json_dump = json.dumps(data_set)
    return json_dump

@app.route('/hello')
def hello_world():
    return 'Hello from Flask!'

