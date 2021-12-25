import datetime

import aiohttp
from celery import Celery

from CurrencyApp.celery import app

from Currency.models import Currency

"""
api doc https://bank.gov.ua/ua/open-data/api-dev
today currency   https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json
by date currency https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json&date=19960106


"""
URL_REQUEST = 'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json'





async def fetch(client, date_str):
    async with client.get(f'{URL_REQUEST}&date={date_str}') as resp:
        assert resp.status == 200
        return await resp.json()


async def parse():
    async with aiohttp.ClientSession() as client:
        first_date = datetime.date(1996, 1, 6)
        output_l = []
        duration = datetime.datetime.now().date() - first_date
        for d in range(duration.days - 100, duration.days):
            day = first_date + datetime.timedelta(days=d)

            data = await fetch(client, day.strftime('%Y%m%d'))
            data_objs = [Currency(r030=d['r030'], txt=d['txt'], rate=d['rate'], cc=d['cc'], exchangedate=day) for d
                         in data]
            output_l += data_objs
        return output_l

@app.task
def update_currency():
    first_date = datetime.date(1996, 1, 6)
    dates_update = []
    duration = datetime.datetime.now().date() - first_date
    currency_objs = Currency.objects.all().values_list('exchangedate').distinct()
    print('currency_objs', currency_objs)
    # currency_objs = await Currency.objects.filter(exchangedate=day)
    # if currency_objs:
    #     continue
    #
    # loop = asyncio.get_event_loop()
    # data_objs = loop.run_until_complete(parse())
    # Currency.objects.bulk_create(data_objs, ignore_conflicts=True)