#-*- coding: UTF-8 -*-

class Page():
    def __init__(self, pageLines):
        self.lines = pageLines
        try:
            self.logTime = self.lines[0]
            self.order = self.lines[2][1:]
            self.contents = self.lines[3:]
            self.pareOrder()
        except Exception as e:
            print 'page lines not enough, lines: ', self.lines
            # raise Exception("lines no long enough", self.lines)

    def pareOrder(self):
        try:
            self.func , self.paras= self.order.split(':')
            self.paras = self.paras.split('/')
        except ValueError:
            print 'noParas func:', self.order
            self.func = self.order
            self.paras = []

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

# print pagesArray[1].order
# pagesArray[1].pareOrder()
# print pagesArray[1].func
# print pagesArray[1].paras
