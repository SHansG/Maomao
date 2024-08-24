
from typing import AnyStr
import json
import os
from pymongo import MongoClient
from addons import Settings, TOKENS
from db.auto_create_db import create_db

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

#--- API Keys ---
tokens = TOKENS()

#--- DB connection check ---
try:
    mongodb = MongoClient(host=tokens.mongodb_url)
    mongodb.server_info()
    if tokens.mongodb_name not in mongodb.list_database_names():
        print(f"{tokens.mongodb_name} does not exist in your mongodb")
        # assuming you have already configured mongodb below function should work just fine
        create_db(mongodb, tokens.mongodb_name)
        # TODO: create database
    print("Succesfully connected to MongoDB!")
except Exception as e:
    raise Exception("Not able to connect MongoDB! Reason:", e)

SETTINGS_DB = mongodb[tokens.mongodb_name]['Settings']

# check for settings.json
if not os.path.exists(os.path.join(ROOT_DIR, "settings.json")):
    raise Exception("No settings file!")

#  cache var
settings: Settings
GUILD_SETTINGS: dict[int,dict[str,AnyStr]] = {}

def get_settings(guild_id:int) -> dict:
    settings_dict = GUILD_SETTINGS.get(guild_id, None)
    if not settings_dict:
        settings_dict = SETTINGS_DB.find_one({"_id":guild_id})
        if not settings_dict:
            SETTINGS_DB.insert_one({**{"_id":guild_id},**settings.settings_dict})
            settings_dict = settings.settings_dict
        GUILD_SETTINGS[guild_id] = settings_dict or {}
    return settings_dict

def update_settings(guild_id:int, data: dict, mode="set") -> bool:
    settings_dict = get_settings(guild_id)

    for key, value in data.items():
        if settings_dict.get(key) != value:
            match mode:
                case "set":
                    GUILD_SETTINGS[guild_id][key] = value
                case "unset":
                    GUILD_SETTINGS[guild_id].pop(key)
                case _:
                    return False
    
    result = SETTINGS_DB.update_one({"_id":guild_id}, {f"${mode}":data})
    return result.modified_count > 0

def open_json(path: str) -> dict:
    try:
        with open(os.path.join(ROOT_DIR, path), encoding="utf8") as json_file:
            return json.load(json_file)
    except:
        return {}

def update_json(path: str, new_data: dict) -> None:
    data = open_json(path)
    if not data:
        return
    
    data.update(new_data)

    with open(os.path.join(ROOT_DIR, path), "w") as json_file:
        json.dump(data, json_file, indent=4)

def init() -> None:
    global settings
    json = open_json("settings.json")
    if json is not None:
        settings = Settings(json)