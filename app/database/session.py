"""
Archivo que contiene la clase Database y la función get_db.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from app.settings import DB_HOST_WRITER, DB_HOST_READ

engines = {}


class RoutingSession(Session):
    """
    Clase de sesión personalizada que permite el enrutamiento dinámico de conexiones a la base de datos.

    Esta clase hereda de la clase Session de SQLAlchemy y proporciona funcionalidad para enrutamiento dinámico
    de conexiones a motores de bases de datos. Esto se logra utilizando el atributo "_name", que puede ser None
    o un nombre de motor de base de datos específico.
    """

    # Atributo de clase que puede ser None o un nombre de motor de base de datos específico.
    _name = None

    def get_bind(self, mapper=None, clause=None):  # pylint: disable=R1710
        """
        Sobrescribe el método get_bind de la clase Session de SQLAlchemy para obtener el motor de base de datos
        adecuado en función del contexto.

        :param mapper: El objeto de asignación de SQLAlchemy.
        :type mapper: Mapper or None
        :param clause: Una cláusula de SQL.
        :type clause: ClauseElement or None
        :return: El motor de base de datos correspondiente al contexto.
        :rtype: Engine
        """
        if self._name:  # pylint: disable=R1705
            return engines[self._name]
        elif mapper:
            return engines["reader"]
        elif self._flushing:
            return engines["writer"]

    def using_bind(self, name):
        """
        Crea una nueva instancia de RoutingSession con un motor de base de datos específico.

        :param name: El nombre del motor de base de datos.
        :type name: str
        :return: Una nueva instancia de RoutingSession con el motor de base de datos especificado.
        :rtype: RoutingSession
        """
        s = RoutingSession()
        vars(s).update(vars(self))
        s._name = name  # pylint: disable=W0212
        return s


engines["writer"] = create_engine(DB_HOST_WRITER, logging_name="writer", echo=False)
engines["reader"] = create_engine(DB_HOST_READ, logging_name="reader", echo=False)
session_database = sessionmaker(
    autocommit=False, autoflush=False, class_=RoutingSession
)


def get_db():
    """
    Obtiene una sesión de base de datos para realizar operaciones.

    :return: Una sesión de base de datos.
    :rtype: Session
    """
    db = session_database.Session()
    try:
        yield db
    finally:
        db.close()