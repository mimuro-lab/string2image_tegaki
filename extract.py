import struct
from PIL import Image
import os, sys, csv

from matlab.extract import pick_image as getImg_EMNIST

import scipy.io as sio

sum_datasets = 40
sum_words = 3036
img_trim_widht = 22
img_trim_height = 32
img_height = 127
img_width = 128
        
# matlabのemnist
pathToMat = os.path.join(__file__, "..", "ETL", "emnist-byclass.mat")
mat_contents = sio.loadmat(pathToMat)
training_img = mat_contents['dataset'][0][0][0][0][0][0]

def add_margin(pil_img, top, right, bottom, left, color):
    width, height = pil_img.size
    new_width = width + right + left
    new_height = height + top + bottom
    result = Image.new("RGB", (new_width, new_height), color)
    result.paste(pil_img, (left, top))
    return result

# get one image from etl_filename by referencing img_index(corrspoinding file, type-csv)
def get_img(etl_filename, img_index):
    RECORD_SIZE = 0
    if("ETL9" in etl_filename):
        RECORD_SIZE = 8199
    if("ETL6" in etl_filename):
        RECORD_SIZE = 2052
    if("emnist-byclass" in etl_filename):
        img = getImg_EMNIST(training_img, img_index)
        w,h = img.size
        img = img.resize((w * 3, h * 3))
        campus = Image.new("RGB", (w * 3, img_height), (255,255,255))
        img = add_margin(img, 43, 0, 0, 0, (255,255,255))
        return img
    with open(etl_filename, 'rb') as f:
        if(img_index != 0):
            img_index = img_index - 1
        # reading one image from 'sys.argv[1]' like a 'ETL9G_01'
        f.seek(RECORD_SIZE*img_index)
        s = f.read(RECORD_SIZE)
        # unpackaging from binay file. refer to 'https://techacademy.jp/magazine/19058'
        # refer to 'http://etlcdb.db.aist.go.jp/specification-of-etl-8'
        if("ETL9" in etl_filename):
            r = struct.unpack("> 2H8sI4B4H2B30x8128s11x", s)
            img = Image.frombytes('F', (128, 127), r[14], 'bit', (4, 0))
            img = img.convert('L')
            img = img.point(lambda x: 255 - (x << 4))
            img = img.resize((int(img_width * 1.5), int(img_height * 1.5)))
            w, h = img.size
            img = img.crop((img_trim_widht, img_trim_height, w - img_trim_widht, h - img_trim_height))
            return img
        if("ETL6" in etl_filename):
            #print(etl_filename)
            r = struct.unpack(">H2sHBBBBBBIHHHHBBBBHH2016s4x", s)
            img = Image.frombytes('F', (64, 63), r[20], 'bit', (4, 0))
            img = img.convert('L')
            img = img.point(lambda x: 255 - (x << 4))
            img = img.resize((128, 127))
            return img

# 一つのETLテーブルから、入力された文字に対応するINDEXを返す（無かったら－１）
def searchIND_oneTABEL(c:str, table:str) -> int:
    fp = open(table, encoding="utf-8")
    reader = csv.reader(fp)
    reader = [row for row in reader]
    #print(reader)
    #print(reader)
    status = "none"
    # tableを全てサーチ
    for e in reader:
        # 文字が一致する,且つ,未使用
        if(len(e) != 3):
            continue
        if(e[1] == c):
            status = "exit"
        if(e[1] == c and e[2] == 'ok'):
            return int(e[0])

    # 見つからなかった時・未使用が無かった時、stasusを返す
    return status

# ETL表のインデックスを使用済みに更新する
def update_oneTABLE(ind:int, table:str):
    fp = open(table, encoding="utf-8")
    reader = csv.reader(fp)
    reader = [row for row in reader]
    # tableを全てサーチ
    tmp = []
    for e in reader:
        if(e[0] == "index"):
            continue
        # 文字が一致する,且つ,未使用
        if(int(e[0]) == ind):
            tmp.append([e[0],e[1],"used"])
        else:
            tmp.append(e)
            
    with open(table, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(tmp)

# 各テーブル中の対応する文字のリフレッシュを行う
def refresh_tableFromChar(chr : str):
    pathToTables = []
    for p in os.listdir(os.path.join(__file__, "..", "ETL")):
        if(os.path.splitext(p)[1] == ".csv"):
            pathToTables.append(os.path.join(__file__, "..", "ETL", p))
    # リフレッシュ対象のテーブルのみを選定する
    tmp = []
    for table in pathToTables:
        reader = csv.reader(open(table, encoding="utf-8"))
        reader = [row for row in reader]
        for e in reader:
            if(e[1] == chr):
                tmp.append(table)

    pathToTables = tmp

    # リフレッシュ対象のテーブルが全てusedかどうか調べる
    isRefresh = True
    for table in pathToTables:
        reader = csv.reader(open(table, encoding="utf-8"))
        reader = [row for row in reader]
        for e in reader:
            # 対象の要素
            if(e[1] == chr):
                # 対象の要素にokがあったらリフレッシュしない
                if(e[2] == "ok"):
                    isRefresh = False
    
    # リフレッシュしないならリターン
    if(not isRefresh):
        return False

    # リフレッシュ対象なら、対象文字の全ての要素をokに書き換える
    isRefresh = True
    for table in pathToTables:
        reader = csv.reader(open(table, encoding="utf-8"))
        reader = [row for row in reader]
        tmp = []
        for e in reader:
            # 対象の要素
            if(e[1] == chr):
                tmp.append([e[0], e[1], "ok"])
                continue
            tmp.append(e)
            
        # 書き換える
        with open(table, mode="w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(tmp)
        
    
    print("文字\""+chr+"\"に対するリフレッシュを行いました")
    return True
        
pointOfLastTable = {}

# 文字から画像を返す
def getImageFromChar(c:str, ind_log:int):
    # etl表から可能なETLファイルとインデックスを探す
    root = os.path.join(__file__, "..", "ETL")
    # ETLの表一覧を取得する
    listOfTable = []
    for l in os.listdir(root):
        if(os.path.splitext(l)[1] == ".csv"):
            l = os.path.join(__file__, "..", "ETL", l)
            listOfTable.append(l)

    # ETL表を全てたどり、対応するETLとインデックスを探す
    ETL_table = ""
    ETL_index = -1
    # もし、対象の文字が以前探索したら、pointOfLastTableの表から始める
    lastTable = False
    if(str(c) in pointOfLastTable):
        lastTable = pointOfLastTable[str(c)]

    isStartFind = False
    isRefresh = False
    for l in listOfTable:
        #print(l)
        if(not lastTable):
            isStartFind = True
        elif(l == lastTable):
            isStartFind = True

        if(not isStartFind):
            continue

        ind = searchIND_oneTABEL(c,l)
        
        # statusを返さないので、成功
        if(ind != "none" and ind != "exit"):
            ETL_table = l
            ETL_index = ind
            pointOfLastTable[str(c)] = l
            break
        
        # 見つからないので、次の表
        if(ind == "none"):
            continue

        # 見つかったが、未使用が無かった、表をリフレッシュする
        if(ind == "exit"):
            isRefresh = refresh_tableFromChar(c)
            continue        

    # リフレッシュされた場合の後処理
    if(isRefresh):
        for l in listOfTable:
            if(not lastTable):
                isStartFind = True
            elif(l == lastTable):
                isStartFind = True
            if(not isStartFind):
                continue

            ind = searchIND_oneTABEL(c,l)
            # statusを返さないので、成功
            if(ind != "none" and ind != "exit"):
                ETL_table = l
                ETL_index = ind
                pointOfLastTable[str(c)] = l
                break
        
        pointOfLastTable.pop(str(c))

    if(ETL_index == -1):
        print("文字"+c+"に対応する画像は見つけられませんでした。")
        # ind_logと、見つけられなかった文字を記録する
        with open("log.txt", mode="a", encoding="utf-8") as f:
            f.write('文字"'+c+'"に対応する画像は見つけられませんでした。('+str(ind_log)+')\n')
        return False

    # 表を更新する
    update_oneTABLE(ETL_index, ETL_table)
    ETL_file = ETL_table.replace("_table.csv", "")
    return get_img(ETL_file, ETL_index)

#print(searchIND_oneTABEL("レ", os.path.join("ETL", "ETL6C_05_table.csv")))
#get_img(os.path.join("ETL", "ETL6C_01"), 1)
"""
img = getImageFromChar("ガ")
if(img != False):
    img.show()


get_img("ETL6\ETL6C_05", 9591).show()
getImageFromChar("ｐ", 0).show()
"""