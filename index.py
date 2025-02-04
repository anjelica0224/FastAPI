from fastapi import FastAPI
# from routes.route import router
from routes.mvlist_route import router
from fastapi.staticfiles import StaticFiles


app = FastAPI()
app.include_router(router, prefix="/api")
app.mount("/static", StaticFiles(directory="static"), name="static")


