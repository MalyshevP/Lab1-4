import pymongo
from bson import ObjectId

from .base import GetView, PostView

# подключение к локальному MongoDB
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# подключение к БД 
mydb = myclient["students"]
# подключение к коллекции (таблице)
mycol = mydb["students"]


# класс для чтения всех записей из БД
class ReadAll(GetView):
    ENDPOINT = "/read"

    def compute(self):
        print("Retriving all data from DB")
        data = list(mycol.find({}))
        for element in data:
            element['_id'] = str(element['_id'])
        return {"collection": data}


# класс для записи нового поля в БД
class Write(PostView):
    ENDPOINT = "/write"

    def compute(self):
        print("Writing data to DB")
        document = {
            "last_name": self._from_body("last_name"),
            "first_name": self._from_body("first_name"),
            "middle_name": self._from_body("middle_name"),
            "age": self._from_body("age"),
            "sex": self._from_body("sex"),
            "id": self._from_body("id")
        }
        status = mycol.insert_one(document)
        if (status.inserted_id):
            return {"status": "OK"}
        else:
            return {"status": "Fail"}

# удаление строки из бд
class Delete(PostView):
    ENDPOINT = "/delete"

    def compute(self):
        print("Deleting item from DB")
        db_id = ObjectId(self._from_body("db_id"))
        remove_query = {"_id": db_id}
        mycol.delete_one(remove_query)
        return {"status": "OK"}
    

# удаление всех записей из бд
class Purge(GetView):
    ENDPOINT = "/purge"

    def compute(self):
        print("Removing all data from DB")
        mycol.drop()
        return {"status": "OK"}