from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.services.HistoryServices import saveHistory, getHistoryByUserId, deleteHistoryById
from app.dependencies.auth import get_current_user

router = APIRouter()

class SaveHistoryInput(BaseModel):
    name: str
    type: str
    sequence: str
    result: str

class DeleteInput(BaseModel):
    id: str

@router.post("/saveLS")
async def save_history(
    data: SaveHistoryInput,
    current_user: dict = Depends(get_current_user)
):
    await saveHistory(current_user["_id"], data.name, data.type, data.sequence, data.result)
    return {"status": "ok"}

@router.post("/getLS")
async def get_history(
    current_user: dict = Depends(get_current_user)
):
    data = await getHistoryByUserId(current_user["_id"])
    return {"data": data}

@router.post("/delete")
async def delete_history(data: DeleteInput, current_user: dict = Depends(get_current_user)):
    result = await deleteHistoryById(data.id)
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Không tìm thấy hoặc không có quyền xoá.")
    return {"status": "ok"}
