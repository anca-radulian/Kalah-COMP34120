class InvalidMessageException(object):
    def __init__(self, message):
        self.message = message
        print(message)
