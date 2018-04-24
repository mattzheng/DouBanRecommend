

import turicreate
import os, time, random
import shutil
import cv2
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import numpy as np
from tqdm import tqdm
from glob import glob
import json
import time
import pandas as pd
from multiprocessing import Pool 


def traverseDirByGlob(path):
    path = os.path.expanduser(path)
    list={}
    i=0
    for f in glob(path + '/*'):
        list[i]=f.strip()
        i=i+1
    return list

# ------ 基于item的推荐 ------ 
def similar_item_data(similar_item,top = 10):
    data_finally = pd.DataFrame()
    for item in similar_item:
        data_tmp = book_excel_all[book_excel_all.type==item].sort_values(by=['scores'],ascending = False)[:top]
        data_finally = pd.concat([data_finally,data_tmp])
        data_finally.reset_index(inplace=True,drop=True)
    return data_finally.drop_duplicates(['book_name'])   

def item_recomend(search_word,book_excel_all,recomend_item,topn = 5):
    book_data = book_excel_all.drop_duplicates(['book_name'])
    recomend_data=book_data[book_data.book_name==search_word]
    similar_item = list(recomend_item.similar[recomend_item.item_id == list(recomend_data.type)[0]])
    #print(similar_item)
    return similar_item_data(similar_item,top=topn)

# ------ 基于item的推荐 ------ 
def search(search_word,book_excel_all):
    '''
    搜索逻辑：
    先完全匹配；匹配不到，局部匹配，包含
    '''
    book_data = book_excel_all.drop_duplicates(['book_name'])
    search_content = book_data[book_data.book_name==search_word]
    if len(search_content.values)>0:
        pass
    else:
        search_content = book_data[[search_word in word for word in book_data.book_name]].sort_values(by=['scores'],ascending = False)
    
    if len(search_content.values)==0:
        search_content = 'No this book!'
    return search_content


if  __name__ == '__main__':
    recomend_item = pd.read_csv('item_data_item.csv')
    book_excel_all = pd.read_csv('book_excel.csv')
    search_word = '深入理解计算机系统（原书第2版）'
    print(item_recomend(search_word,book_excel_all,recomend_item,topn = 10))
    search_word = '书籍'
    print(search(search_word,book_excel_all))