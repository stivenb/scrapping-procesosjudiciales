import asyncio 
from fastapi import APIRouter, HTTPException, status, Depends

from app.repository import web_scraping

from app.schemas.schemas import CausaJudicial
from fastapi import APIRouter, Request, FastAPI
from sqlalchemy.orm import Session, joinedload
from app.database.session import get_db
from app.database.models import models
from app.utils import get_data_authorizer

app = FastAPI(
    debug="DEBUG",
    title="WebScrapping Service",
)

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
def post_api_scrapping(request: Request, causa_judicial: CausaJudicial, db: Session = Depends(get_db), data_token=Depends(get_data_authorizer) ):
    causa_judicial = causa_judicial.dict()
    causas = web_scraping.get_all_causas(causa_judicial)
    if not causas:
        return {"status": "error", "message": "No data found for the given parameters"}
    list_scrapping = web_scraping.get_all_pages(causas)
    elements_search_causas = web_scraping.get_all_causas_search(
        causa_judicial, list_scrapping
    )
    data_details = web_scraping.generate_payload_details(elements_search_causas)
    details = asyncio.run(web_scraping.consume_api_get(data_details, "data_info_juicio"))
    for jucio in data_details:
        try:
            web_scraping.insert_juicio(jucio, db)  
        except Exception as e:
            db.rollback()
            raise Exception(f"Error inserting juicio: {str(e)}")
        finally:
            db.close()
    return {
        "causas": details,
    }
    
@router.get("/causas/{causa_id}" )
def get_causa_detail(causa_id: str, db: Session = Depends(get_db), data_token=Depends(get_data_authorizer)):
    """
    Obtener detalles de una causa por ID, con todas las relaciones asociadas.
    """
    try:
        # Realiza una consulta para obtener la causa y todas sus relaciones
        causa = (
            db.query(models.Causa)
            .options(
                joinedload(models.Causa.incidentes).joinedload(models.Incidente.litigantes),
                joinedload(models.Causa.incidentes).joinedload(models.Incidente.actuaciones),
            )
            .filter(models.Causa.idJuicio == str(causa_id))
            .first()
        )

        if not causa:
            raise HTTPException(status_code=404, detail="Causa no encontrada")

        return causa

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
app.include_router(router)