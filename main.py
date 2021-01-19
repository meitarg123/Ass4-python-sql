# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
#import os
#import sqlite3
#import atexit
#from dto import Vaccine, Supplier, Clinic, Logistic
import repositery
import sys
from dto import Vaccine
from repositery import repo


def main():
#    repo.create_tables()
    print(5)
    inputfile = open("config.txt", "r")
    line = inputfile.readline()
    indexlist = line.split(",")

    vaccines_amount = int(indexlist[0])
    suppliers_amount = int(indexlist[1])
    clinics_amount = int(indexlist[2])
    logistics_amount = int(indexlist[3])
    counter = 0
    while line != None:
        counter += 1
        line = inputfile.readline()
        line_by_list = line.split(",")

        if counter <= vaccines_amount:
            repo.vaccines.insert(Vaccine(*line_by_list))
#            repo._Vaccines.insert(Vaccine(*line_by_list))

        if counter > vaccines_amount & counter < clinics_amount:
            repo.suppliers.insert(line_by_list)

        if counter > suppliers_amount & counter < logistics_amount:
            repo.clinics.insert(line_by_list)

        if counter >= logistics_amount:
            repo.logistics.insert(line_by_list)

    with open(sys.argv[2]) as inputorder:
        file = open("output.txt", "a")
        order = inputorder.readline()
        order_by_list = order.split(",")
        while order_by_list != None:
            size = len(order_by_list)
            if size == 2:
                location = order_by_list[0]
                amount = order_by_list[1]
                repo.send_shipment(location, amount)
            else:
                name = order_by_list[0]
                amount = order_by_list[1]
                date = order_by_list[2]
                repo.receive_shipment(name, amount, date)
            order = inputorder.readline()
            if order != None:
                order_by_list = order.split(",")
            file.write(repo.summary())

if __name__ == '__main__':
  main()

