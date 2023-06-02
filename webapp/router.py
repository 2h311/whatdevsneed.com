import os
from typing import Optional

import requests
from cloudinary.uploader import upload
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import APIRouter, Request, status, Form, File, UploadFile

from . import htmlgen
from db.detabase import db_document


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def get_root(request: Request, search: Optional[str] = None):
    if search:
        return templates.TemplateResponse(
            "index.html", {"request": request, "tools": htmlgen.search(search)}
        )
    return templates.TemplateResponse(
        "index.html", {"request": request, "tools": htmlgen.tools("all")}
    )


@router.get("/category/{tag}", response_class=HTMLResponse)
async def get_category(request: Request, tag: str):
    return templates.TemplateResponse(
        "index.html", {"request": request, "tools": htmlgen.tools(tag)}
    )


@router.get("/about", response_class=HTMLResponse)
async def get_about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})


@router.get("/help", response_class=HTMLResponse)
async def get_help(request: Request):
    return templates.TemplateResponse("help.html", {"request": request})


@router.get("/add", response_class=HTMLResponse)
async def get_add(request: Request, show: Optional[str] = None):
    if show == "success":
        alert = htmlgen.alert("add-success")
    elif show == "error":
        alert = htmlgen.alert("add-error")
    else:
        alert = """"""
    return templates.TemplateResponse(
        "add.html",
        {"request": request, "alert": alert, "options": htmlgen.category_options()},
    )


@router.post("/add/submit")
async def post_add_submit(
    name: str = Form(...),
    category: str = Form(...),
    description: str = Form(...),
    image: UploadFile = File(...),
    link: str = Form(...),
    pricing: str = Form(...),
):
    try:
        # push image to cloudinary
        cloudinary_response = upload(
            image.file.read(), public_id=name, folder="whatdevsneed"
        )
        # Add to database
        db_document.insert(
            {
                "name": name,
                "img": cloudinary_response.get("secure_url"),
                "category": category,
                "staffpick": False,
                "description": description,
                "link": link,
                "pricing": pricing,
                "show": False,
            }
        )

        # Send push
        token = os.getenv("push_token")
        title = "[wdn] New Submission"
        body = f"{name} ({category})"
        push_res = requests.post(
            f"https://push.techulus.com/api/v1/notify/{token}?title={title}&body={body}"
        )
        return RedirectResponse(
            url="/add?show=success", status_code=status.HTTP_303_SEE_OTHER
        )
    except:
        return RedirectResponse(
            url="/add?show=error", status_code=status.HTTP_303_SEE_OTHER
        )
