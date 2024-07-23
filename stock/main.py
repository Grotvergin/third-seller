from stock.source import *


def Main():
    sheet_id, token = GetSector('B7', 'C7', SERVICE, 'Сервисы', SHEET_ID)[0]
    warehouses = GetData(URL_WAREHOUSES, token)
    barcodes = GetData(URL_BARCODES, token, {'dateFrom': '2019-06-20'})
    data = ProcessData(warehouses, barcodes, token)
    CleanSheet(len(COLUMNS), 'Данные', ExtractSheetId(sheet_id), SERVICE)
    UploadData(data, 'Данные', ExtractSheetId(sheet_id), SERVICE)


def ProcessData(warehouses: list, barcodes: dict, token: str) -> list:
    barcodes = [str(item['barcode']) for item in barcodes]
    list_of_rows = []
    for warehouse in warehouses:
        data = GetData(URL_STOCKS.format(warehouse['id']), token, body={'skus': barcodes})
        for stock in data['stocks']:
            one_row = []
            for column in COLUMNS:
                if column in ('sku', 'amount'):
                    one_row.append(stock[column])
                else:
                    one_row.append(warehouse[column])
            list_of_rows.append(one_row)
    return list_of_rows


@ControlRecursion
def GetData(url: str, token: str, params: dict = None, body: dict = None) -> dict:
    Stamp(f'Trying to connect {url}', 'i')
    try:
        if body:
            response = post(url, headers={'Authorization': token}, params=params, json=body)
        else:
            response = get(url, headers={'Authorization': token}, params=params)
    except ConnectionError:
        Stamp(f'On connection {url}', 'e')
        Sleep(LONG_SLEEP)
        raw = GetData(url, token, body)
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
            raw = GetData(url, token, body)
    return raw


if __name__ == '__main__':
    Main()
