
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
        return uuid.uuid4().hex

    def _printDb(self):
        self.store = Store()
        result = self.store.load()
        pp = pprint.PrettyPrinter(indent=2)
        pp.pprint(self.store._store)

    def createUser(self, document):
        self.store = Store()
        result = self.store.load()
        
        result = self.store.get(document["_id"], namespace=self.namespace)

        if result["success"] == False:
            result = self.store.put(document["_id"], document, namespace=self.namespace)
            result = self.store.save()
            print(MESSAGES.USER_ADDED)
        else:
            print(MESSAGES.USER_EXISTS)
            return
        # self._printDb()

    def createFile(self, user, tags, document):
        self.store = Store()
        result = self.store.load()
        
        result = self.store.get(user, namespace=self.namespace)
        # print(result, "result")
        if result["success"] == False:
            print(MESSAGES.USER_NOT_EXISTS)
            return
        document["_id"] = self._getId()
        
        for tag in tags:
            data = self.store.get(user + "." + tag, namespace=self.namespace)
            if data["success"] == False:
                result = self.store.put(user + "." + tag, [document], namespace=self.namespace)
            else:
                data["value"].append(document)
                result = self.store.put(user + "." + tag, data["value"], namespace=self.namespace, guard=data["guard"])
        
        # result = self.store.save()
        print(MESSAGES.FILE_ADDED)
        # self._printDb()
    
    def searchUser(self, user):
        self.store = Store()
        result = self.store.load()
        result = self.store.get(user, namespace=self.namespace)
        if result["success"] == False:
            print(MESSAGES.USER_NOT_EXISTS)
            return
        print(result)

    def updateUser(self, userid, user):
        self.store = Store()
        result = self.store.load()
        if "_id" in user.keys():
            print(MESSAGES.INVALID_ID)
            return
        data = self.store.get(user, namespace=self.namespace)
        if data["success"] == False:
            print(MESSAGES.USER_NOT_EXISTS)
            return
        result = self.store.put(userid, user, namespace=self.namespace, guard=data["guard"])
        print(MESSAGES.USER_UPDATED)                


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
