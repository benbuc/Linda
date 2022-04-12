# Author: Benito Buchheim

import jsonpickle
import os.path
import smtplib
from email.mime import multipart
from email.mime import text
import socket

from linda import utilities

# generate the logger
log = utilities.getLogger()


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
        destination = os.path.join(self.datapath, self.name + ".lise")
        log.debug("Saving service to %s", destination)
        with open(destination, "w") as f:
            f.write(jsonpickle.encode(self, indent=4))


class Trigger(object):
    def __init__(self, datapath, name, **kwargs):
        # datapath holds the path where the trigger is allowed to save
        #   data it needs for the future
        # name is the same name the service has (every service may
        #   have up to one trigger)
        #   this is used to save persistent data and Linda can remove the trigger
        #   when the service should be deleted
        # kwargs holds a variable length dictionary with additional arguments
        #   (like the thresholds for specific trigger types or the path to
        #    input data files)
        self.datapath = datapath
        self.name = name

        self.kwargs = kwargs

    def isTriggered(self):
        return False


class DeviationTriggerTwoThresholds(Trigger):
    def __init__(self, datapath, name, **kwargs):
        super(DeviationTriggerTwoThresholds, self).__init__(datapath, name, **kwargs)

        ########################################
        # COPY ARGUMENTS TO INSTANCE VARIABLES #
        ########################################

        # triggerThreshold is the Threshold which has to be reached to start the trigger
        # (then triggers once and waits to return below resetThreshold)
        # Direction is calculated from both triggers so you can set up the trigger to
        # fire when the value rises above or falls below a certain threshold
        self.triggerThreshold = self.kwargs["trigger_threshold"]
        self.resetThreshold = self.kwargs["reset_threshold"]

        # the filepath where the input data will be stored
        self.datafile = self.kwargs["datafile"]

    def loadCurrent(self):
        """Return the current value from datafile."""
        if not os.path.exists(self.datafile):
            log.error("Datafile does not exist: %s", self.datafile)
            return -1

        with open(self.datafile, "r") as f:
            content = f.read().strip()

            try:
                content = float(content)
                return content
            except ValueError:
                log.error("Could not interpret datafile: %s", self.datafile)

        return -1

    def getStateFilepath(self):
        return os.path.join(self.datapath, self.name + ".triggerstate")

    def getState(self):
        """Get the current state from file"""
        # State can be:
        #   - wait_for_threshold
        #   - wait_for_reset
        # If the files is empty or does not exist it will return wait_for_threshold

        log.debug("Loading trigger state")
        filepath = self.getStateFilepath()

        if not os.path.exists(filepath):
            log.debug("Trigger state file does not exist: %s", filepath)
            return "wait_for_threshold"

        with open(filepath, "rb") as f:
            return jsonpickle.decode(f.read())

    def setState(self, state):
        """Set the current trigger state in file"""
        # See getState for further information

        log.debug("Setting trigger state")
        filepath = self.getStateFilepath()

        if state not in ["wait_for_threshold", "wait_for_reset"]:
            log.error("Unknown trigger state: %s", state)
            return

        if not os.path.exists(self.datapath):
            log.debug("Datapath does not exist")
            return

        with open(filepath, "w") as f:
            f.write(jsonpickle.encode(state, indent=4))

        log.debug("Saved state")

    def isTriggered(self):
        """Triggers on deviation"""

        # check if value exceeds triggers
        # and only trigger when trigger hasn't fired yet
        # otherwise wait for it to return back to reset threshold

        state = self.getState()

        # calculate the direction the current value has to pass the threshold
        if self.triggerThreshold < self.resetThreshold:
            # direction is fall
            if (
                state == "wait_for_threshold"
                and self.loadCurrent() <= self.triggerThreshold
            ):
                self.setState("wait_for_reset")
                return True
            elif (
                state == "wait_for_reset" and self.loadCurrent() >= self.resetThreshold
            ):
                self.setState("wait_for_threshold")
        elif self.triggerThreshold > self.resetThreshold:
            # direction is rise
            if (
                state == "wait_for_threshold"
                and self.loadCurrent() >= self.triggerThreshold
            ):
                self.setState("wait_for_reset")
                return True
            elif (
                state == "wait_for_reset" and self.loadCurrent() <= self.resetThreshold
            ):
                self.setState("wait_for_threshold")
        else:
            log.warning("Trigger and Reset threshold are equal in: %s", self.name)

        return False


class Action(object):
    def __init__(self, datapath, name, **kwargs):
        self.datapath = datapath
        self.name = name
        self.kwargs = kwargs

    def trigger(self):
        print("Action triggered")


class MailAction(Action):
    """When triggered, it sends an E-Mail to the given recipients."""

    def __init__(self, datapath, name, **kwargs):
        super(MailAction, self).__init__(datapath, name, **kwargs)

        self.recipients = self.kwargs["recipients"]
        self.subject = self.kwargs["subject"]
        self.content = self.kwargs["content"]

    def getConfig(self):
        """Returns the server, user and password."""

        log.debug("Getting config")

        server = os.getenv("mail_server")
        port = int(os.getenv("mail_port"))
        user = os.getenv("mail_user")
        password = os.getenv("mail_pass")

        log.debug(f"Sending email from {user} on {server}")

        return (server, port, user, password)

    def trigger(self):
        """Send E-Mail to recipients."""

        server, port, user, password = self.getConfig()

        for recipient in self.recipients.split(","):
            log.debug("Constructing E-Mail for %s" % (recipient.strip()))
            msg = multipart.MIMEMultipart()
            msg["From"] = user
            msg["To"] = recipient.strip()
            msg["Subject"] = self.subject

            msg.attach(text.MIMEText(self.content, "plain"))

            log.debug("Connecting to server")

            try:
                conn = smtplib.SMTP(server, port)
                conn.starttls()
                conn.login(user, password)
                log.debug("Sending Mail")
                conn.sendmail(user, recipient.strip(), msg.as_string())
                conn.quit()
                log.debug("Successfully sent Mail")

            except socket.gaierror:
                log.error("SMTP Server name invalid")
                return
            except smtplib.SMTPAuthenticationError:
                log.error("SMTP credentials invalid")
                return
            except Exception as e:
                log.error("Unknown error while sending mail: %s", e)
                return


if __name__ == "__main__":
    m = MailAction(
        "data",
        "test_mail_action",
        recipients=["benitoalpha@buchheims.de"],
        subject="Testmail",
        content="Funktioniert!",
    )
    m.trigger()
