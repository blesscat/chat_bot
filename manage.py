import requests
import sys
from flask_script import Command, Option

from flask_script import Manager, Server

from app import app, db
from app.modules import db_models
from app.modules.beauty_crawler import BeautyCrawler


manager = Manager(app)
manager.add_command('runserver', Server())

TOKEN = '637218572:AAGmOxtvixXYH2KIL9cLA79Rt6dTMCYOjmc'


@manager.option('--url', help='webhook url')
def updateWebhook(url):
    res = requests.get(
        'https://api.telegram.org/bot{}/setwebhook'.format(TOKEN),
        params={'url': '{}/{}'.format(url, TOKEN)}
    )
    print('res', res.text)


@manager.shell
def make_shell_context():
    return dict(
        app=app, db=db,
        beauty=db_models.Beauty,
        launch=db_models.Launch,
        gq=db_models.GqLaunch,
        ban=db_models.Ban,
        pr=db_models.Pr,
        commit=db_models.Commit
    )


manager.add_command('update-beauty', BeautyCrawler())
manager.add_command('pr-status', BeautyCrawler())


if __name__ == '__main__':
    manager.run()
