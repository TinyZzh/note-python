#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pyexcel as pe
import types
import os


def excel_book_append(filename, sheet_index, rows):
    if not os.path.exists(filename):
        book = pe.Book(None, filename)
    else:
        book = pe.get_book(file_name=filename)
    sheet = book.sheet_by_index(sheet_index)
    for row in rows:
        sheet.row += row
    book.save_as(filename)


def excel_append(filename, rows):
    if not os.path.exists(filename):
        sheet = pe.Sheet()
    else:
        sheet = pe.get_sheet(file_name=filename)
    for row in rows:
        if isinstance(row, tuple):
            sheet.row += list(row)
        elif isinstance(row, list):
            sheet.row += row
    sheet.save_as(filename)


def export_excel(filename, columns, rows_map):
    if not isinstance(rows_map, dict) or not isinstance(columns, list):
        return
    _data = []
    for k, v in rows_map.iteritems():
        _line_data = [k, ]
        for column_name in columns:
            _value = v[column_name] if column_name in v else ''
            _line_data.append(str(_value))
        _data.append(_line_data)
    columns.insert(0, "")  # A1 = ""
    _data.insert(0, columns)
    excel_append(filename, _data)
