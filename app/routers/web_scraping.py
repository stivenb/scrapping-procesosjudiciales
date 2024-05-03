import asyncio 
from fastapi import APIRouter, HTTPException, status, Depends

from app.repository import web_scraping

from app.schemas.schemas import CausaJudicial
from fastapi import APIRouter, Request 
from sqlalchemy.orm import Session
from app.database.session import get_db
 

router = APIRouter(prefix="/web_scraping", tags=["web_scraping"])


@router.get("/test", status_code=status.HTTP_200_OK)
def test():
    try:
        print("HOLA")
    except HTTPException as e:
        raise e
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return "test"

@router.post("/", status_code=200)
def post_api_scrapping(request: Request, causa_judicial: CausaJudicial, db: Session = Depends(get_db), ):
    causa_judicial = causa_judicial.dict()
    causas = web_scraping.get_all_causas(causa_judicial)
    if not causas:
        return {"status": "error", "message": "No data found for the given parameters"}
    list_scrapping = web_scraping.get_all_pages(causas)
    elements_search_causas = web_scraping.get_all_causas_search(
        causa_judicial, list_scrapping
    )
    data_details = web_scraping.generate_payload_details(elements_search_causas)
    datails = asyncio.run(web_scraping.consume_api_get(data_details, "data_info_juicio"))
    web_scraping.insert_juicio(datails, db)
    return {
        "causas": datails,
    }