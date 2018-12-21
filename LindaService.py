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

class DeviationTriggerTwoThresholds(Trigger):

    def __init__(self, triggerThreshold, resetThreshold, datafile):
        super.__init__()

        # triggerThreshold is the Threshold which has to be reached to start the trigger
        # (then triggers once and waits to return below resetThreshold)
        # Direction is calculated from both triggers so you can set up the trigger to fire
        # when the value rises above or falls below a certain threshold
        self.triggerThreshold = triggerThreshold
        self.resetThreshold = resetThreshold

        # the filepath where the input data will be stored
        self.datafile = datafile

    def loadCurrent(self):
        """Return the current value from datafile."""
        if not os.path.exists(self.datafile):
            print("[DeviationTriggerTwoThresholds] datafile does not exist")
            return -1

        with open(self.datafile, 'r') as f:
            content = f.read().strip()

            try:
                content = float(content)
                return content
            except ValueError, e:
                print("[DeviationTriggerTwoThresholds] could not load datafile")
                print(e)
                return -1

        return -1

    def isTriggered(self):
        """Triggers on deviation"""
        
        # check if value exceeds triggers
        # and only trigger when trigger hasn't fired yet
        # otherwise wait for it to return back to reset threshold

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