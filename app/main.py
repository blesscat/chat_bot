import os
import re
import random
import time
import requests
import subprocess
from flask import request, render_template, jsonify, current_app, send_from_directory, make_response
from sqlalchemy.sql import func

from . import app, db, TOKEN, DEV_TOKEN
from .modules import db_models
from .modules import lots_pool
from .modules import tg_group
from .modules.parse_incoming import ParseIncoming

from .modules.redmine_webhook_parser import RedmineWebhookParser

from .modules import redmine
from .modules import redmine_keys

import xmltodict

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

def prNotify(incom):
    onGoing = db_models.Pr.query.filter(db_models.Pr.status!='closed').all()
    text = ', \r\n'.join(str(pr.location) for pr in onGoing)
    text = '{} \r\n\r\n are still on going.'.format(text)
    
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
    elif incoming.isPr:
        prNotify(incoming)

    # elif incoming.isSticker or incoming.isDoc:
    elif incoming.isSticker:
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
    notify = bool(incom.assignee_name == 'xiaoxuan'
                  or incom.assignee_name == 'vseven'
                  or incom.assignee_name == 'allen'
                  or incom.assignee_name == 'dns'
              )

    print('redmine receiver', incom)
    if not notify:
        return jsonify({'res': 'success'})

    chat_id = tg_group.name['sport_official']
    # chat_id = tg_group.name['sport']
    name = '@Vsenver' if incom.assignee_name == 'vseven' else incom.assignee_name
    name = '@Dennis_cute' if incom.assignee_name == 'dns' else incom.assignee_name
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


def HandlePushEvent(data):
    issues = []
    for commit in data['commits']:
        username = commit['author']['username']
        if username.lower() not in redmine_keys.keys:
            username = commit['author']['name']
            if username.lower() not in redmine_keys.keys: continue

        key = redmine_keys.keys[username.lower()]
        message = commit['message']

        commitID = commit['id']
        hasCommitted = db_models.Commit.query.filter_by(commitID=commitID).all()
        if hasCommitted:
            continue
        else:
            commit = db_models.Commit(commitID)
            db.session.add(commit)
            db.session.commit()

        pattern = r"\[?(#\d+)\]?"
        numbers = []
        end = 0

        for match in re.finditer(pattern, message):
            number = re.search(r"\d+", match.group()).group()
            numbers.append(number)
            end = match.end()
        
        notes = message[end: ]
        issues.extend(numbers)

        for num in numbers:
            redmine.issueUpdater(num, key=key, notes=notes)
            print('redmine', username, key)

    if issues:
        team = request.args.get('team')
        chat_id = tg_group.name['redmine_notify']
        text = 'team: {team}\n{numbers} has been updated on redmine.'.format(
            team=team,
            numbers=', '.join('#{}'.format(num) for num in issues)
        )
        data = {
            'chat_id': chat_id,
            'text': text
        }
        Post('sendMessage', data)


def HandlePrEvent(data):
    team = request.args.get('team')
    if team not in tg_group.name: return

    chat_id = tg_group.name[team]
    action = data['action']
    number = data['number']
    name = data['repository']['name']
    pr = data['pull_request']
    creator = pr['user']['username']
    sender = data['sender']['username']
    if pr['assignees']:
        assignees = [ '@{}'.format(assignee['username']) for assignee in pr['assignees'] ]
    else:
        assignees = None
    url = data['repository']['html_url']
    location ='{url}/pulls/{number}'.format(url=url, number=number)
    text = '''
pull request\r
repository: {name}\r
sender: {sender}\r
URL: {location}\r
action: {action}\r
assignees: {assignees}\r
    '''.format(
        name=name,
        action=action,
        sender=sender,
        location=location,
        assignees=', '.join(assignees) if assignees else None
    )

    found = db_models.Pr.query.filter_by(location=location).first()
    if (found):
        if action == 'closed':
            db.session.delete(found)
        else:
            found.status = action
        db.session.commit()
    else:
        pr = db_models.Pr(location, action, text)
        db.session.add(pr)
        db.session.commit()

    data = {
        'chat_id': chat_id,
        'text': text 
    }
    Post('sendMessage', data)

    

@app.route("/redmineUpdater", methods=['POST'])
def redmine_hook():
    data = request.get_json()
    print(request.args.get('team'))
    print(request.headers.get('X-GitHub-Event'))
    print(data)
    event = request.headers.get('X-GitHub-Event') 
    if event == 'push':
        HandlePushEvent(data)
    elif event == 'pull_request':
        HandlePrEvent(data)

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


@app.route("/udid/<udid>", methods=['GET'])
def udidDisplay(udid):
    return udid


@app.route("/udid/receiver", methods=['POST'])
def udid():
    s = request.get_data()
    decoded = s.decode(errors="ignore")
    start = decoded.find('<plist')
    end = decoded.find('</plist')
    plist = xmltodict.parse(decoded[start:end + 8])
    print(plist)
    for i, key in enumerate(plist['plist']['dict']['key']):
        if key == 'UDID':
            idx = i
    response = make_response('hello', 301)
    location = 'https://blesstest.lianfa.co/udid/{}'.format(
        plist['plist']['dict']['string'][idx]
    )
    response.headers['Location'] = location
    return response

@app.route("/udid/profile", methods=['GET'])
def downloadProfile():
    path = os.path.join(current_app.root_path, 'files')
    return send_from_directory(path,
                               filename="umbilical.mobileconfig",
                               as_attachment=True 
                               )
