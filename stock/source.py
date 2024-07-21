from __init__ import *
from secret import *

URL_WAREHOUSES = 'https://suppliers-api.wildberries.ru/api/v3/warehouses'
URL_NMIDS = 'https://discounts-prices-api.wildberries.ru/api/v2/list/goods/filter'
URL_STOCKS = 'https://suppliers-api.wildberries.ru/api/v3/stocks/{}'
LONG_SLEEP = 60
SHORT_SLEEP = 20
COLUMNS = ['name', 'officeId', 'id', 'cargoType', 'deliveryType', 'sku', 'amount']