
class TlgrmException(Exception):
    pass


class TelegramException(TlgrmException):

    def __init__(self, data):
        self.error_code = data['error_code']
        self.description = data['description']

    def __str__(self):
        return 'Telegram return error: {0}, {1}'.format(
            self.error_code,
            self.description
        )
