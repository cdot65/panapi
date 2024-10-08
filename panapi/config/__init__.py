#!/usr/bin/env python3


class PanObject:
    """
    PanObject - Base class for all resource objects

    This class defines a configuration object that can be defined in
    Palo Alto Networks Unified Cloud Manager.

    It provides basic CRUD (Create, Read, Update, Delete) operations
    and implements a payload property that can be used to send & receive data
    in JSON format.

    Attributes
    ----------
    _base_url (str)
        base url for the API calls, defaults to
        "https://api.sase.paloaltonetworks.com"

    Methods
    -------
    init(self, **kwargs)
        constructor that initializes the object with key-value pairs
        passed as kwargs.

    str(self)
        returns a string representation of the object

    create(self, session)
        creates a new resource object.

    read(self, session)
        reads an existing resource object.

    list(self, session)
        lists all resource objects of the same type.

    update(self, session)
        updates an existing resource object.

    delete(self, session)
        deletes a resource object.

    Properties
    ----------
    payload (dict)
        returns a dictionary representation of the object's attributes,
        except for 'folder' and 'id'.
    """

    _base_url = "https://api.sase.paloaltonetworks.com"

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __str__(self):
        return str(self.__dict__)

    def create(self, session):
        if session.is_expired:
            session.reauthenticate()
        url = self._base_url + self._endpoint
        headers = {"Content-Type": "application/json"}
        if hasattr(self, "folder"):
            params = {"folder": self.folder}
        else:
            params = {}
        try:
            session.response = session.post(
                url=url, headers=headers, params=params, json=self.payload
            )
        except Exception as err:
            print(err)
        else:
            if session.response.status_code == 201:
                config = session.response.json()
                self.id = config.get("id")

    def read(self, session):
        if session.is_expired:
            session.reauthenticate()
        url = self._base_url + self._endpoint
        if hasattr(self, "folder"):
            params = {"folder": self.folder}
        else:
            params = {}
        has_id = hasattr(self, "id")
        has_name = hasattr(self, "name")
        if has_id:
            url = self._base_url + self._endpoint + "/{}".format(self.id)
        elif has_name:
            params.update({"name": self.name})
        else:
            raise ValueError("name or id value is required")
        try:
            session.response = session.get(url=url, params=params)
        except Exception as err:
            print(err)
        else:
            if session.response.status_code == 200:
                result = session.response.json()
                if has_id:
                    return type(self)(**result)
                elif has_name:
                    config = result["data"][0]
                    return type(self)(**config)

    def list(self, session):
        if session.is_expired:
            session.reauthenticate()
        url = self._base_url + self._endpoint
        if hasattr(self, "folder"):
            params = {"folder": self.folder, "limit": 5000}
        else:
            params = {}
        try:
            session.response = session.get(url=url, params=params)
        except Exception as err:
            print(err)
        else:
            if session.response.status_code == 200:
                result = session.response.json()
                obj_list = []
                for config in result["data"]:
                    obj_list.append(type(self)(**config))
                return obj_list

    def update(self, session):
        if session.is_expired:
            session.reauthenticate()
        if hasattr(self, "id"):
            url = self._base_url + self._endpoint + "/{}".format(self.id)
        else:
            url = self._base_url + self._endpoint
        headers = {"Content-Type": "application/json"}
        if hasattr(self, "folder"):
            params = {"folder": self.folder}
        else:
            params = {}
        try:
            session.response = session.put(
                url=url, headers=headers, params=params, json=self.payload
            )
        except Exception as err:
            print(err)
        else:
            if session.response.status_code == 200:
                session.response.json()
            #     config = session.response.json()
            # return config

    def delete(self, session):
        if session.is_expired:
            session.reauthenticate()
        url = self._base_url + self._endpoint + "/{}".format(self.id)
        headers = {"Content-Type": "application/json"}
        if hasattr(self, "folder"):
            params = {"folder": self.folder}
        else:
            params = {}
        try:
            session.response = session.delete(
                url=url, headers=headers, params=params
            )
        except Exception as err:
            print(err)
        else:
            if session.response.status_code == 200:
                del self

    @property
    def payload(self):
        items = {k: v for k, v in self.__dict__.items()}
        return items
