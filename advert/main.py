from advert.source import *


def Main() -> None:
    sheet_id, token = GetSector(SECTOR[0], SECTOR[1], SERVICE, SHEET_SERVICE, SHEET_ID)[0]
    ParallelThreads('Данные', ExtractSheetId(sheet_id), token)


def ParallelThreads(heading: str, sheet_id: str, token: str):
    Stamp(f'Opened thread for {heading}', 'b')
    campaigns = PrepareCampaigns(token)
    ProcessData(campaigns, heading, token, sheet_id, SERVICE)
    Stamp(f'Closed thread for {heading}', 'b')


def PrepareCampaigns(token: str) -> dict:
    raw = GetData(URL_CAMPAIGNS, token)
    dict_of_campaigns = {}
    for i in range(SmartLen(raw['adverts'])):
        for j in range(SmartLen(raw['adverts'][i]['advert_list'])):
            dict_of_campaigns[raw['adverts'][i]['advert_list'][j]['advertId']] = raw['adverts'][i]['type']
    dates = []
    for i in range(0, SmartLen(list(dict_of_campaigns.keys())), PORTION):
        Stamp(f'PREPARING {PORTION} campaigns from {i} out of {SmartLen(list(dict_of_campaigns.keys()))}', 'i')
        portion_of_campaigns = list(list(dict_of_campaigns.keys()))[i:i + PORTION]
        dates += GetData(URL_DATE, token, portion_of_campaigns)
        Stamp(f'Now data length is {SmartLen(dates)}', 'i')
        Sleep(SLEEP)
    res_dict_for_dates = {}
    for key, value in dict_of_campaigns.items():
        for item in dates:
            start_time = datetime.strptime(item['startTime'].rsplit('+', 1)[0], "%Y-%m-%dT%H:%M:%S.%f")
            try:
                end_time = datetime.strptime(item['endTime'].rsplit('+', 1)[0], "%Y-%m-%dT%H:%M:%S.%f")
            except ValueError:
                end_time = datetime.strptime(item['endTime'].rsplit('+', 1)[0], "%Y-%m-%dT%H:%M:%S")
            req_time = datetime.strptime(DATE, '%Y-%m-%d')
            if key == item['advertId'] and start_time < req_time < end_time:
                res_dict_for_dates[key] = value
    return res_dict_for_dates


@ControlRecursion
def GetData(url: str, token:str, body: list = None) -> dict:
    Stamp(f'Trying to connect {url}', 'i')
    try:
        if body is None:
            response = get(url, headers={'Authorization': token})
        else:
            response = post(url, headers={'Authorization': token}, data=dumps(body))
    except ConnectionError:
        Stamp(f'Connection on {url}', 'e')
        Sleep(SLEEP)
        raw = GetData(url, token, body)
    else:
        if str(response.status_code)[0] == '2':
            Stamp(f'Status = {response.status_code} on URL: {url}', 's')
            if response.content:
                raw = response.json()
            else:
                Stamp('Response is empty', 'w')
                raw = {}
        else:
            Stamp(f'Status = {response.status_code} on {url}', 'e')
            Sleep(SLEEP)
            raw = GetData(url, token, body)
    return raw


def ProcessData(raw: dict, sheet_name: str, token: str, sheet_id: str, service: Resource) -> None:
    row = len(GetSector('A2', 'A40000', service, sheet_name, sheet_id)) + 2
    Stamp(f'For sheet {sheet_name} found {SmartLen(raw)} companies', 'i')
    for i in range(0, SmartLen(raw), PORTION):
        Stamp(f'Processing {PORTION} campaigns from {i} out of {SmartLen(raw)}', 'i')
        portion_of_campaigns = list(raw.keys())[i:i + PORTION]
        list_for_request = [{'id': campaign, 'interval': {'begin': DATE, 'end': DATE}} for campaign in portion_of_campaigns]
        data = GetData(URL_STAT, token, list_for_request)
        list_of_all = []
        for t in range(SmartLen(data)):
            for j in range(SmartLen(data[t]['days'])):
                for k in range(SmartLen(data[t]['days'][j]['apps'])):
                    for nm in range(SmartLen(data[t]['days'][j]['apps'][k]['nm'])):
                        one_row = []
                        for key, value in COLUMNS.items():
                            try:
                                if value is None:
                                    one_row.append(str(data[t]['days'][j]['apps'][k]['nm'][nm][key]).replace('.', ','))
                                elif key == 'advertId':
                                    one_row.append(str(data[t]['advertId']))
                                elif key == 'date':
                                    one_row.append(str(data[t]['days'][j]['date'])[:10])
                                elif key == 'appType':
                                    one_row.append(str(data[t]['days'][j]['apps'][k][key]))
                                elif key == 'companyType':
                                    one_row.append(str(TYPES_AND_NAMES[int(raw[data[t]['advertId']])]))
                                else:
                                    one_row.append(value.replace('.', ','))
                            except KeyError:
                                one_row.append(MSG)
                        list_of_all.append(one_row)
        UploadData(list_of_all, sheet_name, sheet_id, service, row)
        row += len(list_of_all)
        Sleep(SLEEP)


if __name__ == '__main__':
    Main()
