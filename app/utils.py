import requests
import time
import jwt
import secrets
import string
import traceback
from passlib.context import CryptContext
from starlette.requests import Request
from fastapi import HTTPException
from app.settings import SECRET_KEY

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class MakeRequestSync:
    @staticmethod
    def make_request_post(url, headers, data):
        """
        Make a request post
        """
        retry = 5
        while True:
            try:
                response = requests.post(url, headers=headers, json=data)
                return response
            except Exception as e:
                retry -= 1
                if retry == 0:
                    return e
                time.sleep(1.2)
                continue

    @staticmethod
    def make_request_post_with_params(url, headers, data, params):
        """
        Make a request post with params
        """
        retry = 5
        while True:
            try:
                response = requests.post(url, headers=headers, json=data, params=params)
                return response
            except Exception as e:
                retry -= 1
                if retry == 0:
                    return e
                time.sleep(1.2)
                continue

def get_data_authorizer(request: Request):
    """
    Gets the authorizer data from the request.

    Parameters:
        request (Request): The HTTP request.

    Returns:
        dict: A dictionary with the authorizer data.
    """ 
    token = request.headers.get("Authorization")
    try:
        token_decode = jwt.decode(
            jwt=token, key=SECRET_KEY, algorithms=["HS256"]
        )
        return token_decode
    except Exception:
        raise HTTPException(status_code=401, detail="You are not permission")

def generate_token(data):
    """
    Genera un token de autenticación y almacena los datos relacionados en la base de datos.

    :param data: Los datos del token y la información asociada.
    :type data: dict
    :return: El token generado y el UUID asociado.
    :rtype: str, str
    """
    try:
        uuid = generateUniqueID()
        expires_at = int(time.time()) + int(120)
        data["expires_at"] = expires_at
        data["uuid"] = uuid 
        encode_data = jwt.encode(
            payload=data, key=SECRET_KEY, algorithm="HS256"
        )
        return encode_data
    except Exception as e:
        print(traceback.format_exc())
        raise Exception("Error generate_token: {}".format(str(e))) 

def generateUniqueID():
    """
    Genera un ID único basado en el tiempo y cadenas aleatorias.

    :return: Un ID único.
    :rtype: str
    """
    time_str = str(int(getCurrentTime()))
    return "{}-{}-{}-{}-{}".format(
        getRandomChar(5).lower(),
        time_str[:5],
        getRandomChar(5).lower(),
        time_str[-5:],
        getRandomChar(5).lower(),
    )

def getCurrentTime():
    """
    Obtiene el tiempo actual en segundos.

    :return: El tiempo actual en segundos.
    :rtype: int
    """
    return int(time.time())

def getRandomChar(y=10):
    """
    Genera una cadena aleatoria de caracteres ASCII.

    :param y: Longitud de la cadena aleatoria.
    :type y: int, optional
    :return: Una cadena aleatoria de caracteres.
    :rtype: str
    """
    return "".join(secrets.choice(string.ascii_letters) for x in range(y))
class Hasher:
    """
    Esta clase proporciona métodos para trabajar con contraseñas y hashes.
    """

    @staticmethod
    def verify_password(plain_password, hashed_password):
        """
        Verifica si una contraseña en texto plano coincide con su versión hasheada.

        :param plain_password: La contraseña en texto plano que se va a verificar.
        :type plain_password: str
        :param hashed_password: La versión hasheada de la contraseña almacenada.
        :type hashed_password: str
        :return: True si la contraseña coincide, False si no coincide.
        :rtype: bool
        """
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str):
        """
        Genera un hash a partir de una contraseña en texto plano.

        :param password: La contraseña en texto plano que se va a hashear.
        :type password: str
        :return: El hash resultante de la contraseña.
        :rtype: str
        """
        return pwd_context.hash(password)


def generate_fake_token(): 
    data = {
        "user_id": 1,
        "email": "test@gmail.com", 
        "expires_at": int(time.time()) + int(120),
        "uuid": "asdasdasdasd",
    }
    encode_data = jwt.encode(
        payload=data, key=SECRET_KEY, algorithm="HS256"
    )  
    return encode_data
