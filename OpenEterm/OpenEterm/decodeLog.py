#-*- coding: UTF-8 -*-
import datetime
class Page():
    def __init__(self, rawPage):
        self.rawPage = rawPage
        self.lines = self.rawPage.split('\r\n')
        self.logTime = self.lines[0]
        self.order = self.lines[2][1:]
        self.content = self.lines[3:]
        self.tokens = []
        self.parseOrder()

        for line in self.content:
            self.tokens += line.split()

    def  __repr__(self):
        return self.order

    def parseOrder(self):
        try:
            self.func , self.paras= self.order.split(':')
            self.paras = self.paras.split('/')
        except ValueError:
            print 'noParas func:', self.order
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
        return self.paras.split('/')[:]

    def getTokens(self):
        return self.tokens[:]

class Syntax():

    def __init__(self, pagesList):
        self.pagesList = pagesList
        self.funcList = []
        for  page in pagesList:
            self.funcList.append(page.getFunc())
        self.scanPages()

    def getPagesList(self):
        return self.pagesList[:]

    def scanPages(self):
        self.termList = []
        indexStart = indexEnd = 0
        for funcIndex in range(len(self.funcList)):
            if funcIndex == 0:
                continue
            if self.funcList[funcIndex] != 'pn' or funcIndex == len(self.funcList)-1:
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
        self.tokens = []
        for page in pagesList:
            self.tokens += page.getTokens()

    def __repr__(self):
        return self.name

    def getTokens(self):
        return self.tokens[:]

class Flp(Term):
    """docstring for Flp."""
    def __init__(self, pagesList):
        Term.__init__(self,pagesList)
        # super(Flp, self).__init__()
        self.tokens = [] #rewrite Term
        endIndex = 0
        for page in pagesList:
            pageContent = page.getContent()
            for line in pageContent[2:]:
                self.tokens += line.split()
        for index in range(len(self.tokens)):
            if self.tokens[index] == 'FLIGHT':
                endIndex = index
        self.tokens = self.tokens[:endIndex]

    def parasParse(self):
        self.

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
        return self.flightNo + ':' +　self.flightDate

    def setBooked(self, cabin, number):
        try:
            self.booked[cabin] = number
        except Exception as e:
            raise e

def dateParse(token):
    date = ''
    try:
        # print(token[0:4])
        date = datetime.datetime.strptime(token[0:5], "%d%b")
    except ValueError as e:
        pass
    if date:
        print 'date is :', date

def  progressParse(token):
    if token == '%':
        return True
    else:
        return False

def bookedParse(token):
    splitedToken = token.split('/')
    if len(splitedToken) > 5:
        for fragment in splitedToken:
            flight = Flight()

fo = open("D:\\iCloudDrive\\officeDesktop\\2017_07_21.log", "rb")
# fo = open("D:\\2017_07_25.log", "rb")
str = fo.read();
pages = str.split('\r\n\r\n')[:-1]
pagesArray = []
print "pages length : ", len(str)
for pageIndex in range(len(pages)):
    print '第%d页'%(pageIndex)
    page = Page(pages[pageIndex])
    # print 'It\'s tokens: ',page.getTokens()
    pagesArray.append(page)
fo.close()

syntax = Syntax(pagesArray)
terms = syntax.getTerms()
pagesArray[0].getContent
print 'page0 content: ', pagesArray[0].getContent()
print 'term0: ', terms[0].getTokens()

tokens = terms[0].getTokens()
for index,token in enumerate(tokens):
    dateParse(token)
    if progressParse(token):
        print tokens[index-1],"%"
#
