# Author: Benito Buchheim

# This Program is used to set up Linda
# You can create new services or remove services

import sys
import os
import os.path
import configparser
import LindaService as lise
from LindaGlobals import CONFIGFILE

FIRST_ITERATION = True

def main():
    raw_input("\nPress ENTER to continue:")
    print("\n")
    print("")
    print("-"*50)
    print("What do you want to do?")
    print("\t[1] List services")
    print("\t[2] Create new service")
    print("\t[3] Remove service")
    print("\t[0] EXIT")

    try:
        action = int(raw_input("Enter Action: "))
    except ValueError:
        print("Invalid input!")
        return

    print("")

    if action == 0:
        print("See you soon")
        sys.exit()
    elif action == 1:
        listServices()
    elif action == 2:
        createNewService()
    elif action == 3:
        removeService()
    else:
        print("Unknown action")

def getDatapath():
    config = configparser.ConfigParser()
    config.read(CONFIGFILE)

    # get datapath config
    datapath = config.get("DEFAULT", "datapath", fallback="data")
    # check if directory exists and create if not
    if not os.path.exists(datapath):
        os.mkdir(datapath)#

    return datapath

def listServices():
    print("Listing all services:")
    for filename in os.listdir(getDatapath()):
        if not filename.endswith(".lise"):
            continue

        print("\t%s" % ".".join(filename.split(".")[:-1]))

def removeService():
    listServices()

    print("Input service name you wish to remove. This can NOT be undone.")
    name = raw_input(": ")

    datapath = getDatapath()

    for filename in os.listdir(datapath):
        if filename.startswith(name+"."):
            os.remove(os.path.join(datapath, filename))

    print("Done deleting service")


def createNewService():
    print("")
    print("Creating a new service")
    name = raw_input("Service name: ")
    if "." in name:
        print("! Name may not contain '.'")
        return
    print("\nSelect a trigger type")
    print("\t[1] DeviationTriggerTwoThresholds")
    try:
        triggerType = int(raw_input(": "))
    except ValueError:
        print("Invalid input")
        return
    if triggerType == 1:
        trigger = setupDeviationTriggerTwoThresholds(getDatapath(), name)
    else:
        print("Unknown trigger type")
        return

    print("\nSelect an action type")
    print("\t[1] MailAction")
    try:
        actionType = int(raw_input(": "))
    except ValueError:
        print("Invalid input")
        return
    if actionType == 1:
        action = setupMailAction(getDatapath(), name)
    else:
        print("Unknown action type")
        return
    
    datapath = getDatapath()
    service = lise.Service(datapath, name)
    service.setTrigger(trigger)
    service.setAction(action)
    service.save()

    print("Successfully created service")


def setupDeviationTriggerTwoThresholds(datapath, name):
    hasData = False
    while not hasData:
        try:
            triggerThreshold = float(raw_input("Trigger Threshold: "))
            resetThreshold = float(raw_input("Reset Threshold: "))
            datafile = raw_input("Path to your datafile: ")
            hasData = True
        except ValueError:
            print("Invalid input. Please try again")
            continue
    
    kwargs = {
        "trigger_threshold" : triggerThreshold,
        "reset_threshold"   : resetThreshold,
        "datafile"          : datafile
    }
    trigger = lise.DeviationTriggerTwoThresholds(datapath, name, **kwargs)

    return trigger

def setupMailAction(datapath, name):
    hasData = False
    while not hasData:
        try:
            recipients = raw_input("Input recipients (comma separated): ")
            subject = raw_input("Input subject: ")
            content = raw_input("Content: ")
            hasData = True
        except ValueError:
            print("Invalid input. Please try again")
            continue

    kwargs = {
        "recipients"    : recipients,
        "subject"       : subject,
        "content"       : content
    }
    return lise.MailAction(datapath, name, **kwargs)

    
if __name__ == "__main__":
    print("Hi, I am Linda. Have a great day")
    try:
        while "pigs" != "fly":
            main()
    except KeyboardInterrupt:
        print("\nBye")