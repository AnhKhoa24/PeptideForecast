from app.db.mongo import db

async def get_or_create_user(user_info):
    users = db["users"]
    email = user_info.get("email")
    user = await users.find_one({"email": email})
    if not user:
        user = {
            "email": email,
            "name": user_info.get("name"),
            "picture": user_info.get("picture")
        }
        await users.insert_one(user)
    return user
