#!/usr/bin/python
# -*- coding: UTF-8 -*-

#  输出文本工具

import os


def output(file_path, data):
    io_file = os.open(file_path, os.O_CREAT | os.O_WRONLY | os.O_APPEND)
    os.write(io_file, data)
    os.close(io_file)
    # with open(file_path, 'a') as io_file:
    #     io_file.write(data)
    return


def output_rows(file_path, rows):
    io_file = os.open(file_path, os.O_CREAT | os.O_WRONLY | os.O_APPEND)
    for column in rows:
        os.write(io_file, "\t".join(map(str, column)))
        os.write(io_file, "\n")
    os.close(io_file)
    # with open(file_path, 'a') as io_file:
    #     for column in rows:
    #         io_file.write("\t".join(map(str, column)))
    #         io_file.write("\r\n")
    return
