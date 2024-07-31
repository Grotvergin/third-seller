from tariff.source import *


def Main():
    sheet_id, token = GetSector('B8', 'C8', SERVICE, 'Сервисы', SHEET_ID)[0]
    row_box = len(GetSector('A2', 'A1000', SERVICE, 'Коробы', ExtractSheetId(sheet_id))) + 2
    row_mono = len(GetSector('A2', 'A1000', SERVICE, 'Монопаллеты', ExtractSheetId(sheet_id))) + 2
    data_box = ProcessData(token, URL_BOX, COLUMNS_BOX)
    data_mono = ProcessData(token, URL_MONO, COLUMNS_MONO)
    UploadData(data_box, 'Коробы', ExtractSheetId(sheet_id), SERVICE, row_box)
    UploadData(data_mono, 'Монопаллеты', ExtractSheetId(sheet_id), SERVICE, row_mono)


def ProcessData(token: str, url: str, columns: list) -> list:
    list_of_rows = []
    for day_delta in range(DAYS_DELTA, 0, -1):
        cur_date = datetime.now() - timedelta(days=day_delta)
        raw = GetData(url, token, cur_date.strftime('%Y-%m-%d'))
        for warehouse in raw['response']['data']['warehouseList']:
            one_row = []
            for column in columns:
                if column == 'timestamp':
                    one_row.append(cur_date.strftime('%Y-%m-%d'))
                else:
                    one_row.append(str(warehouse[column]).replace('.', ','))
            list_of_rows.append(one_row)
        Sleep(SHORT_SLEEP)
    return list_of_rows


@ControlRecursion
def GetData(url: str, token: str, date: str) -> list:
    Stamp(f'Trying to connect {url}', 'i')
    try:
        response = get(url, headers={'Authorization': token}, params={'date': date})
    except ConnectionError:
        Stamp(f'Connection on {url}', 'e')
        Sleep(LONG_SLEEP)
        raw = GetData(url, token, date)
    else:
        if str(response.status_code)[0] == '2':
            Stamp(f'Status = {response.status_code} on {url}', 's')
            if response.content:
                raw = response.json()
            else:
                Stamp('Response is empty', 'w')
                raw = {}
        else:
            Stamp(f'Status = {response.status_code} on {url}', 'e')
            Sleep(LONG_SLEEP)
            raw = GetData(url, token, date)
    return raw


if __name__ == '__main__':
    Main()