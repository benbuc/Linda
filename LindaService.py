# Author: Benito Buchheim

import pickle

class Service(object):

    def __init__(self, name, trigger=None, action=None):
        self.name = name
        self.trigger = trigger
        self.action = action

    def setTrigger(self, trigger):
        self.trigger = trigger
    
    def setAction(self, action):
        self.action = action

    def check(self):
        """Check whether trigger is active and fire action if so."""
        if not (self.trigger and self.action):
            return

        if self.trigger.isTriggered():
            self.action.trigger()

    def save(self, filepath):
        """Save service to filepath"""
        with open(filepath, 'w') as f:
            pickle.dump(self, f)

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
        print("Sending E-Mail")

if __name__ == "__main__":
    # generate a sample service
    service = Service("sample_service")
    service.save("data/sample_service.lise")