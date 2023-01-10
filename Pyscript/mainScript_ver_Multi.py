from Crawling import Crawling_Service
from Preprocessing import product_pre
from DBcontrol import projectDAO
from multiprocessing import Pool
import sys, requests, json, os

"""
    Multiprocessing 사용하는 버전
    한번에 4개의 창을 동시에 제어...
    tqdm이랑 print 수정해서 콘솔창만 이쁘게 만들면 됨
"""

def mainWork(argsLi : list):
    startPage, endPage, categorys = argsLi[0], argsLi[1], argsLi[2]

    # Folder 생성 
    if not os.path.exists(os.path.join(r'C:\Final_Project_Files', categorys)):
        os.mkdir(os.path.join(r'C:\Final_Project_Files', categorys))
    
    crawlingApp = Crawling_Service.Crawling_process()

    # 크롤링 (카테코리명, 네이버 크롤링 시작페이지, 네이버 크롤링 끝페이지, 에누리 탐색 여부)            
    crawlingApp.ALL_Crawling_process(categorys, startPage, endPage, True)
    
    # 전성분 전처리
    product_pre.Final_Preprocessing(categorys)
    
    # 최종 파일 생성
    product_pre.make_Final_productData(categorys)
    
    # 최종 파일 DB insert
    # projectDAO.Insert_product(cat)

    # Slack Message
    requests.post('https://hooks.slack.com/services/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',
                    headers={"Content-type" : "application/json"},
                    data=json.dumps({"text": f"{categorys} Prodcut Crawling Done!!"}), 
                    verify=False)

if __name__ == "__main__":
    startPage, endPage = list(map(int, sys.argv[1:]))
    categorys = ["Skin", "Cream", "Lotion", "Essence", "BodyLotion", "BodyCream"]
    argsLi = [[startPage, endPage, cat] for cat in categorys]
    
    pool = Pool(processes=4)
    pool.map(mainWork, argsLi)
    pool.close()
    pool.join()
    
    # 성분 관련 제품 update
    # projectDAO.Update_ingredientProduct()

    print("Product Crawling Done!!")
    sys.exit()