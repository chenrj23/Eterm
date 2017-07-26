#-*- coding: UTF-8 -*-

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

    # def parseFLPJ(self):
    #     cleanTokens = filter(None, self.getTokens())
    #     print 'cleanTokens: ', cleanTokens


class SyntaxParse():
    def __init__(self, pagesList):
        self.funcList = []
        for  page in pagesList:
            self.funcList.append(page.order)

    def package(self):
        self.packagelist = []
        indexStart = indexEnd = 0
        for funcIndex in range(len(self.funcList)):
            if funcIndex == 0:
                continue
            if self.funcList[funcIndex] != 'pn' or funcIndex == len(self.funcList)-1:
                indexEnd = funcIndex
                self.packagelist.append(pagesArray[indexStart:indexEnd])
                indexStart = indexEnd

    def  getPackages(self):
        return self.packagelist[:]

    def  parseFLPJ(self, package):
        package.content = []
        for page in package:
            package.content += page.cleanTokens

# fo = open("D:\\iCloudDrive\\officeDesktop\\2017_07_21.log", "rb")
fo = open("D:\\2017_07_25.log", "rb")
str = fo.read();
pages = str.split('\r\n\r\n')[:-1]
pagesArray = []
print "pages length : ", len(str)
for pageIndex in range(len(pages)):
    print '第%d页'%(pageIndex)
    page = Page(pages[pageIndex])
    print 'It\'s tokens: ',page.getTokens()
    pagesArray.append(page)
fo.close()

#
# for page in pagesArray:
#     print 'page logTime: ', page.logTime
#     print 'page order: ', page.order
#     print 'page func: ', page.func
#     print 'page paras: ', page.paras
#     print 'page body: ', page.body
#     print 'page parseFLPJ: ', page.parseFLPJ()
#     print ' '
#
# syntaxPages = SyntaxParse(pagesArray)
# syntaxPages.package()
# print 'func list: ',  syntaxPages.funcList
# packages = syntaxPages.getPackages()
# print 'package list: ',  packages
#
# syntaxPages.parseFLPJ(packages[0])
# print 'packages[0] content: ', packages[0].content

# print pagesArray[1].order
# pagesArray[1].parseOrder()
# print pagesArray[1].func
# print pagesArray[1].paras
