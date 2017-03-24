#coding=utf8
import itchat, time
import requests
from itchat.content import *
from picamera import PiCamera

KEY = '8edce3ce905a4c1dbb965e6b35c3834d'

def get_response(msg):
    # 这里我们就像在“3. 实现最简单的与图灵机器人的交互”中做的一样
    # 构造了要发送给服务器的数据
    apiUrl = 'http://www.tuling123.com/openapi/api'
    data = {
        'key'    : KEY,
        'info'   : msg,
        'userid' : 'wechat-robot',
    }
    try:
        r = requests.post(apiUrl, data=data).json()
        # 字典的get方法在字典没有'text'值的时候会返回None而不会抛出异常
        return r.get('text')
    # 为了防止服务器没有正常响应导致程序异常退出，这里用try-except捕获了异常
    # 如果服务器没能正常交互（返回非json或无法连接），那么就会进入下面的return
    except:
        # 将会返回一个None
        return
def take_photo():
    try:
        camera = PiCamera()
        camera.capture('image.jpg')
        camera.close()
    except:
        return 0
    else:
        return 1

def record_video():
    try:
        camera = PiCamera()
        camera.resolution = (640, 480)
        camera.start_recording('my_video.h264')
        camera.wait_recording(5)
        camera.stop_recording()
        camera.close()
    except:
        return 0
    else:
        return 1

def camera_close():
    camera = PiCamera()
    camera.close()
    return
 
@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def tuling_reply(msg):
    if (msg['Text'] == 'photo'):
        if (take_photo() == 1):
            itchat.send_image('image.jpg', msg['FromUserName'])
            return
            #return '@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), 'image.png')
        else:
            return 'take_photo error'
    if (msg['Text'] == 'video'):
        if (record_video() == 1):
            itchat.send_video('my_video.h264', msg['FromUserName'])
            return
        else:
            return 'record_video error'
    if (msg['Text'] == 'test'):
        #while(1):
        take_photo()
        return
    if (msg['Text'] == '1'):
        camera_close()
        return
    # 为了保证在图灵Key出现问题的时候仍旧可以回复，这里设置一个默认回复
    defaultReply = 'I received: ' + msg['Text']
    # 如果图灵Key出现问题，那么reply将会是None
    reply = get_response(msg['Text'])
    # a or b的意思是，如果a有内容，那么返回a，否则返回b
    # 有内容一般就是指非空或者非None，你可以用`if a: print('True')`来测试
    return reply or defaultReply

@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
    msg['Text'](msg['FileName'])
    #return msg['FileName']
    return '@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName'])

@itchat.msg_register(FRIENDS)
def add_friend(msg):
    itchat.add_friend(**msg['Text']) # 该操作会自动将新好友的消息录入，不需要重载通讯录
    itchat.send_msg('Nice to meet you!', msg['RecommendInfo']['UserName'])

@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
    if msg['isAt']:
        itchat.send(u'@%s\u2005I received: %s' % (msg['ActualNickName'], msg['Content']), msg['FromUserName'])

itchat.auto_login(hotReload=True)
itchat.run()