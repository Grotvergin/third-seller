from prices.source import *


def Main():
    sheet_id, token = GetSector('B4', 'C4', SERVICE, 'Сервисы', SHEET_ID)[0]
    CleanSheet(len(COLUMNS), 'Данные', ExtractSheetId(sheet_id), SERVICE)
    raw = GetData(token)
    prepared = ProcessData(raw)
    UploadData(prepared, 'Данные', ExtractSheetId(sheet_id), SERVICE)


@ControlRecursion
def GetData(token: str) -> list:
    Stamp(f'Trying to connect {URL}', 'i')
    try:
        response = get(URL, headers={'Authorization': token}, params={'limit': 1000})
    except ConnectionError:
        Stamp(f'Connection on {URL}', 'e')
        Sleep(LONG_SLEEP)
        raw = GetData(token)
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
            raw = GetData(token)
    return raw


def ProcessData(raw: dict) -> list:
    list_of_rows = []
    for good in raw['data']['listGoods']:
        for size in good['sizes']:
            one_row = []
            for column in COLUMNS:
                if column == 'time':
                    one_row.append(str(datetime.now().strftime('%Y-%m-%d %H:%M')))
                elif column in ('nmID', 'vendorCode', 'discount'):
                    one_row.append(str(good[column]))
                else:
                    one_row.append(str(size[column]).replace('.', ','))
            list_of_rows.append(one_row)
    return list_of_rows


if __name__ == '__main__':
    Main()
