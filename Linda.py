# Author: Benito Buchheim

from LindaService import *
import pickle
import os
import os.path

DATAPATH = "data/"

class Linda(object):

    def __init__(self, datapath):
        self.services = []
        self.datapath = datapath

    def loadServices(self):
        self.services = []
        # check if datapath exists
        if not os.path.exists(self.datapath):
            print("loadServices: datapath does not exist")
            return

        # iterate through all services and add to list
        for filename in os.listdir(self.datapath):
            if not filename.endswith(".lise"):
                continue

            # load the service and add to services
            with open(os.path.join(self.datapath, filename), 'r') as f:
                self.services.append(pickle.load(f))

    def checkAll(self):
        # checks through all services and triggers
        for service in self.services:
            self.check(service)

    def check(self, service):
        service.check()

    def removeServiceWithName(self, serviceName):
        """Remove all services with given name."""
        if not os.path.exists(self.datapath):
            print("removeServiceWithName: datapath does not exist")
            return
        
        for filename in os.listdir(self.datapath):
            if not filename.endswith(".lise"):
                continue

            with open(os.path.join(self.datapath, filename), 'r') as f:
                if pickle.load(f).name == serviceName:
                    os.remove(os.path.join(self.datapath, filename))

if __name__ == "__main__":
    linda = Linda(DATAPATH)
    