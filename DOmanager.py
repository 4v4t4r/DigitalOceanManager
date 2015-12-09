#!/usr/bin/python

'''
Author: Hunter Gregal

Requires: python-digitalocean
pip install -U python-digitalocean

To Suppress SSL Errors:
pip install pyopenssl ndg-httpsclient pyasn1
'''
import argparse
import digitalocean as do
import os, sys

#Debug
from IPython import embed

def initManager():
    f = open("token.conf", "r")
    secretToken = f.readline()
    f.close()
    manager = do.Manager(token=secretToken)
    return manager,secretToken

def setup():
    print "Please paste your Digital Ocean API token below"
    token = raw_input("API Token: ")
    config = open("token.conf", "w")
    config.write(token)
    config.close
    print "Digital Ocean API Token Succesfully setup!"

def checkSetup():
    if (os.stat("token.conf").st_size == 0):
        print "Digital Ocean API Token Not Configured."
        choice = raw_input("Would you like to configure your API token now? [y/n]: ")
        if (choice == "y" or choice == "Y"):
            setup()
        else:
            print "Please setup your Digital Ocean API token to continue..."
            sys.exit(0)

def menu(manager,secretToken):
    os.system("clear")
    print "#################################"
    print "Welcome to the Digital Ocean Manager!\nPlease choose an option number below"
    print "#################################"

    print "1) List Droplets (All, Running, Off)"
    print "2) Droplets Power Control (Shutdown, Restart, Boot)"
    print "3) Create Droplets (Single, Multi)"
    print "4) Destroy Droplets (Single, Multi)"
    print "5) List Images (Snapshots, Backups)"
    print "6) Advanced Droplet Management (Snapshots, Backups, Reset Root Password)"
    print "7) Exit"
    print "#################################"
    processOptions(manager,secretToken)

def processOptions(manager,secretToken):
    choice = raw_input("Choice: ")
    if (choice == "1"):
        listDroplets(manager,secretToken)
    elif (choice == "2"):
        powerControlDroplets(manager,secretToken)
    elif (choice == "3"):
        createDropletsMenu(manager,secretToken)
    elif (choice == "4"):
        destroyDroplets(manager,secretToken)
    elif (choice == "5"):
        listImages()
    elif (choice == "6"):
        advancedMenu()
    elif (choice == "7"):
        sys.exit(0)
    else:
        print "\nInvalid Choice!"

    raw_input("Press Enter to Continue...")

def listDroplets(manager,secretToken):
    droplets = manager.get_all_droplets()
    print "#################################"
    print "1) Show All Droplets"
    print "2) Show Active Droplets"
    print "3) Show Off Droplets"
    choice = raw_input("Choice: ")
    if (choice == "1"):
        for droplet in droplets:
            droplet_info(droplet)
    elif (choice == "2"):
        for droplet in droplets:
            if "active" in droplet.status:
                droplet_info(droplet)
    elif (choice == "3"):
        for droplet in droplets:
            if "off" in droplet.status:
                droplet_info(droplet)
    else:  
        print "\nInvalid Choice!"
    
    raw_input("Press Enter to Continue...")
    menu(manager,secretToken)

def droplet_info(droplet):
    print "#################################"
    print "Name:", droplet.name
    print "Image:", droplet.image.get("name")
    print "Region:", droplet.region.get("name")
    print "Disk:", droplet.size.get("disk")
    print "Memory:", droplet.size.get("memory")
    print "STATUS:", droplet.status

def powerControlDroplets(manager,secretToken):
    droplets = manager.get_all_droplets()
    print "#################################"
    print "1) Shutdown Droplets"
    print "2) Restart (PowerCycle) Droplets"
    print "3) Boot Droplets"
    choice = raw_input("Choice: ")

    if (choice == "1"):
        for droplet in droplets:
            if "active" in droplet.status:
                droplet_info(droplet)
        print "#################################"
        name = raw_input("Name of Droplet to Shutdown: ")
        print "Shutting down", name +"..."
        for droplet in droplets:
            if name == str(droplet.name):
                droplet.shutdown()
                print "Droplet", name, "successfully shutdown"
                
    elif (choice == "2"):
        for droplet in droplets:
            if "active" in droplet.status:
                droplet_info(droplet)
        print "#################################"
        name = raw_input("Name of Droplet to Restart: ")
        print "Restarting", name +"..."
        for droplet in droplets:
            if name == str(droplet.name):
                droplet.power_cycle()
                print "Droplet", name,"succesfully restarted"

    elif (choice == "3"):
        for droplet in droplets:
            if "off" in droplet.status:
                droplet_info(droplet)
        print "#################################"
        name = raw_input("Name of Droplet to Boot: ")
        print "Booting", name +"..."
        for droplet in droplets:
            if name == str(droplet.name):
                droplet.power_on()
                print "Droplet", name, "successfully booted"
                print "Droplet", name," succesfully restarted"
    else:  
        print "\nInvalid Choice!"
    
    raw_input("Press Enter to Continue...")
    menu(manager,secretToken)

def createDropletsMenu(manager,secretToken):
    #how many droplets?
    print "#################################"
    number = ""
    number = raw_input("Number of Droplets to Create: ")
    if number.isdigit() == False:
        print "Please input a real number!"
        raw_input("Press Enter to Continue...")
        menu(manager,secretToken)
    #if one get its name
    name = False
    prefix = False
    if number == "1":
        name = raw_input("Name of Droplet: ")
    #if more than 1, get a suffix
    elif number > 1:
        prefix = raw_input("Prefix of droplets: ")
    #derp out
    else:
        print "Invalid number!"
        raw_input("Press Enter to Continue...")
        menu(manager,secretToken)

    #select region to use
    print "#################################"
    print "Regions"
    print "1) New York"
    print "2) Amsterdam"
    print "3) San Francisco"
    print "4) Singapore"
    print "5) London"
    print "6) Frankfurt"
    print "7) Toronto"
    region = ""
    region = raw_input("Region to Use: ")
    if region == "1":
        region = "nyc3"
    elif region == "2":
        region = "ams3"
    elif region == "3":
        region = "sfo1"
    elif region == "4":
        region = "sgp1"
    elif region == "5":
        region = "lon1"
    elif region == "6":
        region = "fra1"
    elif region == "7":
        region = "tor1"
    else:
        print "Invalid Option!"
        raw_input("Press Enter to Continue...")
        menu(manager,secretToken)

    #select image to use
    print "#################################"
    print "Images"
    print "1) Ubuntu 14 x32"
    print "2) Ubuntu 14 x64"
    print "3) FreeBSD 10 x64"
    print "4) Fedora 22 x64"
    print "5) Debian 8 x32"
    print "6) Debian 8 x64"
    print "7) CoreOS 877 beta"
    print "8) CentOS 7 x64"
    image = ""
    image = raw_input("Image to Use: ")
    if image == "1":
        image = "ubuntu-14-04-x32"
    elif image == "2":
        image = "ubuntu-14-04-x64"
    elif image == "3":
        image = "freebsd-10-2-x64"
    elif image == "4":
        image = "fedora-22-x64"
    elif image == "5":
        image = "debian-8-x32"
    elif image == "6":
        image = "debian-8-x64"
    elif image == "7":
        image = "coreos-beta"
    elif image == "8":
        image = "centos-7-0-x64"
    else:
        print "Invalid Option!"
        raw_input("Press Enter to Continue...")
        menu(manager,secretToken)

    #select slug_size
    print "#################################"
    print "Droplet Size"
    print "1) 512mb"
    print "2) 1gb"
    print "3) 2gb"
    print "4) 4gb"
    print "5) 8gb"
    print "6) 16gb"
    print "7) 32gb"
    print "8) 48gb"
    print "9) 64gb"
    size = ""
    size = raw_input("Droplet Size to Use: ")
    if size == "1":
        size = "512mb"
    elif size == "2":
        size = "1gb"
    elif size == "3":
        size = "2gb"
    elif size == "4":
        size = "4gb"
    elif size == "5":
        size = "8gb"
    elif size == "6":
        size = "16gb"
    elif size == "7":
        size = "32gb"
    elif size == "8":
        size = "48gb"
    elif size == "9":
        size = "64gb"
    else:
        print "Invalid Option!"
        raw_input("Press Enter to Continue...")
        menu(manager,secretToken)

    #backups yes/no
    print "#################################"
    print "Would you like backups enabled?"
    backups = ""
    backups = raw_input("y/n: ")
    if backups == "y" or backups == "Y":
        backups = True
    elif backups == "n" or backups == "N":
        backups = False
    else:
        print "Invalid Option!"
        raw_input("Press Enter to Continue...")
        menu(manager,secretToken)
   
    #Final Confirmation
    print "#################################"
    print "!! WARNING !! ACCOUNT WILL BE CHARGED !!"
    print "#################################"
    print "You are about to create", number, "droplet(s) with the name/suffix of", name, "with the following specs:"
    print "Region:", region
    print "Image:", image
    print "Size:", size
    print "Backups:", str(backups)
    print "#################################"
    confirm = raw_input("Are you sure you want to continue? [y/n]: ")
    #if no backout
    if confirm == "n" or confirm == "N":
        menu(manager,secretToken)
    #if yes launch it
    elif confirm == "y" or confirm == "Y":
        #if multiple, use suffix
        if prefix:
            number = int(number)
            i = 1
            while i <= number:
                droplet = do.Droplet(token=secretToken,
                        name = prefix + "-" + str(i),
                        region = region,
                        image = image,
                        size_slug = size,
                        backups = backups)
                droplet.create()
                print "Droplet", str(i), "Created"
                i = i + 1
            print "Droplets successfully created!"
        if name:
            droplet = do.Droplet(token=secretToken,
                    name = name,
                    region = region,
                    image = image,
                    size_slug = size,
                    backups = backups)
            droplet.create()
            print "Droplet successfully created!"

def destroyDroplets(manager,secretToken):
    droplets = manager.get_all_droplets()
    print "#################################"
    print "1) Destroy a single droplet"
    print "2) Destroy multiple droplets (suffix/contains word)"
    choice = raw_input("Choice: ")
    if (choice == "1"):
        for droplet in droplets:
            droplet_info(droplet)
        print "#################################"
        name = raw_input("Name of Droplet to Destroy: ")
        print "!! ARE YOU SURE YOU WANT TO DESTROY DROPLET", name + "? !!"
        confirm = raw_input("[y/n]: ")
        if confirm == "y" or confirm == "Y":
            print "Destroying", name +"..."
            for droplet in droplets:
                if name == str(droplet.name):
                    droplet.destroy()
                    print "Droplet", name, "successfully destroyed"
        elif confirm =="n" or confirm == "N":
            raw_input("Press Enter To Continue...")
            menu(manager,secretToken)
        else:
            print "\nInvalid Option!"
            raw_input("Press Enter To Continue...")
            menu(manager,secretToken)
    elif (choice == "2"):
        for droplet in droplets:
            droplet_info(droplet)
        print "#################################"
        name = raw_input("Suffix or match string of Droplets to Destroy: ")
        print "!! ARE YOU SURE YOU WANT TO DESTROY DROPLETS LIKE", name + "? !!"
        confirm = raw_input("[y/n]: ")
        if confirm == "y" or confirm == "Y":
            print "Destroying Droplets LIKE", name +"..."
            for droplet in droplets:
                if name in str(droplet.name):
                    droplet.destroy()
                    print "Droplet", str(droplet.name), "successfully destroyed"
        elif confirm =="n" or confirm == "N":
            raw_input("Press Enter To Continue...")
            menu(manager,secretToken)
        else:
            print "\nInvalid Option!"
            raw_input("Press Enter To Continue...")
            menu(manager,secretToken)
        
    else:
        print "\nInvalid Option!"
        raw_input("Press Enter To Continue...")
        menu(manager,secretToken)

def listImages(manager):
    0
def advancedMenu(manager):
    0

if __name__ == "__main__":
    checkSetup()
    manager,secretToken = initManager()
    while True:
        menu(manager,secretToken)

