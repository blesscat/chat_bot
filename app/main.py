import os
import random
import time
import requests
import subprocess
from flask import request, render_template, jsonify
from sqlalchemy.sql import func

from . import app, db, TOKEN, DEV_TOKEN
from .modules import db_models
from .modules import lots_pool
from .modules.parse_incoming import ParseIncoming

bless = 461302625
owen = 574164683
nordy = 558029648

banList = [owen, nordy]
# banList = []


def Test(incom):
    doc = 'https://blesscat.github.io/images/lots/A1.gif'
    data = {'chat_id': incom.chat_id, 'document': doc}
    Post('sendDocument', data)


def Draw():
    beauty = db_models.Beauty.query.order_by(func.random()).first()
    db.session.delete(beauty)
    db.session.commit()
    return beauty.url


def Post(method, data):
    HTTP = 'https://api.telegram.org/bot{}/{}'.format(TOKEN, method)
    # HTTP = 'https://api.telegram.org/bot{}/{}'.format(DEV_TOKEN, method)
    r = requests.post(HTTP, data=data)
    print(r.text)
    return r.json()


def Ocr(incom):
    base64 = incom.text[4:]
    subprocess.call(['bash', 'ocr.sh', base64])

    with open(os.path.join('./app/modules/ocr/', 'output.txt'), "r") as f:
        res = f.read()

    data = {
        'chat_id': incom.chat_id,
        'reply_to_message_id': incom.message_id,
        'text': res
    }
    
    Post('sendMessage', data)

def DelMsg(incom):
    data = {
        'chat_id': incom.chat_id,
        'message_id': incom.message_id,
    }
    Post('deleteMessage', data)     


def postLunch(incom, launch):
    choice = random.choice(launch)

    data = {
        'chat_id': incom.chat_id,
        'reply_to_message_id': incom.message_id,
        'text': choice.name
    }
    send = Post('sendMessage', data)

    data = {
        'chat_id': incom.chat_id,
        'latitude': choice.latitude,
        'longitude': choice.longitude,
        'reply_to_message_id': send['result']['message_id']
    }
    Post('sendLocation', data)


def drawLots(incom):
    choice = random.choice(lots_pool.lots_pool)
    url = 'https://blesscat.github.io/images/lots/{}C.gif'.format(choice)
    data = {
        'chat_id': incom.chat_id, 
        'text': '恭迎持蔥初音⎝༼ ◕д ◕ ༽⎠ 渡世靈顯四方⎝༼ ◕д ◕ ༽⎠',
        'reply_to_message_id': incom.message_id
    }
    Post('sendMessage', data)

    time.sleep(1)

    udata = {
        'chat_id': incom.chat_id, 
        'reply_to_message_id': incom.message_id,
        'video': url
    }

    # Post('sendDocument', udata)
    Post('sendVideo', udata)


def postDraw(incom):
    url = Draw()
    data = {
        'chat_id': incom.chat_id, 
        'reply_to_message_id': incom.message_id
    }

    if url.endswith('.gif'):
        data['document'] = url
        Post('sendDocument', data)
    else:
        data['photo'] = url
        Post('sendPhoto', data)


def sendReport(data):
    print(data.from_id, blessId)
    if data.from_id == blessId:
        doc = 'BQADBQADTAADydmBVO_IRRXZzwrMAg'
        data = {'chat_id': data.chat_id, 'document': doc}
        Post('sendDocument', data)
    else:
        data = {'chat_id': data.chat_id, 'text': '你是誰？'}
        Post('sendMessage', data)


def sendDocument(data):
    doc = 'https://ws2.sinaimg.cn/large/006tNbRwgy1fxwsx3i81sg30640621kz.gif'
    data = {'chat_id': data.chat_id, 'document': doc}
    Post('sendDocument', data)


# telegram 創樂前端小妹
@app.route("/637218572:AAGmOxtvixXYH2KIL9cLA79Rt6dTMCYOjmc",
           methods=['GET', 'POST'])
def telegram():
    print(request.get_json())
    incoming = ParseIncoming(request.get_json())

    if incoming.isLunch:
        launch = db_models.Launch.query.all()
        postLunch(incoming, launch)
    elif incoming.gqLunch:
        launch = db_models.GqLaunch.query.all()
        postLunch(incoming, launch)
    elif incoming.isDraw:
        postDraw(incoming)
    elif incoming.isJavaCat:
        sendDocument(incoming)
    elif incoming.isReport:
        sendReport(incoming)
    elif incoming.isTeaTime:
        data = {
            'chat_id': incoming.chat_id,
            'reply_to_message_id': incoming.message_id,
            'text': '歐文'
        }
        Post('sendMessage', data)
        
    elif incoming.isDrawLots:
        drawLots(incoming)
    elif incoming.isOCR:
        Ocr(incoming)
    elif incoming.from_id in banList:
        if incoming.isSticker or incoming.isDoc:
            DelMsg(incoming)
    # elif incoming.isTest:
    #     Test(incoming)

    return ''


@app.route("/ocr", methods=['POST'])
def useOCR():
    img = request.get_json()['img']
    if not img:
        return 'no data'

    subprocess.call(['bash', 'ocr.sh', img])
    with open(os.path.join('./app/modules/ocr/', 'output.txt'), "r") as f:
        res = f.read()
    
    return res


@app.route("/setWebhook", methods=['GET'])
def setWebhook():
    return app.send_static_file('setWebhook.html')


@app.route("/gqLaunch", methods=['GET', 'POST'])
def gqLaunch():
    if request.method == 'GET':
        launch = db_models.GqLaunch.query.all()
        pool = [i.to_json() for i in launch]
        return render_template('setLaunch.html', my_list=pool, address='gqLaunch')

    elif request.method == 'POST':
        data = request.get_json()
        launch = db_models.GqLaunch(
            data['name'], data['latitude'], data['longitude'])
        db.session.add(launch)
        db.session.commit()

        return jsonify({'res': 'success'})

@app.route("/setLaunch", methods=['GET', 'POST'])
def setLaunch():
    if request.method == 'GET':
        launch = db_models.Launch.query.all()
        pool = [i.to_json() for i in launch]
        return render_template('setLaunch.html', my_list=pool, address='setLaunch')

    elif request.method == 'POST':
        data = request.get_json()
        launch = db_models.Launch(
            data['name'], data['latitude'], data['longitude'])
        db.session.add(launch)
        db.session.commit()

        return jsonify({'res': 'success'})
