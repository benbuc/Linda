# Author: Benito Buchheim

# This Program is used to set up Linda
# You can create new services or remove services

import sys
import os
import os.path
import configparser
import utilities
import LindaService as lise
from LindaConfig import LindaConfig

FIRST_ITERATION = True

log = utilities.getLogger()

def main():
    input("\nPress ENTER to continue:")
    print("\n")
    print("")
    print("-"*50)
    print("What do you want to do?")
    print("\t[1] List services")
    print("\t[2] Create new service")
    print("\t[3] Remove service")
    print("\t[0] EXIT")

    try:
        action = int(input("Enter Action: "))
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
    log.debug("Getting datapath from config")
    config = LindaConfig()

    # get datapath config
    datapath = config.get("DEFAULT", "datapath", fallback="data")
    # check if directory exists and create if not
    if not os.path.exists(datapath):
        log.debug("Creating datapath directory")
        os.mkdir(datapath)

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
    name = input(": ")

    datapath = getDatapath()

    deletions = 0
    for filename in os.listdir(datapath):
        if filename.startswith(name+"."):
            deletions += 1
            log.debug("Deleting %s" % filename)
            os.remove(os.path.join(datapath, filename))

    if deletions > 0:
        print("Done deleting service %s" % name)
    else:
        print("No service found with name %s" % name)


def createNewService():
    print("")
    print("Creating a new service")
    name = input("Service name: ")
    if "." in name:
        print("! Name may not contain '.'")
        return
    print("\nSelect a trigger type")
    print("\t[1] DeviationTriggerTwoThresholds")
    try:
        triggerType = int(input(": "))
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
        actionType = int(input(": "))
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
            triggerThreshold = float(input("Trigger Threshold: "))
            resetThreshold = float(input("Reset Threshold: "))
            datafile = input("Path to your datafile: ")
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
            recipients = input("Input recipients (comma separated): ")
            subject = input("Input subject: ")
            content = input("Content: ")
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
    utilities.checkVersion()
    print("Hi, I am Linda. Have a great day")
    try:
        while "pigs" != "fly":
            main()
    except KeyboardInterrupt:
        print("\nBye")