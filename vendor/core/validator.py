from telethon.types import User
from telethon.tl.types.users import UserFull

from sfmanager import FileManager, FilesManager

from vendor.core.utils import time_string

from app import config
from vendor.misc import BASE_OPTIONS, DATA_DIR, client, FILE_NAMES

import re

generic_manager = FilesManager(level=2)

class Validator:
    access_level = 0

    filename = None

    entity = None
    full_entity = None
    data_keys = []
    full_data_keys = []

    skip_errors = None

    data_manager = None

    def __init__(self, filename: str, entity: User = None, full_entity: UserFull = None, data_keys: [] = None, full_data_keys: [] = None, access_level: int = 3, skip_errors: bool = False):
        """
        :param entity: Target user entity. Use: client.get_entity()
        :param full_entity: Target user full entity. Use: client(GetFullUserRequest(client.get_entity().id))
        :param data_keys: Keys to get data from "entity". Example ["username", "id"]
        :param full_data_keys: Keys to get data from "full_entity". Example ["about"]. DO NOT FORWARD birthday
        :param access_level: Access level for filemanager. See sfmanager docs.
        :param skip_errors: Skip errors, where possible
        :return: Int - count of inconsistencies, orr error code. Error codes start with 100, 200 etc. See error codes below
        """

        self.access_level = access_level
        self.filename = filename

        self.entity = entity
        self.full_entity = full_entity

        self.data_keys = data_keys
        self.full_data_keys = full_data_keys

        self.skip_errors = skip_errors

        print(time_string("Validator inited"))

        self.data_manager = FileManager(filename=f"{DATA_DIR}/{filename}", level=access_level)
        print(time_string(f"Filemanager inited. Filename: \"{DATA_DIR}/{filename}\", access level: {access_level}"))

    async def data_validation(self):


        # Array with data from profile

        tmp = [getattr(self.entity, key, None) for key in self.data_keys] + [
            (lambda obj, keys: None if any((obj := getattr(obj, k, None)) is None for k in keys) else obj)
            (self.full_entity.full_user, key.split(".")) if "." in key else getattr(self.full_entity.full_user, key,
                                                                                    None)
            for key in self.full_data_keys
        ]

        _birthday = self.full_entity.full_user.birthday

        if _birthday:
            tmp.append(f"{_birthday.year}.{_birthday.month:02}.{_birthday.day:02}")
        else:
            tmp.append(None)

        data = self.data_manager.readlines()

        # Сhecking the existence of a file
        if data == "Something went wrong...":
            if self.skip_errors is False:
                return 200  # File not found
            else:  # Create file
                print(time_string("Creating base-data file..."))
                generic_manager.create(f"{DATA_DIR}/{self.filename}")
                data = self.data_manager.readlines()

        # Сhecking the file for emptiness
        if len(data) == 0 or data[0] == "" or data[0] == "\n":
            print(time_string("Initialization base-data file..."))
            for _data in tmp:  # Adding data in file
                _out = self.data_manager.add(str(_data) + "\n")
                if re.search(r"Low access level! (\d+), but need (\d+)", str(_out)):
                    return 201  # Forbidden manipulation

        # Clearing transitions to a new line
        for i in range(0, len(data)):
            data[i] = data[i].replace("\n", "")

        incos_count = 0

        # Compare data in the file and data in the profile
        for i in range(min(len(tmp), len(data))):
            if str(tmp[i]) != data[i]:
                _output = time_string(f"{BASE_OPTIONS[i]}: {data[i]} > {tmp[i]}")
                await client.send_message(config.target_channel,
                                          f"Target: {config.target}\n\n{_output}")
                print(_output)
                incos_count += 1

        # Writing new data to the file
        if incos_count > 0:
            _out = self.data_manager.set("")
            if re.search(r"Low access level! (\d+), but need (\d+)", str(_out)):
                return 201  # Forbidden manipulation

            for i in range(0, len(tmp)):
             self.data_manager.add(str(tmp[i]) + "\n")

        """
        Return count of inconsistencies
        If the return value is > 100, then it's error

        Error codes:
            100 - Entity not found
            101 - Full entity not found
            102 - Forbidden request

            200 - Readable file not found
            201 - Forbidden manipulation
            202 - Invalid access level
            203 - Invalid encode
        """

        return incos_count
