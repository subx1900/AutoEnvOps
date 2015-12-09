import os
# imports for MongoDB connection
from pymongo import MongoClient
import pymongo

os.environ["MONGOHQ_URL"] = 'mongodb://envopsusr:axp1900@centos6-mongodb/envops'

# ___________________________________________________________________________________________________________


class MachineDal(object):
    def __init__(self):
        self.__connected = True
        try:
            self.__mongoClient = MongoClient(os.environ.get('MONGOHQ_URL'))
            self.__db = self.__mongoClient.envops
            # gets machines collection from db
            self.__machines_collection = self.__db.machines

        except pymongo.errors.ConnectionFailure, e:
            print "Could not connect to MongoDB: %s" % e
            self.__connected = False

    def addMachine(self, machine):

        # Create a document from the machine object
        machine_document = machine.__dict__

        # Insert the machine document into the machines collection
        machine_id = self.__machines_collection.insert(machine_document, check_keys=False)

    def updateMachine(self, s_hostaddr, u_hostaddr, u_description, u_osEnv, u_port_list, u_service_list, u_path_list):
        pass

    def delMachine(self, hostaddr):

        query = {"hostaddr": hostaddr}
        return self.__machines_collection.remove(query)

    def getAllMachines(self):
        return self.__machines_collection.find()

    def getMachine(self, hostaddr):

        query = {"hostaddr": hostaddr}
        return self.__machines_collection.find_one(query)

    def __del__(self):

        # close the connection to MongoDB
        if self.__connected:
            self.__mongoClient.close()