import datetime
# from app.db.mongo import db
from app.db.mongo import db
from bson import ObjectId

async def saveHistory(user_id, name, type, content, result):
    document = {
        "id_user": user_id,
        "name": name,
        "time_change": datetime.datetime.utcnow(),
        "luu": {
            "type": type,
            "content":content,
            "result": result
        }
    }
    collection = db["history"]
    await collection.insert_one(document)

async def getHistoryByUserId(user_id: str):
    collection = db["history"]
    cursor = collection.find({"id_user": user_id}).sort("time_change", -1)

    results = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])  # Chuyển ObjectId về chuỗi
        results.append(doc)
    return results


async def deleteHistoryById(id: str):
    collection = db["history"]
    result = await collection.delete_one({
        "_id": ObjectId(id)
    })
    return result
