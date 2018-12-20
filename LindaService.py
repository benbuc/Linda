# Author: Benito Buchheim

import pickle
import os.path

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

class DeviationTriggerConstantFromFile(Trigger):

    def __init__(self, normal, threshold, datafile):
        super.__init__()

        self.normal = normal
        self.threshold = threshold
        self.datafile = datafile

    def loadCurrent(self):
        """Return the current value from datafile."""
        if not os.path.exists(self.datafile):
            print("[DeviationTriggerConstantFromFile] datafile does not exist")
            return -1

        with open(self.datafile, 'r') as f:
            content = f.read().strip()

            try:
                content = float(content)
            except ValueError, e:
                print("[DeviationTriggerConstantFromFile] could not load datafile")
                print(e)
                return -1

    def isTriggered(self):
        """Triggers on deviation"""
        
        if abs(self.loadCurrent() - self.normal) >= self.threshold:
            return True

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