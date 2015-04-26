# imports for remote machine operations
from fabric.api import run, env, cd
from fabric.context_managers import hide, settings
from fabric.exceptions import NetworkError


class RemOpr():
    def __init__(self):
        pass

    @staticmethod
    def remoteOperation(remopr, machineObj):
        """
            :rtype : the result of remote operation
        """
        try:
            crd = machineObj.getCredentials()

            with settings(hide('warnings', 'running', 'stdout', 'stderr'), warn_only=True):
                # with hide('output', '', ''):
                env.user = crd.user
                env.password = crd.password

                env.host_string = machineObj.hostaddr
                result = run(remopr)
        except NetworkError:
            print "There is a network connection failure to %s" % env.host_string
            return 0
        else:
            return result

    @staticmethod
    def remoteOperations(wdir, remoprs):
        with cd(wdir):
            for remopr in remoprs:
                print run(remopr)