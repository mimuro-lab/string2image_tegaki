# this code is exiting 'https://qiita.com/kcrt/items/a7f0582a91d6599d164d'
# this code is should exit ETL9G/
# make a table, all of ETL9G_XX, (don't devide to category)
import struct
import numpy as np
import os
import sys
from PIL import Image
import csv
import jaconv

RECORD_SIZE = 2052

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
            r = struct.unpack(">H2sHBBBBBBIHHHHBBBBHH2016s4x", s)
            img = Image.frombytes('F', (64, 63), r[20], 'bit', (4, 0))
            img = np.array(img.convert('L'))  # 0..15
            #print(r[0:5], type(r[3].to_bytes(1,"big")))
            #print(r[3].to_bytes(1,"big"))
            #print(r[3].to_bytes(1,"big").decode('shift_jis'))
            lbl = r[3].to_bytes(1,"big").decode('shift_jis') # 文字コード
            lbl = jaconv.h2z(lbl,digit=True, ascii=True)

            #lbl = r[3].to_bytes(1,"big").decode('utf-8') # 文字コード
            #dirname = bytes.fromhex(lbl).decode('jis_x_0201')
            #input()
            # write index and char to 'table.csv'
            
            with open(csv_filename, mode='a', newline='', encoding='utf-8') as csvf:
                writer = csv.writer(csvf)
                writer.writerow([str(r[0] - 1), str(lbl), "ok"])
            i += 1

def fixOffset(csv_filename):
    reader = csv.reader(open(csv_filename, encoding="utf-8", mode="r"))
    reader = [row for row in reader]
    # ずれを直す
    tmp = []
    pre_chr = ""
    now_chr = ""
    for e in reader:
        now_chr = e[1]
        if(now_chr != pre_chr and pre_chr != ""):
            tmp.append([e[0], pre_chr, e[2]])
        else:
            tmp.append(e)

        pre_chr = now_chr
        
    with open(csv_filename, mode='w', newline='', encoding="utf-8") as csvf:
        writer = csv.writer(csvf)
        writer.writerows(tmp)
    
        
#fixOffset(os.path.join(__file__, "..", "ETL6C_02_table.csv"))


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
    fixOffset(csv_filename)
    print('created successfully ', csv_filename)
