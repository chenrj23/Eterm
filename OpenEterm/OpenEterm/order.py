#-*- coding: UTF-8 -*-
import datetime
def flp(flightNo,startDate, endDate, route, option=''):
    orders = []
    startDateObj = datetime.datetime.strptime(startDate, "%d%b")
    endDateObj = datetime.datetime.strptime(endDate, "%d%b")
    dayLong = (endDateObj - startDateObj).days

    if option:
        commend = 'flp:' + option + '/' + flightNo + '/' + startDate + '/' + endDate + '/' + route
        orders.append(commend)
    else:
        commend = 'flp:' + flightNo + '/' + startDate + '/' + endDate + '/' + route
        orders.append(commend)

    pnLong = dayLong // 11
    if pnLong > 0:
        for pnNumb in range(pnLong):
            orders.append('pn')
    print 'dayLong: ', dayLong
    print 'pnLong: ', pnLong
    print 'orders: ', orders


if __name__ == '__main__':
    flp('y87561', '8aug', '12sep', 'hethld', "")
