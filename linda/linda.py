import jsonpickle
import os
import os.path

from linda import utilities

# SETUP LOGGING
log = utilities.getLogger()


class Linda(object):
    def __init__(self):
        log.info("Linda initializing")

        self.services = []

        self.readConfig()

        self.loadServices()

    def readConfig(self):
        # get datapath config
        self.datapath = os.getenv("datapath", "data/")
        # check if directory exists and create if not
        log.debug("Checking if datapath exists")
        if not os.path.exists(self.datapath):
            log.debug("Creating directory for datapath")
            os.mkdir(self.datapath)

    def loadServices(self):
        log.debug("Loading services from datapath")
        self.services = []

        # iterate through all services and add to list
        for filename in os.listdir(self.datapath):
            if not filename.endswith(".lise"):
                continue

            # load the service and add to services
            log.debug("Adding service: %s", filename)
            with open(os.path.join(self.datapath, filename), "rb") as f:
                self.services.append(jsonpickle.decode(f.read()))

    def checkAll(self):
        # checks through all services and triggers
        log.debug("Checking all services")
        for service in self.services:
            self.check(service)
        log.debug("Done checking all services")

    def check(self, service):
        service.check()
