class Message(object):
    def __init__(self, sender, receiver, data):
        self.sender = sender
        self.receiver = receiver
        self.data = data

    def __getitem__(self, key):
        try:
            return self.data[key]
        except (KeyError):
            return None

    def __str__(self):
        return "{} -> {} : {}".format(self.sender, self.receiver, self.data)

    def get_channel(self):
        return (self.sender, self.receiver)

    def as_sendable(self):
        return { 'obj': self }

