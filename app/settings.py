"""settings file"""

from os import getenv as env
from dotenv import load_dotenv

load_dotenv()

DB_NAME = str(env("DB_NAME", default=""))
DB_USER = str(env("DB_USER", default=""))
DB_PASSWORD = str(env("DB_PASSWORD", default=""))
DB_PORT = str(env("DB_PORT", default=""))
DB_HOST_WRITER = str(env("DB_HOST_WRITER", default=""))
DB_HOST_READ = str(env("DB_HOST_READ", default=""))

DB_URL_WRITER = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST_WRITER}:{DB_PORT}/{DB_NAME}"
)
DB_URL_READ = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST_READ}:{DB_PORT}/{DB_NAME}"
URL_API_FUNCTION_JUDICIAL_CONTAR_CAUSAS = str(
    env("URL_API_FUNCTION_JUDICIAL_CONTAR_CAUSAS", default="")
)
URL_API_OBTENER_CAUSAS = str(env("URL_API_OBTENER_CAUSAS", default=""))
URL_INFORMACION_INFO = str(env("URL_INFORMACION_INFO", default=""))
URL_INFORMACION_INCIDENTE_JUDICATURA = str(
    env("URL_INFORMACION_INCIDENTE_JUDICATURA", default="")
)
URL_ACTUACIONES_JUDICIALES = str(env("URL_ACTUACIONES_JUDICIALES", default=""))
SECRET_KEY = str(env("SECRET_KEY", default=""))