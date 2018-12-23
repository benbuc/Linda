# Author: Benito Buchheim

from LindaService import *
import pickle
import os
import os.path
import configparser
import utilities

DATAPATH = "data/"
CONFIGFILE = "lindaconfig.ini"

# SETUP LOGGING
log = utilities.getLogger()

class Linda(object):

    def __init__(self, configfile):
        
        log.info("Linda initializing")

        self.services = []
        self.configfile = configfile

        self.readConfig()

        self.loadServices()

    def readConfig(self):
        log.debug("Reading configuration files")
        config = configparser.ConfigParser()
        config.read(self.configfile)

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
            with open(os.path.join(self.datapath, filename), 'r') as f:
                self.services.append(pickle.load(f))

    def checkAll(self):
        # checks through all services and triggers
        log.debug("Checking all services")
        for service in self.services:
            self.check(service)

    def check(self, service):
        service.check()

    def removeServiceWithName(self, serviceName):
        """Remove all services with given name."""

        # TO-DO: This function probably should be moved to the LindaHelper

        log.debug("Removing service with name")
        
        for filename in os.listdir(self.datapath):
            if not filename.endswith(".lise"):
                continue

            with open(os.path.join(self.datapath, filename), 'r') as f:
                if pickle.load(f).name == serviceName:
                    os.remove(os.path.join(self.datapath, filename))

if __name__ == "__main__":
    linda = Linda(CONFIGFILE)
    linda.checkAll()