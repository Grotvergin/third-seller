from __init__ import *
from secret import *

URL_CAMPAIGNS = 'https://advert-api.wildberries.ru/adv/v1/promotion/count'
URL_STAT = 'https://advert-api.wildberries.ru/adv/v2/fullstats'
URL_DATE = 'https://advert-api.wildberries.ru/adv/v1/promotion/adverts'
SLEEP = 60
PORTION = 50
DATE = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
SECTOR = ('B3', 'C3')
TYPES_AND_NAMES = {
    4: 'в каталоге',
    5: 'в карточке товара',
    6: 'в поиске',
    7: 'в рекомендациях на главной странице',
    8: 'автоматическая',
    9: 'поиск + каталог'
}
COLUMNS = {'advertId': 'SPEC',
           'date': 'SPEC',
           'appType': 'SPEC',
           'companyType': 'SPEC',
           'nmId': None,
           'name': None,
           'views': None,
           'clicks': None,
           'ctr': None,
           'cpc': None,
           'sum': None,
           'atbs': None,
           'orders': None,
           'cr': None,
           'shks': None,
           'sum_price': None}
