class IOException(object):
    def __init__(self, message):
        self.message = message
        print(message)

    def getMessage(self):
        return self.message
