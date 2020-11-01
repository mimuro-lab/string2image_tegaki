import os
from extract import getImageFromChar
from PIL import Image
import csv

def readString() -> list:
    fp = open("strings.txt", encoding="utf-8")
    retList = []
    for l in fp.readlines():
        retList.append(l.replace("\n", ""))
    return retList

def concat_v(img:list):
    height = 0
    width = 0
    widht_all = 0
    for i in img:
        if(not i):
            continue
        w,h = i.size
        widht_all += w
        if(height < i.height):
            height = i.height
        if(width < i.width):
            width = width + i.width
            
    canpus = Image.new("RGB", (widht_all, height), (255,255,255))
    
    init_x = 0
    for i in range(0, len(img)):
        if(not img[i]):
            continue
        w,h = img[i].size
        canpus.paste(img[i], (init_x, 0))
        init_x += w
        
    return canpus

def add_margin(pil_img, top, right, bottom, left, color):
    width, height = pil_img.size
    new_width = width + right + left
    new_height = height + top + bottom
    result = Image.new("RGB", (new_width, new_height), color)
    result.paste(pil_img, (left, top))
    return result

def editDakuten(img):
    w, h = img.size
    trimUp = int(h/5)
    trimDown = int(h/2)
    trimRight = int(w/5)
    trimLeft = 0
    img = img.crop((trimLeft, trimUp, w - trimRight, h - trimDown))
    
    #img = add_margin(img, 0, 0, trimLeft + trimRight, trimDown + trimUp, (255,255,255))
    img = add_margin(img, 0, 0, trimDown + trimUp, trimLeft + trimRight, (255,255,255))
    #img.show()
    return img

def editSmall(img):
    w, h = img.size
    sml_w = int(w/2)
    sml_h = int(h/2)
    result = Image.new("RGB", (sml_w, h), (255,255,255))
    image = img.resize((sml_w, sml_h))
    result.paste(image, (0, sml_h))
    return result

startIND = 0

def main():
    strings = readString()
    rootDir = os.path.join(__file__, "..", "result")
    lineIND = 0
    # 全ての文字列をたどる
    for s in strings:
        if(lineIND < startIND):
            lineIND += 1
            continue
        imgList = []
        # 一文字ずつたどる
        for c in s:
            print(c, end="")
            if(c == "ー"):
                c = "－"
            # 合成文字かも？（カ＋”）
            reader = csv.reader(open("special_ten.csv",mode="r",encoding="utf-8_sig"))
            reader = [row for row in reader]

            isTen = False
            for e in reader:
                # 合成文字に該当するようだったら
                if(e[0] == c):
                    isTen = True
                    print(" 合成文字と判断しました。（"+c+"）")
                    img1 = getImageFromChar(e[1], lineIND)#元の文字、少し小さくする
                    w, h = img1.size
                    img1 = img1.resize((w-10, h-10))
                    img1 = add_margin(img1, 20, 20, 0, 0, (255,255,255))
                    img2 = getImageFromChar(e[2], lineIND)#濁点or半濁点
                    img2 = editDakuten(img2)
                    mask = Image.new("L", img1.size, 128)
                    img = Image.composite(img1, img2, mask)
                    imgList.append(img)
                    break

            # 小さい文字かも？
            reader = csv.reader(open("special_small.csv",mode="r",encoding="utf-8_sig"))
            reader = [row for row in reader]

            isSmall = False
            for e in reader:
                # 合成文字に該当するようだったら
                if(e[0] == c):
                    isSmall = True
                    print(" 小さい文字と判断しました。（"+e[1]+"）")
                    img = getImageFromChar(e[1], lineIND)
                    img = editSmall(img)
                    imgList.append(img)
                    break

            if(isSmall or isTen):
                continue
            img = getImageFromChar(c, lineIND)
            imgList.append(img)
            print(" 見つかりました")
        
        # Falseの要素は消す
        """
        tmp = []
        for img in imgList:
            if(not img):
                continue
            tmp.append(img)
        imgList = tmp
        """
        savePath = os.path.join(rootDir, str(lineIND)+"_"+s+".png")
        # 画像を結合する
        concat_v(imgList).save(savePath)
        lineIND += 1
        
        print('画像"'+s+'"を作成しました。')

main()