# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import sys
from dto import Vaccine, Supplier, Clinic, Logistic
from repositery import repo


def main():
    repo.create_tables()
    inputfile = open("config.txt", "r")
    line = inputfile.readline()
    indexlist = line.split(",")

    vaccines_amount = int(indexlist[0])
    suppliers_amount = int(indexlist[1])
    clinics_amount = int(indexlist[2])
    logistics_amount = int(indexlist[3])

    suppliers_amount = suppliers_amount + vaccines_amount
    clinics_amount = clinics_amount + suppliers_amount
    logistics_amount = logistics_amount + clinics_amount
    counter = 0
    while line != "":
        counter += 1
        line = inputfile.readline()
        line_by_list = line.split(",")
        if line != "":
            if counter <= vaccines_amount:
                vac = Vaccine(int(line_by_list[0]), line_by_list[1], int(line_by_list[2]), int(line_by_list[3]))
                repo.vaccines.insert(vac)

            if (counter > vaccines_amount) & (counter <= suppliers_amount):
                sup = Supplier(int(line_by_list[0]), line_by_list[1], int(line_by_list[2]))
                repo.suppliers.insert(sup)

            if (counter > suppliers_amount) & (counter <= clinics_amount):
                clin = Clinic(int(line_by_list[0]), line_by_list[1], int(line_by_list[2]), int(line_by_list[3]))
                repo.clinics.insert(clin)

            if counter > clinics_amount:
                log = Logistic(int(line_by_list[0]), line_by_list[1], int(line_by_list[2]), int(line_by_list[3]))
                repo.logistics.insert(log)


    orders = open("orders.txt", "r")  #sys.argv[2]
    order = orders.readline()
    order_by_list = order.split(",")
    while order_by_list != ['']:
        size = len(order_by_list)
        if size == 2:
            location = order_by_list[0]
            amount = order_by_list[1]
            repo.send_shipment(location, amount)
        if size == 3:
            name = order_by_list[0]
            amount = order_by_list[1]
            date = order_by_list[2]
            repo.receive_shipment(name, amount, date)

        if order != ['']:
            output = open("summary.txt", "a")
            output.write(repo.summary())
            order = orders.readline()
            order_by_list = order.split(",")


if __name__ == '__main__':
    main()

