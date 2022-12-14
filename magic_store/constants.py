class MESSAGES:
    INCORRECT_NAMESPACE_CODE = 202
    INCORRECT_TYPE_CODE = 207
    INCORRECT_GUARD_CODE = 205
    INCORRECT_KEY_CODE = 203
    USER_EXISTS_CODE = "0x01"
    USER_NOT_EXISTS_CODE = "0x02"
    TAG_NOT_EXISTS_CODE = "0x03"

    OK_CODE = 100 #przyjmujemy dowolną wartość
    USER_ADDED_CODE = "1x01"
    FILE_ADDED_CODE = "1x02"

    INCORRECT_NAMESPACE = {"code": INCORRECT_NAMESPACE_CODE, "success": False, "description": "Incorrect (nonexisting) namespace"}
    INCORRECT_TYPE = {"code": INCORRECT_TYPE_CODE, "success": False, "description": "Incorrect type"}
    INCORRECT_GUARD = {"code": INCORRECT_GUARD_CODE,  "success": False,"description": "Incorrect guard"}
    INCORRECT_KEY = {"code": INCORRECT_KEY_CODE, "success": False, "description": "Incorrect key"}
    USER_EXISTS = {"code": USER_EXISTS_CODE, "success": False, "description": "User already exists"}
    USER_NOT_EXISTS = {"code": USER_NOT_EXISTS_CODE, "success": False, "description": "User does not exist"}
    TAG_NOT_EXISTS = {"code": TAG_NOT_EXISTS_CODE, "success": False, "description": "Tag does not exist"}


    OK = {"code": OK_CODE, "success": True, "description": "OK"}
    USER_ADDED = {"code": USER_ADDED_CODE, "success":True, "description": "User added successfully"}
    FILE_ADDED = {"code": FILE_ADDED_CODE, "success":True, "description": "File added successfully"}

    @classmethod
    def ok(cls, value, guard):
        result = cls.OK.copy()
        result["value"] = value
        result["guard"] = guard
        return result