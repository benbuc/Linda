# Author: Benito Buchheim

from LindaService import *
import pickle
import os
import os.path
import configparser
import logging

DATAPATH = "data/"
CONFIGFILE = "lindaconfig.ini"

class Linda(object):

    def __init__(self, configfile):
        self.log = logging.getLogger()
        self.logHandler = logging.StreamHandler()
        
        self.logFormatter = logging.Formatter("%(asctime)s %(name)-12s %(levelname)-8s %(message)s")
        self.logHandler.setFormatter(self.logFormatter)
        self.log.addHandler(self.logHandler)

        self.log.setLevel(logging.DEBUG)

        self.log.info("Linda initializing")

        self.services = []
        self.configfile = configfile

        self.readConfig()

        self.loadServices()

    def readConfig(self):
        self.log.debug("Reading configuration files")
        config = configparser.ConfigParser()
        config.read(self.configfile)

        # get datapath config
        self.datapath = config.get("DEFAULT", "datapath", fallback="data")
        # check if directory exists and create if not
        self.log.debug("Checking if datapath exists")
        if not os.path.exists(self.datapath):
            self.log.debug("Creating directory for datapath")
            os.mkdir(self.datapath)

    def loadServices(self):
        self.log.debug("Loading services from datapath")
        self.services = []

        # iterate through all services and add to list
        for filename in os.listdir(self.datapath):
            if not filename.endswith(".lise"):
                continue

            # load the service and add to services
            self.log.debug("Adding service: %s", filename)
            with open(os.path.join(self.datapath, filename), 'r') as f:
                self.services.append(pickle.load(f))

    def checkAll(self):
        # checks through all services and triggers
        self.log.debug("Checking all services")
        for service in self.services:
            self.check(service)

    def check(self, service):
        service.check()

    def removeServiceWithName(self, serviceName):
        """Remove all services with given name."""

        # TO-DO: This function probably should be moved to the LindaHelper

        self.log.debug("Removing service with name")
        
        for filename in os.listdir(self.datapath):
            if not filename.endswith(".lise"):
                continue

            with open(os.path.join(self.datapath, filename), 'r') as f:
                if pickle.load(f).name == serviceName:
                    os.remove(os.path.join(self.datapath, filename))

if __name__ == "__main__":
    linda = Linda(CONFIGFILE)
    