from fastapi import Header, HTTPException
from app.core.security import verify_jwt_token
from app.db.mongo import db

async def get_current_user(token: str = Header(...)):
    email = verify_jwt_token(token)
    if not email:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = await db["users"].find_one({"email": email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user["_id"] = str(user["_id"])  # convert ObjectId to string
    return user