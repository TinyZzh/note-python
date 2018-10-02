#!/usr/bin/python
# -*- coding: UTF-8 -*-
from collections import OrderedDict

import pyexcel as pe
from pyexcel.sheets.sheet import Sheet
import pyexcel_xls

from utilities import excel_util


def show():
    # file = pyexcel.get_records(file_name="your_file.xls")

    book = pe.get_book(file_name="excel_example.xls")
    sheet = book.sheet_by_index(0)
    sheet.row += ["1", "2", "3", "4"]
    book.save_as("excel_example.xls")

    # sheet = pe.get_sheet(file_name="excel_l1.xls")
    # sheet.row += ["1", "2", "3", "4"]
    # sheet.row += ["1", "2", "3", "4"]
    # print sheet.to_array()
    # sheet.save_as("excel_l1.xls")

    return


def _main():
    # _total_data = []
    # out_excel = OrderedDict()
    # out_excel.update({"na_bug_20160921": _total_data})
    # # pyexcel_xls.save_data("platform_" + server_info[0] + ".xls", out_excel)
    # pyexcel_xls.save_data("na_bug_20160921.xls", out_excel)

    _columns = ["Name", "Age"]
    _rows_map = {
        "John": {
            "Name": "John",
            "Age": 15
        },
        "Green": {
            "Name": "Green",
            "Age": 18
        }
    }
    excel_util.export_excel("xx.xls", _columns, _rows_map)

    pass


if __name__ == '__main__':
    _main()
    print "end"
