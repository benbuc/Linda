# Author: Benito Buchheim

import jsonpickle
import os
import os.path
import utilities
from LindaService import Service
from LindaConfig import LindaConfig
import sys

# SETUP LOGGING
log = utilities.getLogger()

# CHANGE WORKING DIRECTORY
os.chdir(os.path.dirname(sys.argv[0]))

class Linda(object):

    def __init__(self):
        log.info("Linda initializing")

        self.services = []

        self.readConfig()

        self.loadServices()

    def readConfig(self):
        log.debug("Reading configuration files")
        config = LindaConfig()

        # get datapath config
        self.datapath = config.get("DEFAULT", "datapath", fallback="data")
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
            with open(os.path.join(self.datapath, filename), 'rb') as f:
                self.services.append(jsonpickle.decode(f.read()))

    def checkAll(self):
        # checks through all services and triggers
        log.debug("Checking all services")
        for service in self.services:
            self.check(service)
        log.debug("Done checking all services")

    def check(self, service):
        service.check()

if __name__ == "__main__":
    # version check
    utilities.checkVersion()
    # if Linda.py is executed normally, just run all services
    linda = Linda()
    linda.checkAll()
