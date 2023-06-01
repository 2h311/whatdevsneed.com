import os
from typing import Optional

from fastapi import APIRouter, Request, status, Form, File, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from . import htmlgen


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def get_root(request: Request, search: Optional[str] = None):
    if search:
        return templates.TemplateResponse(
            "index.html", {"request": request, "tools": htmlgen.search(search)}
        )
    # return templates.TemplateResponse(
    #     "index.html", {"request": request, "tools": htmlgen.tools("all")}
    # )
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
        },
    )


@router.get("/category/{tag}", response_class=HTMLResponse)
async def get_category(request: Request, tag: str):
    return templates.TemplateResponse(
        "index.html", {"request": request, "tools": htmlgen.tool(tag)}
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
        # Upload image
        image = str(uuid.uuid4()) + "." + image.filename.rsplit(".", 1)[1]
        img_content = image.file.read()

        # Get S3 client
        client = get_s3_client()
        # Upload
        client.put_object(
            Body=img_content,
            Bucket="cdn.whatdevsneed.com",
            key=f"img/{img_name}",
            ContentType=image.content_type,
        )
        # Set public
        client.put_object_acl(
            ACL="public-read",
            Bucket="cdn.whatdevsneed.com",
            Key=f"img/{img_name}",
        )
        # Add to database
        tools.insert(
            {
                "name": name,
                "img": f"https://cdn.whatdevsneed.com/img/{img_name}",
                "category": category,
                "staffpick": False,
                "description": description,
                "link": link,
                "pricing": pricing,
                "show": False,
            }
        )

        # Send push
        api_key = os.getenv("PUSH_TOKEN")
        title = "[wdn] New Submission"
        body = f"{name} ({category})"
        push_res = requests.post(
            f"https://push.techulus.com/api/v1/notify/{api_key}?title={title}&body={body}"
        )

        return RedirectResponse(
            url="/add?show=success", status_code=status.HTTP_303_SEE_OTHER
        )
    except:
        return RedirectResponse(
            url="/add?show=error", status_code=status.HTTP_303_SEE_OTHER
        )
