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
    new_doc = []
    for doc in documents:
        print(doc["_id"])
        new_doc.append({
            "id" : doc['_id'],
            "name" : doc['name'],
            "time_taken" : doc["time_taken"],
            "emojis_used" : doc["emojis_used"]
        })
    print(new_doc)    
    return templates.TemplateResponse(
        request=request, name="index.html", context={"new_doc": new_doc}
    )


# @router.post("/submit-score", response_class = HTMLResponse)

