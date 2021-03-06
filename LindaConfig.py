# Author: Benito Buchheim
# This file contains a wrapper to handle Linda's configuration

import configparser as cp
from LindaGlobals import CONFIGFILE

class LindaConfig(cp.ConfigParser):

    def __init__(self):
        super(LindaConfig, self).__init__()
        self.read(CONFIGFILE)

if __name__ == "__main__":
    LindaConfig()