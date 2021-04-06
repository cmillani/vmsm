from flask import Blueprint
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

def parseVmPowerActionError(error):
    if (not error):
        return 'OK'
    else:
        return error, 500


def getDomain():
    global conn
    if(conn == None or not conn.isAlive()):
        print("Connecting to remote QEMU")
        # TODO: KEYFILE should be env var to be configurable from docker
        conn = libvirt.open('qemu+ssh://carlos@192.168.1.6/system?keyfile=/home/carlos/.ssh/id_rsa')
        print("Connected!")
    # TODO: Name should be env var
    domain = conn.lookupByName('debtest')
    return domain

