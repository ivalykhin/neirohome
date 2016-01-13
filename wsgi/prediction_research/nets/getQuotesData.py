from suds.client import Client
from suds.xsd.doctor import Import, ImportDoctor
import urllib2
import lxml.html


def getUSDQuotesOnDate(d):
    url = 'http://www.cbr.ru/DailyInfoWebServ/DailyInfo.asmx?wsdl'
    imp = Import('http://www.w3.org/2001/XMLSchema', location='http://www.w3.org/2001/XMLSchema.xsd')
    imp.filter.add('http://web.cbr.ru/')
    client = Client(url, doctor=ImportDoctor(imp))
    curs = 0.0
    response = client.service.GetCursOnDate(On_date=d)
    print 'Received response on ' + str(d)
    for item in response['diffgram']['ValuteData']['ValuteCursOnDate']:
        if item['_id'] == 'ValuteCursOnDate10':
            curs = item['Vcurs']
            break
    return curs


def getCurrentOilQuotes():
    html = lxml.html.fromstring(urllib2.urlopen(urllib2.Request('http://www.yandex.ru/')).read())
    xpath_expr = '//div[@class="inline-stocks inline-stocks_new_yes i-bem"]/div[3]/div/span/span[2]'
    element = html.xpath(xpath_expr)
    return element[0].text



