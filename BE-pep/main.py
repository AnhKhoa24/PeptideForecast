from fastapi import FastAPI, Depends
from app.api.routes import auth, user, peptide3d, classification, history
from fastapi.middleware.cors import CORSMiddleware
from app.dependencies.auth import get_current_user
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(user.router, prefix="/user", tags=["user"])
app.include_router(peptide3d.router, prefix="/ai", tags=["ai"])
app.include_router(classification.router, prefix="/ai", tags=["ai"])
app.include_router(history.router, prefix="/access", tags=["access"],dependencies=[Depends(get_current_user)])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
