# Author: Benito Buchheim

from LindaService import *
import pickle
import os
import os.path

DATAPATH = "data/"

class Linda(object):

    def __init__(self):
        self.services = []

    def loadServices(self, datapath):
        # iterate through all services
        for filename in os.listdir(datapath):
            if not filename.endswith(".lise"):
                continue

            # load the service and add to services
            with open(os.path.join(datapath, filename), 'r') as f:
                self.services.append(pickle.load(f))

    def checkAll(self):
        # checks through all services and triggers
        for service in self.services:
            self.check(service)

    def check(self, service):
        service.check()

    def addService(self, service):
        self.services.append(service)

    def removeService(self, service):
        self.services.remove(service)


if __name__ == "__main__":
    pass