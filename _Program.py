from Credentials import Credentials
from EnvOps import EnvOps
from Machine import Machine

#mc1 = Machine("centos-apache", Credentials("subx", "axp1900", ""))
#mc1.setOsTypeAndRelease()
#mc1.setDescription("my noc server")
#mc1.addPort("443")
#mc1.addPort("80")
#mc1.addService("nagios", True)
#mc1.addService("httpd", True)
#mc1.addConfigFile("/tmp/tmp.conf", "ServerAddr=", "centos-repo")
#mc1.addConfigFile("/tmp/pmt.conf", "ServerIP=", "127.0.0.1")

myEnvOps = EnvOps()
#myEnvOps.addMachine(mc1)

#mc1.printMe()



print "-" * 100 + "\n"

print "All machines status:"
myEnvOps.getAllMachinesStatus()
