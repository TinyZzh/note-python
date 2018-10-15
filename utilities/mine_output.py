#!/usr/bin/python
# -*- coding: UTF-8 -*-

#  输出文本工具

import os


def output_list(file_path, header, lines, **kw):
    io_file = os.open(file_path, os.O_CREAT | os.O_WRONLY | os.O_APPEND)
    try:
        if header:
            os.write(io_file, '\t'.join(map(str, header)).encode())
        os.write(io_file, '\n'.encode())
        os.write(io_file, '\n'.join(lines).encode())
    finally:
        os.close(io_file)
    return


def output(file_path, data):
    io_file = os.open(file_path, os.O_CREAT | os.O_WRONLY | os.O_APPEND)
    try:
        os.write(io_file, data.encode())
    finally:
        os.close(io_file)
    # with open(file_path, 'a') as io_file:
    #     io_file.write(data)
    return


def output_rows(file_path, rows, header=[], **kw):
    io_file = os.open(file_path, os.O_CREAT | os.O_WRONLY | os.O_APPEND)
    try:
        # print table header.
        if header:
            os.write(io_file, "\t".join(map(str, header)).encode())
            os.write(io_file, "\n".encode())
        # print row data
        for column in rows:
            os.write(io_file, "\t".join(map(str, column)).encode())
            os.write(io_file, "\n".encode())
    finally:
        os.close(io_file)
    # with open(file_path, 'a') as io_file:
    #     for column in rows:
    #         io_file.write("\t".join(map(str, column)))
    #         io_file.write("\r\n")
    return
