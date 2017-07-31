#-*- coding: UTF-8 -*-
import datetime
class Page():
    def __init__(self, rawPage):
        self.rawPage = rawPage
        self.lines = self.rawPage.split('\r\n')
        self.logTime = self.lines[0]
        self.content = self.lines[3:]
        self.order = ''
        self.tokens = []
        self.parseOrder()

        for line in self.content:
            self.tokens += line.split()

    def  __repr__(self):
        return self.order

    def parseOrder(self):
        try:
            self.order = self.lines[2][1:]
            self.func , self.paras= self.order.split(':')
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
        for  page in pagesList:
            self.funcList.append(page.getFunc())
        self.scanPages()

    def getPagesList(self):
        return self.pagesList[:]

    def scanPages(self):
        indexStart = indexEnd = 0
        self.funcList.append('END') #为方便截取
        for funcIndex in range(len(self.funcList)):
            if funcIndex == 0:   #开始时因为假定都是指令开头
                continue
            if self.funcList[funcIndex] != 'pn':
                indexEnd = funcIndex
                if self.funcList[indexStart] == 'flp':
                    term = Flp(pagesArray[indexStart:indexEnd])
                else:
                    raise Exception('unknow func', self.funcList[indexStart])
                self.termList.append(term)
                indexStart = indexEnd

    def  getTerms(self):
        return self.termList[:]

class Term():
    def __init__(self, pagesList):
        self.name = pagesList[0].getFunc()
        self.paras = pagesList[0].getParas()
        self.pagesList = pagesList
        self.tokens = []
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
        Term.__init__(self,pagesList)
        self.tokens = [] #rewrite Term
        self.flightNo = ''
        self.route=''
        endIndex = 0
        for page in pagesList:
            pageContent = page.getContent()
            for line in pageContent[2:]:
                self.tokens += line.split()
        for index in range(len(self.tokens)):
            if self.tokens[index] == 'FLIGHT':
                endIndex = index
        self.tokens = self.tokens[:endIndex]
        self.parasParse()

    def parasParse(self):
        self.flightNo = self.paras[1]
        self.route = self.paras[4]

    def getFlightNo(self):
        return self.flightNo

    def getRoute(self):
        return self.route

class Flight():
    def __init__(self,flightNo, flightDate):
        self.flightNo = flightNo
        self.flightDate = flightDate
        self.booked = {
        'C': 0,
        'D': 0,
        'I': 0,
        'J': 0,
        'Y': 0,
        'B': 0,
        'H': 0,
        'K': 0,
        'L': 0,
        'M': 0,
        'Q': 0,
        'X': 0,
        'U': 0,
        'E': 0,
        'N': 0,
        'T': 0,
        'R': 0,
        'W': 0,
        'V': 0,
        'G': 0,
        '0': 0,
        'S': 0,
        }

    def __repr__(self):
        return self.flightNo + ':' + self.flightDate

    def setBooked(self, cabin, number):
        try:
            self.booked[cabin] = number
        except Exception as e:
            raise e

def dateParse(token):
    date = ''
    try:
        date = datetime.datetime.strptime(token[0:5], "%d%b")
    except ValueError as e:
        pass
        # raise e
    if date:
        return date
    else:
        return False

def  progressParse(token):
    if token == '%':
        return True
    else:
        return False

def bookedParse(token):
    bookedData = {}
    splitedToken = token.split('/')
    splitedToken = filter(None, splitedToken) #remove empty terms in list
    if len(splitedToken) >= 3:
        for fragment in splitedToken:
            cabin = fragment[0]
            numb = fragment[1]
            bookedData[cabin] = numb

    return bookedData

fo = open("D:\\iCloudDrive\\officeDesktop\\test.log", "rb")
# fo = open("D:\\2017_07_25.log", "rb")
str = fo.read();
pages = str.split('\r\n\r\n')[:-1]
pagesArray = []
print "pages length : ", len(pages)
for pageIndex in range(len(pages)):
    print '第%d页'%(pageIndex)
    page = Page(pages[pageIndex])
    # print 'It\'s tokens: ',page.getTokens()
    pagesArray.append(page)
fo.close()

syntax = Syntax(pagesArray)
print 'funcList: ', syntax.funcList
terms = syntax.getTerms()
print 'term: ', terms

flights = []

for term in terms:
    print 'term flightNo: ', term.getFlightNo()
    print 'term Route: ', term.getRoute()
    # print 'term Tokens: ', term.getTokens()
    tokens = term.getTokens()
    # print 'term pagesList: ', term.getPagesList()
    for index,token in enumerate(tokens):
        parsedDate = dateParse(token)
        bookedData = bookedParse(token)
        if parsedDate:
            print parsedDate
            flight = Flight(term.getFlightNo, parsedDate)
        if bookedData:
            print 'bookedData: ', bookedData
        if progressParse(token):
            print tokens[index-1],"%"
#
