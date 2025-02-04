from funnel.source import *


def Main():
    sheet_id, token = GetSector('B5', 'C5', SERVICE, 'Сервисы', SHEET_ID)[0]
    for sheet_name, period in PERIODS.items():
        CleanSheet(len(COLUMNS), sheet_name, ExtractSheetId(sheet_id), SERVICE)
        raw = GetAllPages(token, period)
        prepared = ProcessData(raw)
        UploadData(prepared, sheet_name, ExtractSheetId(sheet_id), SERVICE)
        Sleep(SHORT_SLEEP)


@ControlRecursion
def GetData(token: str, period: dict, page: int) -> dict:
    Stamp(f'Trying to connect {URL}', 'i')
    body = SAMPLE.copy()
    body['period']['begin'] = period['Start']
    body['period']['end'] = period['Finish']
    body['page'] = page
    try:
        response = post(URL, headers={'Authorization': token}, json=body)
    except ConnectionError:
        Stamp(f'On connection {URL}', 'e')
        Sleep(LONG_SLEEP)
        raw = GetData(token, period, page)
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
            raw = GetData(token, period, page)
    return raw


def GetAllPages(token: str, period: dict) -> list:
    list_of_pages = []
    Stamp(f"Trying to get all pages from {period['Start']} to {period['Finish']}", 'i')
    page = 1
    portion = GetData(token, period, page)
    list_of_pages.append(portion['data'])
    while portion['data']['isNextPage']:
        page += 1
        Sleep(SHORT_SLEEP)
        portion = GetData(token, period, page)
        list_of_pages += portion['data']
    return list_of_pages


def ProcessData(raw: list) -> list:
    list_of_rows = []
    for page in raw:
        for card in page['cards']:
            one_row = []
            for column in COLUMNS:
                match column:
                    case 'page':
                        one_row.append(str(page[column]))
                    case 'nmID' | 'vendorCode' | 'brandName':
                        one_row.append(str(card[column]))
                    case 'addToCartPercent' | 'cartToOrderPercent' | 'buyoutsPercent':
                        one_row.append(str(card['statistics']['selectedPeriod']['conversions'][column]))
                    case 'stocksMp' | 'stocksWb':
                        one_row.append(str(card['stocks'][column]))
                    case _:
                        one_row.append(str(card['statistics']['selectedPeriod'][column]).replace('.', ','))
            list_of_rows.append(one_row)
    return list_of_rows


if __name__ == '__main__':
    Main()
