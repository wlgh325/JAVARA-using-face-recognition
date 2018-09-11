# -*- coding:utf-8 -*-
# http://yoonpunk.tistory.com/4 *naver news crwaling

import requests
from bs4 import BeautifulSoup as bs
from itertools import count 

# 출력 파일 명
VODKA_NAME_DB = 'VODKA_NAME_DB.txt'

###
url = "https://drizly.com/vodka/c89"

def main():    
    #file open
    open_output_file = open(VODKA_NAME_DB, 'w',encoding='UTF-8')
    
    idx = 1 #vodka number
    #76page is last page
    for page_num in range(1,76):
        temp_url = url + "/page" + str(page_num)
        r = requests.get(temp_url)
        html = r.text
        soup = bs(html, 'html.parser')
            
        vodka_name = soup.select('.CatalogItem__CatalogItemName___3UVrJ')    #'.'은 해당 클래스가 포함된 모든 태그 출력
        
        for vodka in(vodka_name):
            open_output_file.write(str(idx) + ' ') 
            open_output_file.write(vodka.text + '\n')  #vodka names
            idx+=1
    #file close
    open_output_file.close()
    
if __name__ == '__main__':
    main()
    print ("finish")