from __init__ import *
from secret import *


PERIODS = {
    'Вчера': {'Start': (date.today() - timedelta(days=1)).strftime('%Y-%m-%d') + ' 00:00:00', 'Finish': (date.today() - timedelta(days=1)).strftime('%Y-%m-%d') + ' 23:59:59'},
    'Позавчера': {'Start': (date.today() - timedelta(days=2)).strftime('%Y-%m-%d') + ' 00:00:00', 'Finish': (date.today() - timedelta(days=2)).strftime('%Y-%m-%d') + ' 23:59:59'},
    '3 дня': {'Start': (date.today() - timedelta(days=3)).strftime('%Y-%m-%d') + ' 00:00:00', 'Finish': datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
    '6-3 дня': {'Start': (date.today() - timedelta(days=6)).strftime('%Y-%m-%d') + ' 00:00:00', 'Finish': (date.today() - timedelta(days=3)).strftime('%Y-%m-%d ') + ' 23:59:59'},
    'Неделя': {'Start': (date.today() - timedelta(days=7)).strftime('%Y-%m-%d') + ' 00:00:00', 'Finish': datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
    '3 месяца': {'Start': (date.today() - timedelta(days=91)).strftime('%Y-%m-%d') + ' 00:00:00', 'Finish': datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
    '6-3 месяца': {'Start': (date.today() - timedelta(days=183)).strftime('%Y-%m-%d') + ' 00:00:00', 'Finish': (date.today() - timedelta(days=91)).strftime('%Y-%m-%d') + ' 23:59:59'},
}
URL = 'https://seller-analytics-api.wildberries.ru/api/v2/nm-report/detail'
LONG_SLEEP = 60
SHORT_SLEEP = 20
COLUMNS = ['page', 'nmID', 'vendorCode', 'brandName', 'begin', 'end', 'openCardCount', 'addToCartCount', 'ordersCount', 'ordersSumRub', 'buyoutsCount', 'buyoutsSumRub', 'cancelCount', 'cancelSumRub',
           'avgPriceRub', 'avgOrdersCountPerDay', 'addToCartPercent', 'cartToOrderPercent', 'buyoutsPercent', 'stocksMp', 'stocksWb']
SAMPLE = {
    'period': {
        'begin': None,
        'end': None
    },
    'orderBy': {
        'field': 'ordersSumRub',
        'mode': 'desc'
        },
    'page': None
}
