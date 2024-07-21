from __init__ import *
from secret import *

URL_BOX = 'https://common-api.wildberries.ru/api/v1/tariffs/box'
URL_MONO = f'https://common-api.wildberries.ru/api/v1/tariffs/pallet'
SHORT_SLEEP = 10
LONG_SLEEP = 60
COLUMNS_MONO = ['palletDeliveryExpr', 'palletDeliveryValueBase', 'palletDeliveryValueLiter',
                'palletStorageExpr', 'palletStorageValueExpr', 'warehouseName', 'timestamp']
COLUMNS_BOX = ['boxDeliveryAndStorageExpr', 'boxDeliveryBase', 'boxDeliveryLiter',
               'boxStorageBase', 'boxStorageLiter', 'warehouseName', 'timestamp']
DAYS_DELTA = 3
