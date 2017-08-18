#-*- coding: UTF-8 -*-
import OpenEterm
import order
import decodeLog
from time import sleep
#
eterm = OpenEterm.OpenEterm()
eterm.OpenEterm()

decode = decodeLog.Decode("../../test.log")
# decode = decodeLog.Decode("D:\\iCloudDrive\\officeDesktop\\2017_07_27.log")
# orders = order.flp('y87565', '14aug', '12sep', 'szxcgo', "j")
# for cmd in orders:
#     OpenEterm.typer(cmd)
#     OpenEterm.press('F12')
#     sleep(1)
#
decode.next()
terms = decode.getTerms()

# print 'terms', terms
#
for term in terms:
    flights = term.getFlights()
    print 'term logTime: ',  term.logTime
    print 'flights len: ',  len(flights)
    print 'flights: ',  flights
    for flight in flights:
        flight.save()
#
# orders = order.flp('y87566', '14aug', '12sep', 'cgoszx', "j")
# for cmd in orders:
#     OpenEterm.typer(cmd)
#     OpenEterm.press('F12')
#     sleep(1)
#
# decode.next()
# terms = decode.getTerms()
#
# print 'terms', terms
#
# for term in terms:
#     flights = term.getFlights()
#     print 'term logTime: ',  term.logTime
#     print 'flights len: ',  len(flights)
#     print 'flights: ',  flights
#     for flight in flights:
#         flight.save()
#
#







        # print flight.getFlightDate()
        # print flight.getBooked()

# orders = order.flp('y87561', '9aug', '12sep', 'szxhet', "j")
# for cmd in orders:
#     OpenEterm.typer(cmd)
#     OpenEterm.press('F12')
#     sleep(1)
#
# decode.next()
# terms = decode.getTerms()
# for term in terms:
#     flights = term.getFlights()
#     print 'term logTime: ',  term.logTime
#     print 'flights len: ',  len(flights)
#     print 'flights: ',  flights
#
#
# orders = order.flp('y87565', '9aug', '12sep', 'szxcgo', "j")
# for cmd in orders:
#     OpenEterm.typer(cmd)
#     OpenEterm.press('F12')
#     sleep(1)
#
# decode.next()
# terms = decode.getTerms()
# for term in terms:
#     flights = term.getFlights()
#     print 'term logTime: ',  term.logTime
#     print 'flights len: ',  len(flights)
#     print 'flights: ',  flights
