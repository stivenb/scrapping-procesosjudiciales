from app.database.models import models
from app.utils import MakeRequestSync 
from app.settings import (
    URL_API_FUNCTION_JUDICIAL_CONTAR_CAUSAS,
    URL_API_OBTENER_CAUSAS,
    URL_INFORMACION_INFO,
    URL_INFORMACION_INCIDENTE_JUDICATURA,
    URL_ACTUACIONES_JUDICIALES
)
from fastapi import HTTPException
import math
import asyncio
import aiohttp 

import ssl

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

async def get_apis(data_req: dict, key, session):
    timeout = aiohttp.ClientTimeout(total=600)
    counter = 0
    max_retries = 15
    status_errors = []
    while counter < max_retries:
        time_sleep = 1.5
        url = data_req[key]["url"].format(id=data_req[key]["payload"])
        async with session.get(
            url,
            headers=data_req[key]["headers"],
            timeout=timeout,
            verify_ssl=False,            
        ) as response:
            if response.status == 200:  # pylint: disable=R1705
                try:
                    data_res = await response.json()
                    data_req_actuaciones = generate_payload_actuaciones_judiciales(data_res, data_req["idJuicio"])
                    data_all_scrapper = await consume_api_post(data_req_actuaciones, "data_info_actuacion")
                    data_req[key] = data_all_scrapper
                    return data_req
                except Exception as error:
                    print("response error", error)
            elif response.status >= 400:
                print("falle", response.status)
                time_sleep += 1.5
                await asyncio.sleep(time_sleep)
            counter += 1
            status_errors.append(response.status)
            await asyncio.sleep(2)
    return {
        "error": "ERROR",
        "response": "max retries",
        "url": data_req["url"],
        "status_errors": status_errors,
        "data": {
            "metadata": data_req["params"],
        },
    }


async def post_api(data_req: dict, key, session):
    timeout = aiohttp.ClientTimeout(total=600)
    counter = 0
    max_retries = 15
    status_errors = []
    while counter < max_retries:
        time_sleep = 1.5
        async with session.post(
            data_req[key]["url"],
            headers=data_req[key]["headers"],
            json=data_req[key]["payload"],
            timeout=timeout,
            verify_ssl=False,
        ) as response:
            if response.status == 200:  # pylint: disable=R1705
                try:
                    data_res = await response.json()
                    data_req[key]["actuaciones"] = data_res                    
                    return data_req
                except Exception as error:
                    print("response error", error)
            elif response.status >= 400:
                print("falle", response.status)
                time_sleep += 1.5
                await asyncio.sleep(time_sleep)
            counter += 1
            status_errors.append(response.status)
            await asyncio.sleep(2)
    return {
        "error": "ERROR",
        "response": "max retries",
        "url": data_req["url"],
        "status_errors": status_errors,
        "data": {
            "metadata": data_req["params"],
        },
    }

async def consume_api_get(data_payload: dict, key: str) -> list:
    """
    Consume la api del judicial
    """
    tasks = []
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context)) as session:
        for record in data_payload:
            task = asyncio.ensure_future(get_apis(record, key, session))
            tasks.append(task)
        process_requests = await asyncio.gather(*tasks, return_exceptions=False)
        return process_requests

async def consume_api_post(data_payload: dict, key: str) -> list:
    """
    Consume la api actuaciones judiciales
    """
    tasks = []
    async with aiohttp.ClientSession() as session:
        for record in data_payload:
            task = asyncio.ensure_future(post_api(record, key, session))
            tasks.append(task)
        process_requests = await asyncio.gather(*tasks, return_exceptions=False)
        return process_requests

def get_all_causas(data):
    """
    Get all causas from the api
    """
    causas = MakeRequestSync.make_request_post(
        URL_API_FUNCTION_JUDICIAL_CONTAR_CAUSAS,
        {"Content-Type": "application/json", "User-Agent": "Mozilla / firefox"},
        data,
    )
    if causas.status_code == 200:
        return causas.json()
    raise HTTPException(status_code=400, detail="Error causas failed to get data")


def get_all_pages(causas):
    """
    Get all pages from the api search
    """
    element_by_page = 50

    total_paginas = math.ceil(causas / element_by_page)
    paginas = []
    for pagina in range(1, total_paginas + 1):
        paginas.append({"page": pagina, "size": element_by_page})
    return paginas


def get_all_causas_search(data, pages):
    """
    Get all causas from the api
    """
    list_causas = []
    for param in pages:
        search_causas = MakeRequestSync.make_request_post_with_params(
            URL_API_OBTENER_CAUSAS,
            {"Content-Type": "application/json", "User-Agent": "Mozilla / firefox"},
            data,
            param,
        )
        if search_causas.status_code == 200:
            list_causas.extend(search_causas.json())

    return list_causas


def generate_payload_details(data):
    """
    Generate Payload details
    """
    list_elements = []
    for record in data:
        dictionary = {
            **record,
            "data_info_juicio": {
                "url": URL_INFORMACION_INCIDENTE_JUDICATURA,
                "headers": {
                    "Content-Type": "application/json",
                    "User-Agent": "Mozilla / firefox",
                },
                "payload": record["idJuicio"],
            },
        }
        list_elements.append(dictionary)
    return list_elements

def generate_payload_actuaciones_judiciales(data: list, id_juicio: str):
    """
    Generate payload actuaciones judiciales
    """
    list_elements = []
    for record in data:
        dictionary = {
            **record,
            "data_info_actuacion": {
                "url": URL_ACTUACIONES_JUDICIALES,
                "headers": {
                    "Content-Type": "application/json",
                    "User-Agent": "Mozilla / firefox",
                },
                "payload": {
                    "aplicativo": "web",
                    "idIncidenteJudicatura":record["lstIncidenteJudicatura"][0]["idIncidenteJudicatura"],
                    "idJudicatura": record["idJudicatura"],
                    "idJuicio": id_juicio,
                    "idMovimientoJuicioIncidente":record["lstIncidenteJudicatura"][0]["idMovimientoJuicioIncidente"],
                    "incidente":record["lstIncidenteJudicatura"][0]["incidente"],
                    "nombreJudicatura": record["nombreJudicatura"]
                },
            },
        }
        list_elements.append(dictionary)
    return list_elements

def insert_juicio(data, session):
    """
    Inserta un juicio en la base de datos, junto con sus incidentes y litigantes asociados.
    """
    # Crear el juicio
    juicio = models.Causa(
        idJuicio=data["idJuicio"],
        estadoActual=data.get("estadoActual"),
        idMateria=data.get("idMateria"),
        nombreDelito=data.get("nombreDelito"),
        fechaIngreso=data.get("fechaIngreso"),
    )
    
    # Añadir incidentes
    for incidente_data in data["data_info_juicio"]:
        incidente = models.Incidente(
            idIncidenteJudicatura=incidente_data["lstIncidenteJudicatura"][0]["idIncidenteJudicatura"],
            idMovimientoJuicioIncidente=incidente_data["lstIncidenteJudicatura"][0]["idMovimientoJuicioIncidente"],
            fechaCrea=incidente_data["lstIncidenteJudicatura"][0]["fechaCrea"],
            incidente=incidente_data["lstIncidenteJudicatura"][0]["incidente"],
        )
        
        # Añadir litigantes al incidente
        for litigante_data in incidente_data["lstIncidenteJudicatura"][0]["lstLitiganteActor"]:
            litigante = models.Litigante(
                tipoLitigante=litigante_data["tipoLitigante"],
                nombresLitigante=litigante_data["nombresLitigante"],
                representadoPor=litigante_data["representadoPor"],
            )
            incidente.litigantes.append(litigante)
        
        for litigante_data in incidente_data["lstIncidenteJudicatura"][0]["lstLitiganteDemandado"]:
            litigante = models.Litigante(
                tipoLitigante=litigante_data["tipoLitigante"],
                nombresLitigante=litigante_data["nombresLitigante"],
                representadoPor=litigante_data["representadoPor"],
            )
            incidente.litigantes.append(litigante)

        # Añadir actuaciones al incidente
        if "data_info_actuacion" in incidente_data:
            for actuacion_data in incidente_data["data_info_actuacion"]["actuaciones"]:
                actuacion = models.Actuacion(
                    codigo=actuacion_data["codigo"],
                    idJudicatura=actuacion_data["idJudicatura"],
                    fecha=actuacion_data["fecha"],
                    tipo=actuacion_data["tipo"],
                    actividad=actuacion_data["actividad"],
                    visible=actuacion_data["visible"],
                    uuid=actuacion_data["uuid"],
                    nombreArchivo=actuacion_data["nombreArchivo"],
                )
                incidente.actuaciones.append(actuacion)
        
        # Asociar el incidente con el juicio
        juicio.incidentes.append(incidente)
    
    # Añadir el juicio a la sesión y hacer commit
    session.add(juicio)
    session.commit()
