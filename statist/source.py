from __init__ import *
from secret import *

SECTOR = ('B2', 'C2')
PERC_COMM = 0.022249
SLEEP = 70
DATE_FROM = (datetime.now() - timedelta(days=120)).strftime('%Y-%m-%d')

SHEETS = {
    'Заказы': {
        'URL': 'https://statistics-api.wildberries.ru/api/v1/supplier/orders',
        'Columns': {
            'srid': 'SPEC',
            'date': None,
            'lastChangeDate': None,
            'supplierArticle': None,
            'techSize': None,
            'barcode': None,
            'quantity': '1',
            'totalPrice': None,
            'discountPercent': None,
            'warehouseName': None,
            'regionName': None,
            'incomeID': None,
            'odid': '',
            'nmId': None,
            'subject': None,
            'category': None,
            'brand': None,
            'isCancel': None,
            'cancelDate': None,
            'gNumber': None
        }
    },
    'Продажи': {
        'URL': 'https://statistics-api.wildberries.ru/api/v1/supplier/sales',
        'Columns': {
            'number': '',
            'supplierArticle': None,
            'techSize': None,
            'quantity': '1',
            'totalPrice': None,
            'discountPercent': None,
            'isSupply': None,
            'isRealization': None,
            'barcode': None,
            'orderId': '',
            'promoCodeDiscount': '',
            'warehouseName': None,
            'countryName': None,
            'oblastOkrugName': None,
            'regionName': None,
            'incomeID': None,
            'saleID': None,
            'odid': '',
            'spp': None,
            'forPay': None,
            'finishedPrice': None,
            'priceWithDisc': None,
            'nmId': None,
            'subject': None,
            'category': None,
            'brand': None,
            'IsStorno': '',
            'gNumber': None,
            'date': None,
            'lastChangeDate': None
        }
    },
    'Склад': {
        'URL': 'https://statistics-api.wildberries.ru/api/v1/supplier/stocks',
        'Columns': {
            'lastChangeDate': None,
            'supplierArticle': None,
            'techSize': None,
            'barcode': None,
            'quantity': None,
            'isSupply': None,
            'isRealization': None,
            'quantityFull': None,
            'quantityNotInOrders': '',
            'warehouseName': None,
            'inWayToClient': None,
            'inWayFromClient': None,
            'nmId': None,
            'subject': None,
            'category': None,
            'daysOnSite': '',
            'brand': None,
            'SCCode': None,
            'Price': None,
            'Discount': None,
            'WarehouseID': ''
        }
    }
}
