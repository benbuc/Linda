# Author: Benito Buchheim

import pickle
import os.path
import logging

# generate the logger
log = logging.getLogger()
logHandler = logging.StreamHandler()

logFormatter = logging.Formatter("%(asctime)s %(name)-12s %(levelname)-8s %(message)s")
logHandler.setFormatter(logFormatter)
log.addHandler(logHandler)

log.setLevel(logging.DEBUG)

class Service(object):

    # Every service has a name which has to be unique inside datapath
    # Service saves itself to datapath/name.lise adding the extension
    # and overwriting every other service with the same name

    def __init__(self, datapath, name, trigger=None, action=None):
        self.datapath = datapath
        self.name = name
        self.trigger = trigger
        self.action = action

        log.debug("Initializing Service: %s", self.name)

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

    def save(self):
        """Save service to filepath"""
        destination = os.path.join(self.datapath, self.name+".lise")
        log.debug("Saving service to %s", destination)
        with open(os.path.join(self.datapath, self.name+".lise"), 'w') as f:
            pickle.dump(self, f)
            
class Trigger(object):

    def __init__(self, datapath, name, **kwargs):
        # datapath holds the path where the trigger is allowed to save
        #   data it needs for the future
        # name is the same name the service has (every service may have up to one trigger)
        #   this is used to save persistent data and Linda can remove the trigger
        #   when the service should be deleted
        # kwargs holds a variable length dictionary with additional arguments
        #   (like the thresholds for specific trigger types or the path to input data files)
        self.datapath = datapath
        self.name = name

        self.kwargs = kwargs

    def isTriggered(self):
        return False

class DeviationTriggerTwoThresholds(Trigger):

    def __init__(self, datapath, name, **kwargs):
        super.__init__(datapath, name, kwargs)

        ########################################
        # COPY ARGUMENTS TO INSTANCE VARIABLES #
        ########################################

        # triggerThreshold is the Threshold which has to be reached to start the trigger
        # (then triggers once and waits to return below resetThreshold)
        # Direction is calculated from both triggers so you can set up the trigger to fire
        # when the value rises above or falls below a certain threshold
        self.triggerThreshold = self.kwargs["trigger_threshold"]
        self.resetThreshold = self.kwargs["reset_threshold"]

        # the filepath where the input data will be stored
        self.datafile = self.kwargs["datafile"]

    def loadCurrent(self):
        """Return the current value from datafile."""
        if not os.path.exists(self.datafile):
            log.error("Datafile does not exist: %s", self.datafile)
            return -1

        with open(self.datafile, 'r') as f:
            content = f.read().strip()

            try:
                content = float(content)
                return content
            except ValueError:
                log.error("Could not interpret datafile: %s", self.datafile)

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
    service = Service("data", "sample_service")
    service.save()