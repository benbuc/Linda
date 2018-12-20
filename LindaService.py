class Service(object):

    def __init__(self, trigger=None, action=None):
        self.trigger = trigger
        self.action = action

    def setTrigger(self, trigger):
        self.trigger = trigger
    
    def setAction(self, action):
        self.action = action

class Trigger(object):

    def isTriggered(self):
        return False

class DeviationTrigger(Trigger):

    def __init__(self, threshold):
        super.__init__()

        self.threshold = threshold

    def isTriggered(self):
        """Triggers on deviation"""
        return False

class Action(object):

    def trigger(self):
        print("Action triggered")

class MailAction(Action):
    """When triggered, it sends an E-Mail to the given recipients."""

    def __init__(self, recipients, content):
        super.__init__()

        self.recipients = recipients
        self.content = content

    def trigger(self):
        """Send E-Mail to recipients."""