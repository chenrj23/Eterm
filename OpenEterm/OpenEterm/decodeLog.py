#-*- coding: UTF-8 -*-
import datetime, copy, time, MySQLdb
from collections import OrderedDict

dbPassword = raw_input("please write you DB password: ");

class DB:
    conn = None

    def connect(self):
        self.conn = MySQLdb.connect(
            "120.27.5.155", "root",dbPassword, "eterm")
        self.conn.autocommit(True)

    def execute(self, sql):
        print 'sql： ', sql
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
        except (AttributeError, MySQLdb.OperationalError):
            print 'connect break'
            print AttributeError
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute(sql)
        return cursor


db = DB()


class Decode():
    def __init__(self, filePath, startPosition=0):
        self.filePath = filePath
        self.position = startPosition
        self.terms = []

    def next(self):
        fo = open(self.filePath, "rb")
        fo.seek(self.position, 0)
        str = fo.read()
        self.position = fo.tell()
        fo.close()

        pages = Pages(str)
        pagesList = pages.getPagesList()
        syntax = Syntax(pagesList)
        self.terms = syntax.getTerms()

    def getTerms(self):
        return self.terms[:]


class Pages():
    def __init__(self, rawStr):
        self.rawStr = rawStr
        self.splitStr = rawStr.split('\r\n\r\n')[:-1]
        self.pagesList = [Page(pageStr) for pageStr in self.splitStr]

    def getPagesList(self):
        return self.pagesList[:]


class Page():
    def __init__(self, rawPage):
        self.rawPage = rawPage
        self.lines = self.rawPage.split('\r\n')
        self.logTime = self.lines[0].split('\n')[-1]
        self.logTime = datetime.datetime.strptime(
            self.logTime, "%Y %B %d, %A, %H:%M:%S")
        print 'logTime ', self.logTime
        # self.parseLog()
        self.content = self.lines[3:]
        self.order = ''
        self.tokens = []
        self.parseOrder()

        for line in self.content:
            self.tokens += line.split()

    def __repr__(self):
        return self.order

    def parseOrder(self):
        try:
            self.order = self.lines[2][1:]
            self.func, self.paras = self.order.split(':')
            self.paras = self.paras.split('/')
        except (ValueError, IndexError):
            print 'noParas func:', self.order
            print 'page lines[0]:', self.lines[0]
            print 'page lines[1]:', self.lines[1]
            print 'page lines[2]:', self.lines[2]
            print 'page lines[3]:', self.lines[3]
            self.func = self.order
            self.paras = []

    def getRawPage(self):
        return self.rawPage

    def getLines(self):
        return self.lines[:]

    def getContent(self):
        return self.content[:]

    def getFunc(self):
        return self.func

    def getParas(self):
        return self.paras[:]

    def getTokens(self):
        return self.tokens[:]


class Syntax():

    def __init__(self, pagesList):
        self.pagesList = pagesList
        self.funcList = []
        self.termList = []
        for page in pagesList:
            self.funcList.append(page.getFunc())
        self.scanPages()

    def getPagesList(self):
        return self.pagesList[:]

    def scanPages(self):
        indexStart = indexEnd = 0
        self.funcList.append('END')  # 为方便截取
        for funcIndex in range(len(self.funcList)):
            if funcIndex == 0:  # 开始时因为假定都是指令开头
                continue
            if self.funcList[funcIndex] != 'pn':
                indexEnd = funcIndex
                if self.funcList[indexStart] == 'flp':
                    term = Flp(self.pagesList[indexStart:indexEnd])
                else:
                    raise Exception('unknow func', self.funcList[indexStart])
                self.termList.append(term)
                indexStart = indexEnd

    def getTerms(self):
        return self.termList[:]


class Term():
    def __init__(self, pagesList):
        self.name = pagesList[0].getFunc()
        self.paras = pagesList[0].getParas()
        self.pagesList = pagesList
        self.tokens = []
        self.logTime = pagesList[0].logTime
        for page in pagesList:
            self.tokens += page.getTokens()

    def __repr__(self):
        return self.name

    def getTokens(self):
        return self.tokens[:]

    def getPagesList(self):
        return self.pagesList[:]


class Flp(Term):
    """docstring for Flp."""

    def __init__(self, pagesList):
        Term.__init__(self, pagesList)
        self.tokens = []  # rewrite Term
        self.flightNo = ''
        self.route = ''
        self.flights = {}
        endIndex = 0
        for page in pagesList:
            pageContent = page.getContent()
            for line in pageContent[2:]:
                self.tokens += line.split()
        for index in range(len(self.tokens)):
            if self.tokens[index] == 'FLIGHT':
                endIndex = index
                self.tokens = self.tokens[:endIndex]
                break
        self.parasParse()
        self.tokenParse()

    def parasParse(self):
        self.flightNo = self.paras[1]
        self.route = self.paras[4]

    def getFlightNo(self):
        return self.flightNo

    def getRoute(self):
        return self.route

    def getFlights(self):
        return copy.deepcopy(self.flights)

    def tokenParse(self):
        for index, token in enumerate(self.tokens):
            parsedDate = dateParse(token)
            bookedData = bookedParse(token)
            if parsedDate:
                # print parsedDate
                flight = Flight(self.flightNo, parsedDate, self.logTime)
                self.flights[flight] = flight
                # print 'flight :', flight
                # self.flight[flight]
            if bookedData:
                # print 'bookedData: ', bookedData
                for (cabin, numb) in bookedData.items():
                    flight.setBooked(cabin, numb)
            if progressParse(token):
                # print self.tokens[index-1],"%"
                amount = int(self.tokens[index - 1])
                flight.setProgress(amount)


class Flight():
    def __init__(self, flightNo, flightDate, logTime):
        self.flightNo = flightNo
        self.flightDate = flightDate
        self.logTime = logTime
        self.progress = 0
        self.booked = OrderedDict([('C',0), ('D',0), ('I',0), ('J',0), ('Y',0), ('B',0), ('H',0), ('K',0), ('L',0), ('M',0),
         ('Q',0), ('X',0), ('U',0), ('E',0), ('N',0), ('T',0), ('V',0), ('R',0), ('W',0), ('P',0), ('G',0), ('O',0), ('S',0)])
# self.booked = {
#     'C': 0,
#     'D': 0,
#     'I': 0,
#     'J': 0,
#     'Y': 0,
#     'B': 0,
#     'H': 0,
#     'K': 0,
#     'L': 0,
#     'M': 0,
#     'Q': 0,
#     'X': 0,
#     'U': 0,
#     'E': 0,
#     'N': 0,
#     'T': 0,
#     'V': 0,
#     'R': 0,
#     'W': 0,
#     'P': 0,
#     'G': 0,
#     'O': 0,
#     'S': 0,
# }

    def __repr__(self):
        return self.flightNo + '-' + self.flightDate.strftime('%d%b%y')

    def save(self):
        airlineCode = self.flightNo[0:2]
        flightNo = self.flightNo[2:]
        depDate = self.flightDate.isoformat()
        LF = self.progress
        booked = tuple(self.booked.values())
        logTime = (self.logTime.isoformat(),)

        # depDateTime
        model = (airlineCode, flightNo, depDate, LF) + booked + logTime
        db.execute("""INSERT INTO flights  (airlineCode, flightNo, depDate, LF, CB, DB, IB, JB, YB, BB, HB, KB, LB, MB, QB, XB, UB, EB, NB, TB, VB, RB, WB, PB, GB, OB, SB, logTime) VALUES ('%s', '%s' ,'%s' ,%d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, '%s')""" % model)

        print model

    def setProgress(self, amount):
        ``` amount is int ```
        self.progress = amount

    def setBooked(self, cabin, number):
        try:
            self.booked[cabin] = number
        except Exception as e:
            raise e

    def getFlightNo(self):
        return self.flightNo

    def getFlightDate(self):
        return self.flightDate

    def getBooked(self):
        return copy.deepcopy(self.booked)

    def getProgress(self):
        return self.progress

    def getLogTime(self):
        return copy.deepcopy(self.logTime)


def dateParse(token):
    date = ''
    try:
        date = datetime.datetime.strptime(token[0:5], "%d%b")
        date = date.replace(date.today().year).date()
    except ValueError as e:
        pass
        # raise e
    if date:
        return date
    else:
        return False


def progressParse(token):
    if token == '%':
        return True
    else:
        return False


def bookedParse(token):
    bookedData = {}
    splitedToken = token.split('/')
    splitedToken = filter(None, splitedToken)  # remove empty terms in list
    if len(splitedToken) >= 3:
        for fragment in splitedToken:
            cabin = fragment[0]
            numb = fragment[1:]
            bookedData[cabin] = int(numb)

    return bookedData


if __name__ == '__main__':
    decode = Decode("D:\\iCloudDrive\\officeDesktop\\2017_07_27.log")
    # decode = Decode("../../test.log")
    decode.next()
    terms = decode.getTerms()
    for term in terms:
        flights = term.getFlights()
        print 'flights len: ',  len(flights)
        print 'flights: ',  flights
