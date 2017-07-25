#-*- coding: UTF-8 -*-

class Page():
    def __init__(self, pageLines):
        self.lines = pageLines
        # try:
        self.logTime = self.lines[0]
        self.order = self.lines[2][1:]
        content = self.lines[3:]
        self.body = [ content[i].split() for  i in range(len(content))]
        self.parseOrder()
        # except Exception as e:
        #     print 'page lines not enough, lines: ', self.lines
            # raise Exception("lines no long enough", self.lines)

    def parseOrder(self):
        try:
            self.func , self.paras= self.order.split(':')
            self.paras = self.paras.split('/')
        except ValueError:
            print 'noParas func:', self.order
            self.func = self.order
            self.paras = []

    def getTokens(self):
        return self.body[:]

    def parseFLPJ(self):
        cleanTokens = filter(None, self.getTokens())
        print 'cleanTokens: ', cleanTokens


class SyntaxParse():
    def __init__(self, pagesList):
        self.orderList = []
        for  page in pagesList:
            self.orderList.append(page.order)

# fo = open("D:\\iCloudDrive\\officeDesktop\\2017_07_21.log", "rb")
fo = open("D:\\iCloudDrive\\officeDesktop\\2017_07_21.log", "rb")
str = fo.read();
pages = str.split('\r\n\r\n')[:-1]
pagesArray = []
print "pages length : ", len(str)
for pageIndex in range(len(pages)):
    print '第%d页'%(pageIndex)
    lines = pages[pageIndex].split('\r\n')
    pagesArray.append(Page(lines))
fo.close()


for page in pagesArray:
    print 'page logTime: ', page.logTime
    print 'page order: ', page.order
    print 'page func: ', page.func
    print 'page paras: ', page.paras
    print 'page body: ', page.body
    print 'page parseFLPJ: ', page.parseFLPJ()
    print ' '

print 'order list: ',  SyntaxParse(pagesArray).orderList
# print pagesArray[1].order
# pagesArray[1].parseOrder()
# print pagesArray[1].func
# print pagesArray[1].paras
