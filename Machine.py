from Credentials import Credentials
from RemOpr import RemOpr


class Machine(object):

    def __init__(self, hostaddr, credentials):

        self.hostaddr = hostaddr
        self.description = ""

        self.osType = ""
        self.osRelease = ""

        self.credentials = {
            "user": credentials.user,
            "password": credentials.password,
            "domain": credentials.domain
        }

        self.ports = []
        self.services = {}

        # self.setOsTypeAndRelease()

    def setDescription(self, description):
        self.description = description

    def setOsTypeAndRelease(self):

        osType = "linux"

        if osType == "linux":

            self.osType = "linux"

            linuxRelease = RemOpr.remoteOperation("cat /etc/*release", self)

            if 'CentOS' in linuxRelease:

                self.osRelease = "CentOS"

            elif 'Red Hat' in linuxRelease:

                self.osRelease = "Red Hat"

            elif 'Ubuntu' in linuxRelease:

                self.osRelease = "Ubuntu"

    def addPort(self, port):
        self.ports.append(port)

    def removePort(self, port):
        self.ports.remove(port)

    def addService(self, serviceName, serviceState):
        self.services[serviceName] = serviceState

    def removeService(self, serviceName):
        if serviceName in self.services:
            del self.services[serviceName]

    def getCredentials(self):

        return Credentials(
            self.credentials["user"],
            self.credentials["password"],
            self.credentials["domain"]
        )

    def printMe(self):

        print "Host Address: " + self.hostaddr
        print "Description: " + self.description
        print "OS Type: " + self.osType
        print "OS Release: " + self.osRelease

        portsStr = ""
        for port in self.ports:
            portsStr += port + " "

        print "Ports: " + portsStr

        servicesStr = ""
        for service in self.services.keys():
            servicesStr += service + "(" + str(self.services[service]) + ") "

        print "Services: " + servicesStr