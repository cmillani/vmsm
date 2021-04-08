from flask import Blueprint
from os import environ
import libvirt

videogame_route = Blueprint('videogame', __name__)
conn = None;

@videogame_route.route('/videogame/turnon', methods=['POST'])
def turnGameOn():
    domain = getDomain()
    error = domain.create()
    return parseVmPowerActionError(error)

@videogame_route.route('/videogame/turnoff', methods=['POST'])
def turnGameOff():
    domain = getDomain()
    error = domain.shutdown()
    return parseVmPowerActionError(error)

@videogame_route.route('/videogame', methods=['GET'])
def getVmStatus():
    domain = getDomain()
    return "ON" if domain.isActive() else "OFF" 

def parseVmPowerActionError(error):
    if (not error):
        return 'OK'
    else:
        return error, 500

def getDomain():
    global conn
    if(conn is None or not conn.isAlive()):
        print("Connecting to remote QEMU")
        conn = libvirt.open(getConnectionString())
        print("Connected!")
    domain = conn.lookupByName(getVmName())
    return domain

def getConnectionString():
    return tryGetConfig('CONNSTRING')

def getVmName():
    return tryGetConfig('VMNAME')

def tryGetConfig(name):
    config = environ.get(name)
    if (config is None):
        raise Exception(f'Config <{name}> not defined')
    return config 

