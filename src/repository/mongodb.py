from pymongo import MongoClient


class MongoRepository:
    """
    Класс для работы с базой данных MongoDB
    """
    def __init__(self, host, port, database, collection):
        self.collection = MongoClient(host, port)[database][collection]

    def get_one(self, item_id):
        """
        Получение одной записи из базы по id
        """
        result = self.collection.find_one({'_id': item_id})
        return result

    def upsert(self, shortmodel):
        """
        Вставка/обновление записи в базе (update+insert=upsert)
        """
        self.collection.update_one({
            '_id': shortmodel['_id']
        }, {
            '$set': {'status': shortmodel['status']}
        }, True)

