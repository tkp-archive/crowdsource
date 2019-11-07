'''Issue: ANTM3667634

    Description: WELLPOINT INC
    Coupon Rate: 5.850
    Maturity Date: 01/15/2036
    Date, Time, Settlement, Status, Quantity, Price, Yield, Remuneration, ATS, Modifier, 2nd Modifier, Special, As-Of, Side, Reporting Party Type, Contra Party Type
    11/2/2017, 12:05:31, 11/6/2017, T, 1243000, 122.045, 4.116, M, _, _, -, -, S, D, C
    11/1/2017, 16:49:05, 11/3/2017, T, 5MM+, 121.791, 4.134, M, _, _, -, -, S, D, C
'''
import tornado.ioloop
import tornado.web
import ujson
import logging
from random import random, sample, randint, normalvariate
from datetime import datetime, timedelta, date
from faker import Faker
from copy import deepcopy

F = Faker()
P = {}


def randomDate():
    exp = sample([3, 5, 10, 30], 1)[0]
    dat = date.today() - timedelta(days=randint(1, 24)*30)
    return dat + timedelta(weeks=exp*52)


def generateInitial():
    for _ in range(10):
        company = F.company()
        P[company] = [{}]
        P[company][0]['Price'] = round(random()*10 + 100, 2)
        P[company][0]['Name'] = company
        P[company][0]['Coupon'] = round(random()*10, 3)
        P[company][0]['Maturity'] = randomDate().strftime('%Y-%m-%d')
        generate(company, True)
    company = 'ABC Corp'
    P[company] = [{}]
    P[company][0]['Price'] = round(random()*10 + 100, 2)
    P[company][0]['Name'] = company
    P[company][0]['Coupon'] = round(random()*10, 3)
    P[company][0]['Maturity'] = randomDate().strftime('%Y-%m-%d')
    generate(company, True)


def generate(company, first=False):
    global P

    if not first:
        time = datetime.strptime(P[company][-1]['Date'] + '::' + P[company][-1]['Time'], '%Y-%m-%d::%H:%M:%S')
        if datetime.now() < time + timedelta(minutes=random()*10) and company != 'ABC Corp':
            return

    if first:
        ret = P[company][-1]
    else:
        ret = deepcopy(P[company][-1])
    ret['Date'] = date.today().strftime('%Y-%m-%d')
    ret['Time'] = datetime.now().strftime('%H:%M:%S')
    ret['Settlement'] = (date.today() + timedelta(days=3)).strftime('%Y-%m-%d')
    ret['Status'] = 'T'
    ret['Quantity'] = randint(1, 50) * 10000

    price = P[company][-1]['Price'] + normalvariate(0.0, 10)
    ret['Price'] = round(price, 2)

    ret['Yield'] = round(random()*10, 3)
    ret['Remuneration'] = sample(['', 'M', 'N'], 1)[0]
    ret['ATS'] = sample(['', 'Y'], 1)[0]
    ret['Modifier'] = '-'
    ret['Modifier2'] = '-'
    ret['Special'] = '-'
    ret['As-Of'] = '-'
    ret['Side'] = sample(['B', 'S'], 1)[0]
    ret['Reporting'] = 'D'  # or T
    ret['Contra'] = sample(['D', 'T', 'C'], 1)[0]
    if not first:
        P[company].append(ret)
        P[company] = P[company][-100:]  # keep last 100


class DataHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header('Content-Type', 'application/json')

    def get(self):
        '''Get the current list of client ids'''
        for c in P:
            generate(c)
        ret = []
        for c in P.values():
            ret.extend(c)
        self.write(ujson.dumps(ret[-100:]))


def main(*args, **kwargs):
    port = kwargs.get('port', 8889)
    handlers = [
        (r"/", DataHandler, {}),
    ]

    generateInitial()

    logging.root.setLevel(0)
    logging.info('Server listening on port: %s', port)

    application = tornado.web.Application(handlers)
    application.listen(port, address='0.0.0.0')
    tornado.ioloop.IOLoop.current().start()

main(port=9399)
