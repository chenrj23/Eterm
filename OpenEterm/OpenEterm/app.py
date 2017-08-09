#-*- coding: UTF-8 -*-
import OpenEterm, decodeLog
from time import sleep

eterm = OpenEterm.OpenEterm()
eterm.OpenEterm()
OpenEterm.typer('flp:j/y87561/./12sep/szxhet')
OpenEterm.press('F12')
sleep(1)

fo = open("D:\\iCloudDrive\\officeDesktop\\2017_07_27.log", "rb")
str = fo.read();
position = fo.tell();
pages = str.split('\r\n\r\n')[:-1]
pagesArray = []
print "pages length : ", len(pages)
for pageIndex in range(len(pages)):
    print '第%d页'%(pageIndex)
    page = decodeLog.Page(pages[pageIndex])
    # print 'It\'s tokens: ',page.getTokens()
    pagesArray.append(page)
fo.close()


syntax = decodeLog.Syntax(pagesArray)
print 'funcList: ', syntax.funcList
terms = syntax.getTerms()
print 'term: ', terms
print 'term[0]: ', terms[0]
print 'term[0]: pagelisht  ', terms[0].getPagesList()
print 'term[0]: tokens  ', terms[0].getTokens()
# print 'term[0] flights: ', terms[0].getFlights()
tmp = terms[0].getFlights()
for value in tmp:
    print value
    print tmp[value].getBooked()
    print tmp[value].getProgress()




#
OpenEterm.typer('flp:j/y87561/./12sep/hethld')
OpenEterm.press('F12')
sleep(1)
#
fo = open("D:\\iCloudDrive\\officeDesktop\\2017_07_27.log", "rb")
fo.seek(position, 0)
str = fo.read();
position = fo.tell();
pages = str.split('\r\n\r\n')[:-1]
pagesArray = []
print "pages length : ", len(pages)
for pageIndex in range(len(pages)):
    print '第%d页'%(pageIndex)
    page = decodeLog.Page(pages[pageIndex])
    # print 'It\'s tokens: ',page.getTokens()
    pagesArray.append(page)
fo.close()


print "当前文件位置 : ", position
print "当前文件内容 : ", str
fo.close()

syntax = decodeLog.Syntax(pagesArray)
print 'funcList: ', syntax.funcList
terms = syntax.getTerms()
print 'term: ', terms
print 'term[0]: ', terms[0]
print 'term[0]: pagelisht  ', terms[0].getPagesList()
print 'term[0]: tokens  ', terms[0].getTokens()
# print 'term[0] flights: ', terms[0].getFlights()
tmp = terms[0].getFlights()
for value in tmp:
    print value
    print tmp[value].getBooked()
    print tmp[value].getProgress()
