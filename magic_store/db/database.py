
from ..kv_idea.store import Store
from ..constants import MESSAGES
import pprint
import uuid

class Database:
    def __init__(self, namespace=None):
        self.store = Store()
        self.namespace = namespace
        self.store.save()

    def _getId(self):
        """Generates random id for document"""
        return uuid.uuid4().hex

    def _printDb(self):
        """Prints database"""
        self.store = Store()
        result = self.store.load()
        pp = pprint.PrettyPrinter(indent=2)
        pp.pprint(self.store._store)
    
    def _getAllUserKeys(self, userKey):
        """Returns list of keys for specific user"""
        self.store = Store()
        result = self.store.load()
        
        namespace = self.namespace
        if namespace == None:
            namespace = "__default__"
        
        tags = []
        for key in self.store._store[namespace].keys():
            if key.split(".")[0] == userKey:
                tags.append(key)
        return tags


    def createUser(self, document, key):
        """Creates user in database, document is a dictionary with user data, key is a key under which user will be stored"""
        self.store = Store()
        result = self.store.load()
        
        result = self.store.get(key, namespace=self.namespace)

        if result["success"] == False:
            id = self._getId()
            document["_id"] = id
            result = self.store.put(key, document, namespace=self.namespace)
            result = self.store.save()
            print(MESSAGES.USER_ADDED)
        else:
            print(MESSAGES.USER_EXISTS)
            return
        # self._printDb()
    
    def searchUser(self, key):
        """Searches for user under specific key"""
        self.store = Store()
        result = self.store.load()
        result = self.store.get(key, namespace=self.namespace)
        if result["success"] == False:
            print(MESSAGES.USER_NOT_EXISTS)
            return
        print(result)

    def updateUser(self, key, user):
        """Updates user data, user is a dictionary with new data, key is a key under which user is stored"""
        self.store = Store()
        result = self.store.load()
        if "_id" in user.keys():
            print(MESSAGES.ID_CHANGE_NOT_ALLOWED)
            return
        data = self.store.get(key, namespace=self.namespace)
        if data["success"] == False:
            print(MESSAGES.USER_NOT_EXISTS)
            return
        id = data["value"]["_id"]
        user["_id"] = id
        result = self.store.put(key, user, namespace=self.namespace, guard=data["guard"])
        result = self.store.save()
        print(MESSAGES.USER_UPDATED)                

    def deleteUser(self, key):
        """Deletes user under specific key"""
        self.store = Store()
        result = self.store.load()
        result = self.store.get(key, namespace=self.namespace)
        if result["success"] == False:
            print(MESSAGES.USER_NOT_EXISTS)
            return

        userKeys = self._getAllUserKeys(key)
        for userKey in userKeys:
            data = self.store.get(userKey, namespace=self.namespace)
            result = self.store.delete(userKey, namespace=self.namespace, guard=data["guard"])
        
        result = self.store.save()
        print(MESSAGES.USER_DELETED)
        # self._printDb()

    def createFile(self, userKey, tags, document):
        self.store = Store()
        result = self.store.load()
        
        result = self.store.get(userKey, namespace=self.namespace)
        # print(result, "result")
        if result["success"] == False:
            print(MESSAGES.USER_NOT_EXISTS)
            return
        document["_id"] = self._getId()
        
        for tag in tags:
            data = self.store.get(userKey + "." + tag, namespace=self.namespace)
            if data["success"] == False:
                result = self.store.put(userKey + "." + tag, [document], namespace=self.namespace)
            else:
                data["value"].append(document)
                result = self.store.put(userKey + "." + tag, data["value"], namespace=self.namespace, guard=data["guard"])
        
        result = self.store.save()
        print(MESSAGES.FILE_ADDED)
        # self._printDb()

    def searchFileByTags(self, user, tags, searchType):
        self.store = Store()
        result = self.store.load()
        if searchType == "or":
            for tag in tags:
                result = self.store.get(user + "." + tag, namespace=self.namespace)
                if result['success'] == False:
                    print(MESSAGES.TAG_NOT_EXISTS, tag)
                    next
                print(result)
        elif searchType == "and":
            pass


        # elif searchType == "and":
        #     if isinstance(tags, list):
        #         dic = {}
        #         for tag in tags:
        #             for file in tag:
        #                 if dic[file["plik"]]:
        #                     dic[file["plik"]] += 1
        #                 else:
        #                     dic[file["plik"]] = 1
        #         print(dic)
