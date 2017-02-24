import json

from telegramio.log import logger
from telegramio.transport import HttpProtocol
from telegramio.exceptions import TelegramException

data_url = "https://api.telegram.org/bot{0}{1}"
file_url = "https://api.telegram.org/file/bot{0}{1}"
headers = {'User-agent': 'Bot on Telegramio'}


def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except (ValueError, TypeError):
        return False
    return True


def to_json(locale):
    data = {key: value for key, value in locale.items()
            if key not in ['self']
            and value is not None
            and key != 'method'}
    return json.dumps(data)


def to_dict(locale):
    data = {key: value for key, value in locale.items()
            if key not in ['self']
            and value is not None
            and key != 'method'}
    return data


class Telegram(HttpProtocol):

    def __init__(self, loop, token, proxy, retry_fail, retry_count, retry_interval):
        HttpProtocol.__init__(self, loop, proxy, retry_fail, retry_count, retry_interval)

        self.token = token
        self.telegram_errors = 0

    def method(func):
        async def decorator(self, *args, **kwargs):
            method, data = func(self, *args, **kwargs)
            if is_json(data):
                headers['Content-type'] = 'application/json'
            url = data_url.format(self.token, method)
            response = await self.request(url, timeout=35, data=data, headers=headers)
            return self.validation(response)
        return decorator

    def validation(self, response):
        if response is not None:
            try:
                response = json.loads(response)
                if response['ok']:
                    return response['result']
                else:
                    raise TelegramException(response)
            except (TelegramException, json.JSONDecodeError) as exc:
                logger.error(exc)
                self.telegram_errors += 1
                return None
        else:
            return None

    @method
    def getUpdates(self, offset=0, limit=10, allowed_updates=[]):
        method = '/getUpdates'
        timeout = 30
        return method, to_json(locals())

    @method
    def getMe(self):
        method = '/getMe'
        return method, to_json(locals())

    @method
    def sendMessage(self, chat_id, text, 
                    parse_mode=None,
                    disable_web_page_preview=None,
                    disable_notification=None,
                    reply_to_message_id=None,
                    reply_markup=None):
        method = '/sendMessage'
        return method, to_json(locals())

    @method
    def forwardMessage(self, chat_id, from_chat_id, message_id,
                       disable_notification=None):
        method = '/forwardMessage'
        return method, to_json(locals())

    @method
    def sendPhoto(self, chat_id, photo,
                  caption=None,
                  disable_notification=None,
                  reply_to_message_id=None,
                  reply_markup=None):
        method = '/sendPhoto'
        if hasattr(photo, 'read') or str(photo).startswith('http'):
            return method, to_dict(locals())
        else:
            return method, to_json(locals())

    @method
    def sendAudio(self, chat_id, audio,
                  caption=None,
                  duration=None,
                  performer=None,
                  title=None,
                  disable_notification=None,
                  reply_to_message_id=None,
                  reply_markup=None):
        method = '/sendAudio'
        if hasattr(audio, 'read') or str(audio).startswith('http'):
            return method, to_dict(locals())
        else:
            return method, to_json(locals())

    @method
    def sendDocument(self, chat_id, document,
                     caption=None,
                     disable_notification=None,
                     reply_to_message_id=None,
                     reply_markup=None):
        method = '/sendDocument'
        if hasattr(document, 'read') or str(document).startswith('http'):
            return method, to_dict(locals())
        else:
            return method, to_json(locals())

    @method
    def sendSticker(self, chat_id, sticker,
                    disable_notification=None,
                    reply_to_message_id=None,
                    reply_markup=None):
        method = '/sendSticker'
        if hasattr(sticker, 'read') or str(sticker).startswith('http'):
            return method, to_dict(locals())
        else:
            return method, to_json(locals())

    @method
    def sendVideo(self, chat_id, video,
                  duration=None,
                  width=None,
                  height=None,
                  caption=None,
                  disable_notification=None,
                  reply_to_message_id=None,
                  reply_markup=None):
        method = '/sendVideo'
        if hasattr(video, 'read') or str(video).startswith('http'):
            return method, to_dict(locals())
        else:
            return method, to_json(locals())

    @method
    def sendVoice(self, chat_id, voice,
                  caption=None,
                  duration=None,
                  disable_notification=None,
                  reply_to_message_id=None,
                  reply_markup=None):
        method = '/sendVoice'
        if hasattr(voice, 'read') or str(voice).startswith('http'):
            return method, to_dict(locals())
        else:
            return method, to_json(locals())

    @method
    def sendLocation(self, chat_id,
                     latitude,
                     longitude,
                     disable_notification=None,
                     reply_to_message_id=None,
                     reply_markup=None):
        method = '/sendLocation'
        return method, to_json(locals())

    @method
    def sendVenue(self, chat_id,
                  latitude,
                  longitude,
                  title,
                  address,
                  foursquare_id=None,
                  disable_notification=None,
                  reply_to_message_id=None,
                  reply_markup=None):
        method = '/sendVenue'
        return method, to_json(locals())

    @method
    def sendContact(self, chat_id,
                    phone_number,
                    first_name,
                    last_name,
                    disable_notification=None,
                    reply_to_message_id=None,
                    reply_markup=None):
        method = '/sendContact'
        return method, to_json(locals())

    @method
    def sendChatAction(self, chat_id, action):
        method = '/sendChatAction'
        return method, to_json(locals())
    
    @method
    def getUserProfilePhotos(self, user_id,
                             offset=None,
                             limit=1):
        method = '/getUserProfilePhotos'
        return method, to_json(locals())

    @method
    def getFile(self, file_id):
        method = '/getFile'
        return method, to_json(locals())

    @method
    def kickChatMember(self, chat_id,
                       user_id):
        method = '/kickChatMember'
        return method, to_json(locals())

    @method
    def leaveChat(self, chat_id):
        method = '/leaveChat'
        return method, to_json(locals())

    @method
    def unbanChatMember(self, chat_id,
                        user_id):
        method = '/unbanChatMember'
        return method, to_json(locals())

    @method
    def getChat(self, chat_id):
        method = '/getChat'
        return method, to_json(locals())

    @method
    def getChatAdministrators(self, chat_id):
        method = '/getChatAdministrators'
        return method, to_json(locals())

    @method
    def getChatMembersCount(self, chat_id):
        method = '/getChatMembersCount'
        return method, to_json(locals())

    @method
    def getChatMember(self, chat_id,
                      user_id):
        method = '/getChatMember'
        return method, to_json(locals())
    
    @method
    def answerCallbackQuery(self, callback_query_id,
                            text=None,
                            show_alert=False,
                            url=None,
                            cache_time=300):
        method = '/answerCallbackQuery'
        return method, to_json(locals())
    
    #Updating messages methods
    @method
    def editMessageText(self, text, chat_id=None, 
                        message_id=None,
                        inline_message_id=None,
                        parse_mode=None,
                        disable_web_page_preview=None,
                        reply_markup=None):
        method = '/editMessageText'
        return method, to_json(locals())

    @method
    def editMessageCaption(self, chat_id=None, 
                        caption=None,
                        message_id=None,
                        inline_message_id=None,
                        reply_markup=None):
        method = '/editMessageCaption'
        return method, to_json(locals())
    
    @method
    def editMessageReplyMarkup(self, chat_id=None, 
                        message_id=None,
                        inline_message_id=None,
                        reply_markup=None):
        method = '/editMessageReplyMarkup'
        return method, to_json(locals())
    
    #Inline mode methods
    def answerInlineQuery(self, inline_query_id, results=[],
                          cache_time=300,
                          is_personal=True,
                          next_offset=None,
                          switch_pm_text=None,
                          switch_pm_parameter=None):
        method = '/answerInlineQuery'
        return method, to_json(locals())





