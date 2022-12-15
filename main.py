import pprint
import uuid
from magic_store.kv_idea.store import Store
from magic_store.db.database import Database

def test():
    store = Store()
    result = store.put("key1", "test text")
    result = store.put("key1", "test text 2", namespace="osiolek")
    result = store.put("key1", "nierozwazna czynnosc")

    x = store.get("key1", namespace="osiolek")
    print(x)
    result = store.delete("key1", namespace="osiolek", guard=x["guard"])
    result = store.put("key1","def", namespace="osiolek")
    # result = store.put("key1", "xxxxxxxxxxxxxxx", guard=x["guard"])

    print(result)
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(store._store)

    result = store.save()
    print(result)


def testLoad():
    store = Store()
    result = store.load()
    print(result)
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(store._store)


def searchByTag(user, tags, searchType):
    store = Store()
    result = store.load()
    
    if searchType == "or":
        if isinstance(tags, list):
            for tag in tags:
                result = store.get(user + "." + tag, namespace="baza1")
                if result['code'] == 203:
                    print("there is no tag", tag)
                    next
                print(result)
        else:
            result = store.get(user + "." + tags, namespace="baza1")
            if result["code"] == 203:
                print("there is no tag", tags)

    elif searchType == "and":
        if isinstance(tags, list):
            dic = {}
            for tag in tags:
                for file in tag:
                    if dic[file["plik"]]:
                        dic[file["plik"]] += 1
                    else:
                        dic[file["plik"]] = 1
            print(dic)

if __name__ == '__main__':

    database = Database()

    user = {
        "imie": "Pawel",
        "nazwisko": "Binkowski",
        "login": "pawel123"
    }
    database.createUser(user, "id1")
    database.searchUser("id1")
    userUpdate = {
        "imie": "Pawelek",
        "nazwisko": "Binkowski",
        "login": "pawel123456",
    }
    database.updateUser("id1", userUpdate)
    # database.deleteUser("id1")
    file1 = {
        "plik": "morze.jpg",
        "path": "C:\\Users\\osiolek\\Desktop\\morze.jpg",
    }
    file2 = {
        "plik": "latarnia_morska.jpg",
        "path": "C:\\Users\\osiolek\\Desktop\\latarnia_morska.jpg",
    }
    file3 = {
        "plik": "zgierz.jpg",
        "path": "C:\\Users\\osiolek\\Desktop\\zgierz.jpg",
    }
    file4 = {
        "plik": "arduinoProject.cpp",
        "path": "C:\\Users\\osiolek\\Desktop\\arduinoProject.cpp",
    }

    database.createFile("id1", ["morze", "wakacje2022"], file1)
    database.createFile("id1", ["morze", "wakacje2022"], file2)
    database.createFile("id1", ["zgierz", "wakacje2022"], file3)
    database.createFile("id1", ["school"], file4)
    database.createFile("asdasdasd", ["scl"], file4)
    database.deleteUser("id1")

    # database.searchFileByTags("id1", ["morze", "wakacje2022"], "or")
    
# dodac mozliwość wyszukiwania po kilku tagach