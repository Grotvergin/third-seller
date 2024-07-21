from random import randint, seed, uniform, choice
from socket import gaierror
from ssl import SSLEOFError
from time import sleep, time
from datetime import datetime, timedelta, date
from functools import wraps
from threading import Thread, Lock
from httplib2.error import ServerNotFoundError
from requests import get, post, ConnectionError
from colorama import Fore, Style, init
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build, Resource
from googleapiclient.errors import HttpError
from typing import Callable, Any
from re import search
from json import dumps
from urllib.parse import quote

init()
seed()
CREDS = Credentials.from_service_account_file('keys.json', scopes=['https://www.googleapis.com/auth/spreadsheets'])
MAX_ROW = 100000
MAX_RECURSION = 15
SLEEP_GOOGLE = 20
SIZE_CHUNK = 5000
START = time()
TODAY = datetime.now().strftime('%Y-%m-%d')
MSG = 'NoData'
SHEET_SERVICE = 'Сервисы'
CONN_ERRORS = (TimeoutError, ServerNotFoundError, gaierror, HttpError, SSLEOFError)


def ExtractSheetId(raw_link: str) -> str:
    pattern = r"/d/([^/]+)/"
    match = search(pattern, raw_link)
    result = match.group(1) if match else None
    return result


def AccurateSleep(timer: float, ratio: float = 0.0) -> None:
    rand_time = round(uniform((1 - ratio) * timer, (1 + ratio) * timer), 2)
    Stamp(f'Sleeping {rand_time} seconds', 'l')
    sleep(rand_time)


def GetSector(start: str, finish: str, service: Resource, sheet_name: str, sheet_id: str) -> list:
    Stamp(f'Trying to get sector from {start} to {finish} from sheet {sheet_name}', 'i')
    try:
        res = service.spreadsheets().values().get(spreadsheetId=sheet_id,
                                                  range=f'{sheet_name}!{start}:{finish}').execute().get('values', [])
    except CONN_ERRORS as err:
        Stamp(f'Status = {err} on getting sector from {start} to {finish} from sheet {sheet_name}', 'e')
        Sleep(SLEEP_GOOGLE)
        res = GetSector(start, finish, service, sheet_name, sheet_id)
    else:
        if not res:
            Stamp(f'No elements in sector from {start} to {finish} sheet {sheet_name} found', 'w')
        else:
            Stamp(f'Found {len(res)} rows from sector from {start} to {finish} sheet {sheet_name}', 's')
    return res


def CleanSheet(width: int, sheet_name: str, sheet_id: str, service: Resource, column: str = 'A'):
    Stamp(f'Trying to clean sheet {sheet_name}', 'i')
    height = len(GetSector(f'{column}1', f'{column}{MAX_ROW}', service, sheet_name, sheet_id))
    empty = PrepareEmpty(width, height)
    UploadData(empty, sheet_name, sheet_id, service)


def ControlRecursion(func: Callable[..., Any], maximum: int = MAX_RECURSION) -> Callable[..., Any]:
    func.recursion_depth = 0

    @wraps(func)
    def Wrapper(*args, **kwargs):
        if func.recursion_depth > maximum:
            Stamp('Max level of recursion reached', 'e')
            raise RecursionError
        if func.recursion_depth > 0:
            Stamp(f"Recursion = {func.recursion_depth}, allowed = {maximum}", 'w')
        func.recursion_depth += 1
        result = func(*args, **kwargs)
        func.recursion_depth -= 1
        return result

    return Wrapper


def SmartLen(data: list | dict) -> int:
    try:
        length = len(data)
    except (TypeError, KeyError):
        length = 0
    return length


def PrepareEmpty(width: int, blank: int) -> list:
    list_of_empty = []
    one_row = [''] * width
    for k in range(blank):
        list_of_empty.append(one_row)
    return list_of_empty


def LargeUpload(list_of_rows: list, sheet_name: str, sheet_id: str, service: Resource, row: int = 2) -> None:
    chunks = [list_of_rows[i:i + SIZE_CHUNK] for i in range(0, len(list_of_rows), SIZE_CHUNK)]
    for i, chunk in enumerate(chunks):
        UploadData(chunk, sheet_name, sheet_id, service, row + i * SIZE_CHUNK)


@ControlRecursion
def UploadData(list_of_rows: list, sheet_name: str, sheet_id: str, service: Resource, row: int = 2) -> None:
    Stamp(f'Trying to upload data to sheet {sheet_name}', 'i')
    try:
        width = SmartLen(list_of_rows[0])
    except IndexError:
        width = 0
    try:
        res = service.spreadsheets().values().update(spreadsheetId=sheet_id,
                                                     range=f'{sheet_name}!A{row}:{COLUMN_INDEXES[width]}{row + len(list_of_rows)}',
                                                     valueInputOption='USER_ENTERED',
                                                     body={'values': list_of_rows}).execute()
    except CONN_ERRORS as err:
        Stamp(f'Status = {err} on uploading data to sheet {sheet_name}', 'e')
        Sleep(SLEEP_GOOGLE)
        UploadData(list_of_rows, sheet_name, sheet_id, service, row)
    else:
        Stamp(f"On uploading: {res.get('updatedRows')} rows in range {res.get('updatedRange')}", 's')


@ControlRecursion
def BuildService() -> Resource:
    Stamp(f'Trying to build service', 'i')
    try:
        service = build('sheets', 'v4', credentials=CREDS)
    except CONN_ERRORS as err:
        Stamp(f'Status = {err} on building service', 'e')
        Sleep(SLEEP_GOOGLE)
        BuildService()
    else:
        Stamp('Built service successfully', 's')
        return service


def Sleep(timer: int, ratio: float = 0.0) -> None:
    rand_time = randint(int((1 - ratio) * timer), int((1 + ratio) * timer))
    Stamp(f'Sleeping {rand_time} seconds', 'l')
    sleep(rand_time)


def Stamp(message: str, level: str) -> None:
    time_stamp = datetime.now().strftime('[%m-%d|%H:%M:%S]')
    match level:
        case 'i':
            print(Fore.LIGHTBLUE_EX + time_stamp + '[INF] ' + message + '.' + Style.RESET_ALL)
        case 'w':
            print(Fore.LIGHTMAGENTA_EX + time_stamp + '[WAR] ' + message + '!' + Style.RESET_ALL)
        case 's':
            print(Fore.LIGHTGREEN_EX + time_stamp + '[SUC] ' + message + '.' + Style.RESET_ALL)
        case 'e':
            print(Fore.RED + time_stamp + '[ERR] ' + message + '!!!' + Style.RESET_ALL)
        case 'l':
            print(Fore.WHITE + time_stamp + '[SLE] ' + message + '...' + Style.RESET_ALL)
        case 'b':
            print(Fore.LIGHTYELLOW_EX + time_stamp + '[BOR] ' + message + '.' + Style.RESET_ALL)
        case _:
            print(Fore.WHITE + time_stamp + '[UNK] ' + message + '?' + Style.RESET_ALL)


def MakeColumnIndexes() -> dict:
    indexes = {}
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for i, letter in enumerate(alphabet):
        indexes[i] = letter
    for i in range(len(alphabet)):
        for j in range(len(alphabet)):
            indexes[len(alphabet) + i * len(alphabet) + j] = alphabet[i] + alphabet[j]
    return indexes


COLUMN_INDEXES = MakeColumnIndexes()
SERVICE = BuildService()
