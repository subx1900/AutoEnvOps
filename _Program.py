from Credentials import Credentials
from EnvOps import EnvOps
from Machine import Machine

'''
mc1 = Machine("RHEL-Nagios", Credentials("subx", "axp1900", ""))
mc1.setOsTypeAndRelease()
mc1.setDescription("my noc server")
mc1.addPort("8140")
mc1.addPort("80")
mc1.addService("nagios", True)
mc1.addService("httpd", False)
'''

myEnvOps = EnvOps()
#myEnvOps.addMachine(mc1)

print "-" * 100 + "\n"

print "All machines status:"

myEnvOps.getAllMachinesStatus()
