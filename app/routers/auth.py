from app.database.session import get_db
from app.utils import Hasher as Hash
from app.utils import generate_token
from fastapi import APIRouter, status, Depends, HTTPException, FastAPI
from app.schemas.schemas import UserSignin
from sqlalchemy.orm import Session 
from app.database.models import models


app = FastAPI(
    debug="DEBUG",
    title="Auth Service",
)
 
router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post(
    "/signin",
    status_code=status.HTTP_200_OK,
)
async def signin( 
    credentials: UserSignin,
    db: Session = Depends(get_db),
):
    """
    Permite que un usuario inicie sesión en el sistema.

    :param request: La solicitud HTTP recibida.
    :type request: Request
    :param credentials: Las credenciales de inicio de sesión proporcionadas por el usuario.
    :type credentials: schema_users.UserSignin
    :param db: Una sesión de base de datos.
    :type db: Session
    :return: Una respuesta que indica el éxito del inicio de sesión.
    :rtype: dict
    """
    try:
        user =  (
            db.query(models.User)
            .filter(models.User.email == credentials.signin_username)
            .first()
            ) 
        is_verified = Hash.verify_password(credentials.signin_value, user.password)
        if not is_verified:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials. Please check your username or password.",
            )
        data_format = { 
            "user_id": user.id,
            "email": user.email,
        }
        token = generate_token(data_format)
        data_format["token"] = token
    except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail= f"error generating token {str(e)}",
            ) 
    return data_format 

app.include_router(router)