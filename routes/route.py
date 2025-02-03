from fastapi import APIRouter, Request, HTTPException
from models.user import User
from config.db import get_database
from fastapi.responses import HTMLResponse
from templates.template import templates
from typing import List


router = APIRouter()
db = get_database()


@router.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    documents = db.scores.find({})
    for doc in documents:
        print(doc["_id"])
    return templates.TemplateResponse(
        request=request, name="index.html"
    )

# @router.post("/submit-score", response_class = HTMLResponse)
