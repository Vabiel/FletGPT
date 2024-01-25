import json
import sqlite3

from src.local_storage.db import DB

class UserSettingsProvider:

    def __init__(self, db: DB):
        self.db = db
        self.db_file = self.db.db_file

    def get_all(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT key, value, type FROM user_settings")
        result = cursor.fetchall()
        settings = {}
        for key, value, type in result:
            settings[key] = value
        conn.close()
        return settings

    def get_str(self, key:str) -> str:
        return self.__get_setting(key)
    
    def set_str(self, key:str, value:str):
         return self.__set_setting(key, value, __Type.STR)
     
    def get_int(self, key:str) -> int:
        return self.__get_setting(key)
    
    def set_int(self, key:str, value:int):
         return self.__set_setting(key, value, __Type.INT)
     
    def get_bool(self, key:str) -> bool:
        return self.__get_setting(key)
    
    def set_bool(self, key:str, value:bool):
         return self.__set_setting(key, value, __Type.BOOL) 

    def __get_setting(self, key:str):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT value, type FROM user_settings WHERE key = ?", (key,))
        result = cursor.fetchone()
        if result is None:
            return None
        value, type = result
        if type == __Type.INT:
            return int(value)
        elif type == __Type.STR:
            return str(value)
        elif type == __Type.BOOL:
            return bool(value)
        elif type == __Type.FLOAT:
            return float(value)
        elif type == __Type.JSON:
            return json.loads(value)
        else:
            return value

    def __set_setting(self, key:str, value, type:str):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO user_settings (key, value, type) VALUES (?, ?, ?)", (key, value, type))
        conn.commit()
        conn.close()

class __Type:
    INT = "int"
    STR = "str"
    BOOL = "bool"
    FLOAT = "float"
    JSON = "json"
