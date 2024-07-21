from parsers.source import *

# Прокси


def Main() -> None:
    sheet_id = ExtractSheetId(GetSector('B6', 'B6', SERVICE, 'Сервисы', SHEET_ID)[0][0])
    row = 2
    barcodes = GetSector('A2', 'A1000', SERVICE, 'Настройки', sheet_id)
    words = GetSector('B2', 'B1000', SERVICE, 'Настройки', sheet_id)
    for word in words:
        Stamp(f'Processing template: {word}', 'i')
        data = []
        for page in range(1, PAGES_QUANTITY + 1):
            Stamp(f'Processing page {page}', 'i')
            raw = GetAndCheck(page, word, proxies)
            advertise, real = ProcessData(raw, word, page)
            data += FilterByBarcode(real, barcodes)
            AccurateSleep(SHORT_SLEEP, 0.5)
        UploadData(advertise_pages, heading, sheet_id, service, row)
        row += len(data)


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


def ParseCurrentHeading(config: ConfigParser, heading: str) -> (str, str, dict):
    column = config[heading]['Column']
    sheet_id = config['DEFAULT']['SheetID' + TYPE]
    proxies = {
        'http': f'http://{config['DEFAULT']['Login']}:{config['DEFAULT']['Password']}@{config['DEFAULT']['IP/Port']}',
        'https': f'http://{config['DEFAULT']['Login']}:{config['DEFAULT']['Password']}@{config['DEFAULT']['IP/Port']}'
    }
    return column, sheet_id, proxies


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
        Stamp('Using proxy', 'i')
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
                    row.append(str(int(raw['data']['products'][i]['sizes'][0]['price']['product']) / 100))
        data.append(row)
    return data


if __name__ == '__main__':
    Main()
