from __init__ import *
from secret import *

URL_WAREHOUSES = 'https://suppliers-api.wildberries.ru/api/v3/warehouses'
URL_BARCODES = 'https://statistics-api.wildberries.ru/api/v1/supplier/stocks'
URL_STOCKS = 'https://suppliers-api.wildberries.ru/api/v3/stocks/{}'
LONG_SLEEP = 60
SHORT_SLEEP = 20
COLUMNS = ['name', 'officeId', 'id', 'cargoType', 'deliveryType', 'sku', 'amount']