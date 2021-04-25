from flask import Blueprint, request
from os import environ
import libvirt

videogame_route = Blueprint('videogame', __name__)
conn = None

@videogame_route.route('/videogame', methods=['POST'])
def turnGameOn():
    body = request.get_json()
    isActive = body["active"]

    domain = getDomain()
    error = None
    if isActive:
        error = domain.create()
        print("Turn ON")
    else:
        error = domain.shutdown()
        print("Turn OFF")
    
    return parseVmPowerActionError(error)


@videogame_route.route('/videogame', methods=['GET'])
def getVmStatus():
    domain = getDomain()
    isActive = domain.isActive()
    return {"is_active": isActive == 1}, 200

def parseVmPowerActionError(error):
    if (not error):
        return 'OK'
    else:
        print(error)
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

