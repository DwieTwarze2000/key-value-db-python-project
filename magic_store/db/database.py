
from ..kv_idea.store import Store
from ..constants import MESSAGES
import pprint
import uuid

class Database:
    def __init__(self, namespace: str=None):
        self.store = Store()
        self.namespace = namespace
        self.store.save()

        self.FOREACH_TAG_SEARCH_TYPE = 1
        self.ALL_TAG_SEARCH_TYPE = 2

    def _getId(self):
        """Generates random id for document"""
        return uuid.uuid4().hex

    def _printDb(self):
        """Prints database"""
        self.store = Store()
        result = self.store.load()
        pp = pprint.PrettyPrinter(indent=2)
        pp.pprint(self.store._store)
    
    def _getAllUserKeys(self, userKey: str):
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


    def createUser(self, document: dict, key: str):
        """
        Creates user in database \n
        Document is a dictionary with user data \n
        Key is a key under which user will be stored
        """
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
    
    def searchUser(self, key: str):
        """Searches for user under specific key"""
        self.store = Store()
        result = self.store.load()
        result = self.store.get(key, namespace=self.namespace)
        if result["success"] == False:
            print(MESSAGES.USER_NOT_EXISTS)
            return
        print(result)

    def updateUser(self, key:str, user:dict):
        """
        Updates user data \n
        User is a dictionary with new data \n
        Key is a key under which user is stored
        """
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

    def deleteUser(self, key: str):
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

    def createFile(self, userKey:str, tags:list, document:dict):
        """
        Creates file for specific user \n
        Tags is a list of tags under which file will be stored \n
        Document is a dictionary with file data"""
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

    def searchFileByTags(self, userKey:str, tags:list, searchType:int):
        """
        Searches for file under specific tags \n
        Tags is a list of tags \n
        SearchType is a type of search, can be "FOREACH TAG SEARCH"-1 or "ALL TAGS SEARCH"-2 
        """
        self.store = Store()
        result = self.store.load()
        if searchType == 1:
            for tag in tags:
                result = self.store.get(userKey + "." + tag, namespace=self.namespace)
                if result['success'] == False:
                    print(MESSAGES.TAG_NOT_EXISTS)
                    next
                else:
                    print("tag =",tag, result)
        elif searchType == 2:
            files = {}
            for tag in tags:
                data = self.store.get(userKey + "." + tag, namespace=self.namespace)
                if data['success'] == False:
                    print(MESSAGES.TAG_NOT_EXISTS)
                    return
                for file in data["value"]:
                    if file["_id"] in files.keys():
                        files[file["_id"]]["count"] += 1
                    else:
                        files[file["_id"]] = {
                            "count": 1,
                            "file": file
                        }
            result = []
            for file in files.values():
                if file["count"] == len(tags):
                    result.append(file["file"])
            print(MESSAGES.FILES_FOUND)
            print(result) 

    def deleteTag(self, userKey:str, tag:str):
        """Deletes tag under specific user"""
        
        self.store = Store()
        result = self.store.load()
        result = self.store.get(userKey + "." + tag, namespace=self.namespace)
        if result["success"] == False:
            print(MESSAGES.TAG_NOT_EXISTS)
            return

        result = self.store.delete(userKey + "." + tag, namespace=self.namespace, guard=result["guard"])
        result = self.store.save()
        print(MESSAGES.TAG_DELETED)
        # self._printDb()

    def deleteFileFromTag(self, userKey:str, tag:str, fileName:str):
        """Deletes file from specific tag"""
        self.store = Store()
        result = self.store.load()
        result = self.store.get(userKey + "." + tag, namespace=self.namespace)
        if result["success"] == False:
            print(MESSAGES.TAG_NOT_EXISTS)
            return
        files = result["value"]
        for file in files:
            if file["plik"] == fileName:
                files.remove(file)
                result = self.store.put(userKey + "." + tag, files, namespace=self.namespace, guard=result["guard"])
                result = self.store.save()
                print(MESSAGES.FILE_DELETED)
                return
        print(MESSAGES.FILE_NOT_EXISTS)
        return

    def deleteFileFromAllTags(self, userKey:str, fileName:str):
        """Deletes file from all tags under specific user"""
        count = 0
        self.store = Store()
        result = self.store.load()
        result = self.store.get(userKey, namespace=self.namespace)
        if result["success"] == False:
            print(MESSAGES.USER_NOT_EXISTS)
            return
        userKeys = self._getAllUserKeys(userKey)
        for key in userKeys:
            if key == userKey:
                continue
            data = self.store.get(key, namespace=self.namespace)
            
            if data["success"] == False:
                continue
            
            files = data["value"]
            for file in files:
                if file["plik"] == fileName:
                    files.remove(file)
                    result = self.store.put(key, files, namespace=self.namespace, guard=data["guard"])
                    result = self.store.save()
                    count += 1
        if count == 0:
            print(MESSAGES.FILE_NOT_EXISTS)
            return
        print(MESSAGES.FILE_DELETED, "from {} tags".format(count))

    def addTagToFile(self, user: str, newTag: str, fileId: str):
        """Adding new Tag to existing File"""
        self.store = Store()

        result = self.store.load()
        result = self.store.get(user, namespace=self.namespace)
        if result["success"] == False:
            print(MESSAGES.USER_NOT_EXISTS)
            return

        userKeys = self._getAllUserKeys(user)

        for key in userKeys:
            if key == user:
                continue

            result = self.store.get(key, namespace=self.namespace)

            files = result["value"]

            for file in files:
                if file["_id"] == fileId:
                    data = self.store.get(user+"."+newTag, namespace=self.namespace)
                    if data["success"] == False:
                        result = self.store.put(user + "." + newTag, [file], namespace=self.namespace)
                        self.store.save()
                        print(MESSAGES.TAG_ADDED)
                        return
                    else:
                        data["value"].append(file)
                        result = self.store.put(user + "." + newTag, data["value"], namespace=self.namespace, guard=data["guard"])
                        self.store.save()
                        print(MESSAGES.TAG_ADDED)
                        return
