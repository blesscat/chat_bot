import os
import re
import random
import time
import requests
import subprocess
from flask import request, render_template, jsonify
from sqlalchemy.sql import func

from . import app, db, TOKEN, DEV_TOKEN
from .modules import db_models
from .modules import lots_pool
from .modules import tg_group
from .modules.parse_incoming import ParseIncoming

from .modules.redmine_webhook_parser import RedmineWebhookParser

from .modules import redmine
from .modules import redmine_keys

bless = 461302625

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

def isBanned(incom):
    banned = db_models.Ban.query.filter_by(
        chat_id=incom.chat_id,
        user_id=incom.from_id
    ).all()
    return bool(banned)

def unbanUser(incom):
    if incom.from_id != bless: return
    if not incom.reply_from_id: return
    banID = incom.reply_from_id
    banned = db_models.Ban.query.filter_by(
        chat_id=incom.chat_id,
        user_id=incom.reply_from_id
    ).all()

    if banned:
        db.session.delete(banned[0])
        db.session.commit()
        text = '{}已放出'.format(incom.reply_from_name)
    else:
        text = '{}並沒有水桶，要浸嗎？'.format(incom.reply_from_name)

    data = {
        'chat_id': incom.chat_id,
        'reply_to_message_id': incom.message_id,
        'text': text
    }
    
    Post('sendMessage', data)

def banUser(incom):
    if incom.from_id != bless: return
    if not incom.reply_from_id: return
    banID = incom.reply_from_id
    banned = db_models.Ban.query.filter_by(
        chat_id=incom.chat_id,
        user_id=incom.reply_from_id
    ).all()

    if banned:
        text = '{}早就水桶了'.format(incom.reply_from_name)
    else:
        ban = db_models.Ban(
            chat_id=incom.chat_id,
            user_id=incom.reply_from_id
        )
        db.session.add(ban)
        db.session.commit()

        text = '{}已ban貼圖'.format(incom.reply_from_name)

    data = {
        'chat_id': incom.chat_id,
        'reply_to_message_id': incom.message_id,
        'text': text
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
    elif incoming.isBan:
        banUser(incoming)
    elif incoming.isUnban:
        unbanUser(incoming)

    elif incoming.isSticker or incoming.isDoc:
        if isBanned(incoming):
            DelMsg(incoming)
    # elif incoming.isTest:
    #     Test(incoming)

    return jsonify({'res': 'success'})


@app.route("/message", methods=['POST'])
def message():
    incom = request.get_json()
    print('chat_name')
    
    if incom:
        if incom['chat_name']:
            chat_id = tg_group.name[incom['chat_name']]
        else :
            chat_id = incom['chat_id']
        data = {
            'chat_id': chat_id,
            'text': incom['text']
        } 
    else:
        if request.form.get('chat_name'):
            chat_id = tg_group.name[request.form.get('chat_name')]
        else :
            chat_id = request.form.get('chat_id')
        data = {
            'chat_id': chat_id,
            'text': request.form.get('text')
        } 

    Post('sendMessage', data)
    return jsonify({'res': 'success'})


@app.route("/redmineReceiver", methods=['POST'])
def redmine_receiver():
    received = request.get_json()
    incom = RedmineWebhookParser(received)
    notify = bool(incom.assignee_name == 'xiaoxuan' or incom.assignee_name == 'vseven')

    if not notify:
        return jsonify({'res': 'success'})

    chat_id = tg_group.name['sport_official']
    name = '@Vsenver' if incom.assignee_name == 'vseven' else incom.assignee_name
    text = '''
URL: http://redmine.lianfa.co/issues/{id}\r
议题: {subject}\r
状态: {status}\r
被分派者: {name}\r
    '''.format(
        id=incom.issue_id,
        subject=incom.subject,
        status=incom.status_name,
        name=name
    )

    data = {
        'chat_id': chat_id,
        'text': text
    }
    Post('sendMessage', data)

    return jsonify({'res': 'success'})


@app.route("/redmineUpdater", methods=['POST'])
def redmine_hook():
    data = request.get_json()
    print(data)
    for commit in data['commits']:
        username = commit['committer']['username']
        key = redmine_keys.keys[username.lower()]
        key = key if key else redmine_keys['blessma'] 
        message = commit['message']
        pattern = r"\[?(#\d+)\]?"
        numbers = []
        end = 0

        for match in re.finditer(pattern, message):
            number = re.search(r"\d+", match.group()).group()
            numbers.append(number)
            end = match.end()
            pass
        
        notes = message[end: ]

        for num in numbers:
            redmine.issueUpdater(num, key=key, notes=notes)
            print('redmine', username, key)

    return jsonify({'res': 'success'})


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
