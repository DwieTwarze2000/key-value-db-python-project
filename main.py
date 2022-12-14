import pprint
import uuid
from magic_store.kv_idea.store import Store


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

def createDefaultDB():
    store = Store()
    #dokumenty
    user1 = {
        "_id": "id1",
        "imie": "Pawel",
        "nazwisko": "Binkowski",
        "login": "pawel123"
    }
    tag1 = [
        {
            "_id": getId(),
            "plik": "test1.txt",
            "path": "C:\\Users\\osiolek\\Desktop\\test1.txt",
        },
        {
            "_id": getId(),
            "plik": "test2.txt",
            "path": "C:\\Users\\osiolek\\Desktop\\test2.txt",
        },
    ]
    tag2 = [{
        "_id": getId(),
        "plik": "test1.txt",
        "path": "C:\\Users\\osiolek\\Desktop\\test1.txt",
    }]
    result = store.put("id1", user1, namespace="baza1")
    result = store.put("id1.tag1", tag1, namespace="baza1")
    result = store.put("id1.tag2", tag2, namespace="baza1")
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(store._store)
    result = store.save()
    # print(result)


def searchUser(user):
    store = Store()
    result = store.load()

    result = store.get(user, namespace="baza1")

    # print(result)


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
        
def getId():
    return uuid.uuid4().hex


def addNewDocument(user, tags, document):
    store = Store()
    result = store.load()
    result = store.get(user, namespace="baza1")
    if result["code"] == 203:
        print("User is not existing!")
        return
    for tag in tags:
        document["_id"] = getId()
        data = store.get(user + "." + tag, namespace="baza1")
        if data["code"] == 203:
            result = store.put(user+ "." + tag, [document], namespace="baza1")
        else:
            docs = data["value"]
            docs.append(document)
            result = store.put(user + "." + tag, docs, namespace="baza1", guard=data["guard"])

        pp = pprint.PrettyPrinter(indent=2)
        pp.pprint(store._store)
        result = store.save()
    # print(result)

def addUser(document): 
    store = Store()
    result = store.load()
    result = store.put(document["_id"], document, namespace="baza1")
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(store._store)
    result = store.save()
    # print(result)


if __name__ == '__main__':
    createDefaultDB()
    # searchUser("pawel123")
    testDoc = {
        "plik": "test777.txt",
        "path": "C:\\Users\\osiolek\\Desktop\\test4.txt",
    }
    addNewDocument("id1", ["test1","test2","tag1"], testDoc)

    user2 = {
        "_id": "id2",
        "imie": "Jan",
        "nazwisko": "Kowalski",
        "login": "jan123"
    }
    addUser(user2)

    addNewDocument("id2", ["HEHE", "swieta2922"], testDoc)
    # searchType = "and"

    # searchByTag("id1", ["tag1", "tag2", "tag3", "test"], searchType)

# dodac mozliwość wyszukiwania po kilku tagach
#dodac dodawanie
