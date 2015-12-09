import cStringIO
# my classes imports
from Credentials import Credentials
from Machine import Machine
from MachineDal import MachineDal
from RemOpr import RemOpr
# imports for port checking
import socket
import sys


class EnvOps(object):
    def __init__(self):
        self.__machines = []

        self.mcDal = MachineDal()

        for machineDoc in self.mcDal.getAllMachines():

            crd = Credentials(
                machineDoc["credentials"]["user"],
                machineDoc["credentials"]["password"],
                machineDoc["credentials"]["domain"])

            tmpMc = Machine(machineDoc["hostaddr"], crd)

            tmpMc.setDescription(machineDoc["description"])

            tmpMc.osType = machineDoc["osType"]
            tmpMc.osRelease = machineDoc["osRelease"]

            for port in machineDoc["ports"]:
                tmpMc.addPort(port)

            services = machineDoc["services"]

            for service in services.keys():
                tmpMc.addService(service, services[service])

            configs = machineDoc["configs"]

            for configKey in configs.keys():
                key = configs[configKey][0]
                value = configs[configKey][1]
                tmpMc.addConfigFile(configKey, key, value)

            self.__machines.append(tmpMc)

    def __getMachineObj(self, hostaddr):

        if hostaddr in self.__machines:
            return self.__machines[hostaddr]

    def __getFreeRam(self, machineObj):
        return int(
            RemOpr.remoteOperation("cat /proc/meminfo | grep MemAvailable | awk '{ print $2 }'", machineObj)) / 1024

    def __getRamSize(self, machineObj):
        return int(RemOpr.remoteOperation("awk '/^Mem/ {print($2);}' <(free -m)", machineObj))
        # return self.__RemOpr.remoteOperation("cat /proc/meminfo | grep MemTotal | awk '{ print $2 }'")

    def __getFreeOS(self, machineObj):

        oprRes = RemOpr.remoteOperation("df -h / | awk '{ print $4 }'", machineObj)

        if oprRes:
            for line in cStringIO.StringIO(oprRes):
                str = line

            return float(str[:len(str) - 1])
        else:
            return 0

    def __getOSdriveSize(self, machineObj):

        oprRes = RemOpr.remoteOperation("df -h / | awk '{ print $2 }'", machineObj)

        if oprRes:

            str = cStringIO.StringIO(oprRes).readlines()[1]

            return float(str[:len(str) - 1])
            # return int(cStringIO.StringIO(oprRes).readlines()[1][:len(cStringIO.StringIO(oprRes).readlines()[1]) - 1])
        else:
            return 0

    def __checkPort(self, hostaddr, port):

        try:
            remoteServerIP = socket.gethostbyname(hostaddr)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((remoteServerIP, port))
            sock.close()

        except KeyboardInterrupt:
            print "You pressed Ctrl+C"
            sys.exit()

        except socket.gaierror:
            print 'Hostname could not be resolved. Exiting'
            sys.exit()

        except socket.error:
            print "Couldn't connect to server"
            sys.exit()

        if result == 0:
            '''print "Port {}: \t Open".format(port)'''
            return True
        else:
            return False

    def __FixPort(self, hostaddr, port):
        pass

    def __checkService(self, machineObj, serviceName):

        if machineObj.osType == "linux":

            if (machineObj.osRelease == 'CentOS') or (machineObj.osRelease == 'Red Hat'):

                serviceStatus = RemOpr.remoteOperation("service " + serviceName + " status | grep Active", machineObj)

                if 'active (running)' in serviceStatus:

                    return True
                else:
                    return False

            elif machineObj.osRelease == 'Ubuntu':
                print "not yet checkable"

        elif machineObj.osType == "windows":
            print "not yet checkable"

    def __FixService(self, hostaddr, serviceName, serviceState):
        pass

    def __FixSampleConfigFile(self):
        pass

    def __getMachineStatus(self, machineObj):

        # check for RAM and OS drive status

        print "RAM: %sMB Free of %sMB" % (self.__getFreeRam(machineObj), self.__getRamSize(machineObj))

        print "OS Drive: %sGB Free of %sGB" % (self.__getFreeOS(machineObj), self.__getOSdriveSize(machineObj))

        # check for machine ports status

        portsStatus = "Ports: "

        for port in machineObj.ports:
            if self.__checkPort(machineObj.hostaddr, int(port)):
                portsStatus += port + "(listening)"
            else:
                portsStatus += port + "(closed)"

            portsStatus += " "

        print portsStatus

        # check for machine services status

        services = machineObj.services

        servicesStatus = "Services: "

        for serviceName in services.keys():

            desiredServiceState = services[serviceName]
            currentServiceState = self.__checkService(machineObj, serviceName)

            if desiredServiceState == currentServiceState:

                servicesStatus += serviceName + "(Running)"
            else:
                servicesStatus += serviceName + "(Stopped)"

            servicesStatus += " "

        print servicesStatus + "\n"

    def __FixMachine(self, machineObj):
        pass

    def rebootMachine(self, hostaddr):
        RemOpr.remoteOperation("reboot", hostaddr)

    def getAllMachinesStatus(self):

        for machineObj in self.__machines:
            machineObj.printMe()
            self.__getMachineStatus(machineObj)

    def printAllMachines(self):

        for machineObj in self.__machines:
            machineObj.printMe()

    def FixAllMachines(self):
        pass

    def addMachine(self, machineObj):

        self.mcDal.addMachine(machineObj)
        self.__machines.append(machineObj)

    def removeMachine(self, hostaddr):

        self.mcDal.delMachine(hostaddr)
        self.__machines.remove(self.__getMachineObj(hostaddr))
