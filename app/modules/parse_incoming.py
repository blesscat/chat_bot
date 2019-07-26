from .lunch_pool import lunch_pool
import random

draw_pool = [
  'https://ws1.sinaimg.cn/large/006tNbRwgy1fxws35vaglj308w08wdfw.jpg',
  'https://ws3.sinaimg.cn/large/006tNbRwgy1fxwscphlxog308c057q4o.gif'
]


class ParseIncoming():
    def __init__(self, data):
        self.data = data

    @property
    def update_id(self):
        if ('update_id' in self.data):
            return self.data['update_id']

    @property
    def document(self):
        if ('document' in self.message):
            return self.message['document']
        return {}

    @property
    def sticker(self):
        if ('sticker' in self.message):
            return self.message['sticker']
        return False

    @property
    def photo(self):
        if ('photo' in self.message):
            return self.message['photo']
        return {}

    @property
    def video(self):
        if ('video' in self.message):
            return self.message['video']
        return {}

    @property
    def from_id(self):
        if('from' in self.message):
            return self.message['from']['id']

    @property
    def chat(self):
        if ('chat' in self.message):
            return self.message['chat']

    @property
    def message_id(self):
        if ('message_id' in self.message):
            return self.message['message_id']

    @property
    def chat_id(self):
        if ('id' in self.chat):
            return self.chat['id']

    @property
    def message(self):
        if ('message' in self.data):
            return self.data['message']
        return {}

    @property
    def text(self):
        if ('text' in self.message):
            return self.message['text']
        return {}
    
    @property
    def isMp4(self):
        if ('mime_type' in self.document) :
            return self.document['mime_type'] == 'video/mp4'


    @property
    def isDoc(self):
        return bool(self.document) or bool(self.photo) or bool(self.video)

    @property
    def isSticker(self):
        return bool(self.sticker)

    @property
    def isLunch(self):
        if (self.text):
            return self.text.startswith('西湖吃什麼', 0, 5)

    @property
    def gqLunch(self):
        if (self.text):
            return self.text.startswith('港墘吃什麼', 0, 5)

    @property
    def isDraw(self):
        if (self.text):
            return self.text.startswith('抽', 0, 1) and len(self.text) == 1

    @property
    def isJavaCat(self):
        if (self.text):
            return self.text.startswith('JAVA小貓咪', 0, 7)

    @property
    def isReport(self):
        if (self.text):
            return self.text.startswith('週三報表', 0, 4)

    @property
    def isTeaTime(self):
        if (self.text):
            return self.text.startswith('下午茶誰請', 0, 5)

    @property
    def isDrawLots(self):
        if (self.text):
            return self.text.startswith('請小妹聖示 ', 0, 6)

    @property
    def isTest(self):
        if (self.text):
            return self.text.startswith('test ', 0, 5)

    @property
    def isOCR(self):
        if (self.text):
            return self.text.startswith('OCR ', 0, 4)

    def getLunch(self):
        return random.choice(lunch_pool)

    # def getDraw(self):
    #     return random.choice(draw_pool)
    
