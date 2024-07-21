from parsers.source import *


def Main() -> None:
    sheet_id = ExtractSheetId(GetSector('B6', 'B6', SERVICE, 'Сервисы', SHEET_ID)[0][0])
    row = len(GetSector('A2', 'A1000', SERVICE, 'Данные', sheet_id)) + 2
    barcodes = [item[0] for item in GetSector('A2', 'A1000', SERVICE, 'Настройки', sheet_id)]
    words = [item[0] for item in GetSector('B2', 'B1000', SERVICE, 'Настройки', sheet_id)]
    proxies = GetProxies()
    for word in words:
        Stamp(f'Processing template: {word}', 'i')
        data = []
        for page in range(1, PAGES_QUANTITY + 1):
            Stamp(f'Processing page {page}', 'i')
            raw = GetAndCheck(page, word, choice(proxies))
            raw = ProcessData(raw, word, page)
            data += FilterByBarcode(raw, barcodes)
            AccurateSleep(SHORT_SLEEP, 0.5)
        UploadData(data, 'Данные', sheet_id, SERVICE, row)
        row += len(data)


def GetProxies() -> list[dict]:
    raw = GetSector('A2', 'D6', SERVICE, 'Прокси', SHEET_ID)
    res = []
    for proxy in raw:
        res.append({'http': f'http://{proxy[0]}:{proxy[1]}@{proxy[2]}:{proxy[3]}',
                    'https': f'http://{proxy[0]}:{proxy[1]}@{proxy[2]}:{proxy[3]}'})
    return res


def GetAndCheck(page: int, word: str, proxies: dict = None) -> dict:
    raw = GetData(page, word, proxies)
    if 'data' not in raw:
        Stamp('No key <<data>> in response, processing again', 'w')
        AccurateSleep(SHORT_SLEEP, 0.5)
        raw = GetAndCheck(page, word, proxies)
    elif 'products' not in raw['data']:
        Stamp('No key <<products>> in response, processing again', 'w')
        AccurateSleep(SHORT_SLEEP, 0.5)
        raw = GetAndCheck(page, word, proxies)
    elif SmartLen(raw['data']['products']) == 1:
        Stamp('Length of products list is equal 1, processing again', 'w')
        AccurateSleep(SHORT_SLEEP, 0.5)
        raw = GetAndCheck(page, word, proxies)
    else:
        Stamp('Good data', 's')
    return raw


def FilterByBarcode(list_for_filter: list, barcodes: list) -> list:
    filtered_list = []
    for sublist in list_for_filter:
        if sublist[0] in barcodes:
            filtered_list.append(sublist)
    return filtered_list


@ControlRecursion
def GetData(page: int, word: str, proxy: dict) -> dict:
    Stamp(f'Trying to connect {URL}', 'i')
    PARAMS['page'] = page
    PARAMS['query'] = word
    HEADERS['User-Agent'] = choice(USER_AGENTS)
    HEADERS['Referer'] = HEADERS['Referer'].format(quote(word))
    try:
        response = get(URL, params=PARAMS, headers=HEADERS, proxies=proxy)
    except ConnectionError:
        Stamp(f'Connection on {URL}', 'e')
        Sleep(LONG_SLEEP)
        raw = GetData(page, word, proxy)
    else:
        if str(response.status_code)[0] == '2':
            Stamp(f'Status = {response.status_code} on {URL}', 's')
            if response.content:
                raw = response.json()
            else:
                Stamp('Response is empty', 'w')
                raw = {}
        else:
            Stamp(f'Status = {response.status_code} on {URL}', 'e')
            Sleep(LONG_SLEEP)
            raw = GetData(page, word, proxy)
    return raw


def ProcessData(raw: dict, word: str, page: int) -> (list, list):
    data = []
    for i in range(SmartLen(raw['data']['products'])):
        row = []
        for column in COLUMNS:
            match column:
                case 'id':
                    row.append(str(raw['data']['products'][i]['id']))
                case 'name':
                    row.append(str(raw['data']['products'][i]['name']))
                case 'word':
                    row.append(word)
                case 'page':
                    row.append(str(page))
                case 'place':
                    row.append(str(i + 1))
                case 'time':
                    row.append(str(datetime.now().strftime('%Y-%m-%d %H:%M')))
                case 'price':
                    row.append(str(round(int(raw['data']['products'][i]['sizes'][0]['price']['product']) / 100)))
        data.append(row)
    return data


if __name__ == '__main__':
    Main()
