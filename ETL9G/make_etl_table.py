# this code is exiting 'https://qiita.com/kcrt/items/a7f0582a91d6599d164d'
# this code is should exit ETL9G/
# make a table, all of ETL9G_XX, (don't devide to category)
import struct
import numpy as np
import os
import sys
from PIL import Image
import csv

RECORD_SIZE = 8199


def init_csv_file(filename):
    # initialize tabel file ()
    with open(filename, mode='w', newline='') as csvf:
        writer = csv.writer(csvf)
        writer.writerow(['index', ''])

def make_table(etl_filename, csv_filename):
    i = 0
    etl_filename = os.path.join(os.path.abspath(__file__), "..", etl_filename)
    with open(etl_filename, 'rb') as f:
        while True:
            # reading one image from 'sys.argv[1]' like a 'ETL9G_01'
            s = f.read(RECORD_SIZE)
            if s is None or len(s) < RECORD_SIZE:
                break
            # unpackaging from binay file. refer to 'https://techacademy.jp/magazine/19058'
            # refer to 'http://etlcdb.db.aist.go.jp/specification-of-etl-8'
            r = struct.unpack("> 2H8sI4B4H2B30x8128s11x", s)
            i = i + 1
            dirname = b'\x1b$B' + r[1].to_bytes(2, 'big') + b'\x1b(B'
            dirname = dirname.decode("iso-2022-jp")
            
            # write index and char to 'table.csv'
            with open(csv_filename, mode='a', newline='', encoding='utf-8') as csvf:
                writer = csv.writer(csvf)
                writer.writerow([str(i), str(dirname), "ok"])

# get the list of filename in the ETL9G/
all_etl_files = os.listdir(os.path.join(os.path.abspath(__file__),".."))

# if exit .xxx, the file is not ETL file, and should excluded.
new_list = []
for etl in all_etl_files:
    root, ext = os.path.splitext(etl)
    if(ext == ''):
        new_list.append(etl)
        print(root, '(', ext, ')', 'is etl file.')
    else:
        print(root, '(', ext, ')', 'is not etl file.')

all_etl_files = new_list

for etl in all_etl_files:
    csv_filename = str(etl) + '_table.csv'
    csv_filename = os.path.join(__file__, "..", csv_filename)
    init_csv_file(csv_filename)
    print('generated ', csv_filename)
    make_table(etl, csv_filename)
    print('created successfully ', csv_filename)