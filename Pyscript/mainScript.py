from Crawling import Crawling_Service
from Preprocessing import product_pre
from DBcontrol import projectDAO
from multiprocessing import Process
import sys, requests, json, os
    

if __name__ == "__main__":
    
    startPage, endPage = list(map(int, sys.argv[1:]))
    categorys = ["Skin", "Cream", "Lotion", "Essence", "BodyLotion", "BodyCream"]
    
    for cat in categorys:
        
        # Folder 생성 
        if not os.path.exists(os.path.join(r'C:\Final_Project_Files', cat)):
            os.mkdir(os.path.join(r'C:\Final_Project_Files', cat))
        
        crawlingApp = Crawling_Service.Crawling_process()
        
        # 크롤링 (카테코리명, 네이버 크롤링 시작페이지, 네이버 크롤링 끝페이지, 에누리 탐색 여부)            
        crawlingApp.ALL_Crawling_process(cat, startPage, endPage, True)
        
        # 전성분 전처리
        product_pre.Final_Preprocessing(cat)
        
        # 최종 파일 생성
        product_pre.make_Final_productData(cat)
        
        # 최종 파일 DB insert
        # projectDAO.Insert_product(cat)
    
        # Slack Message
        requests.post('https://hooks.slack.com/services/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',
                      headers={"Content-type" : "application/json"},
                      data=json.dumps({"text": f"{cat} Prodcut Crawling Done!!"}), 
                      verify=False)
    
    # 성분 관련 제품 update
    projectDAO.Update_ingredientProduct()

    print("Product Crawling Done!!")
    sys.exit()
    
    # 성분 확인
    # product_pre.Final_Check_preprocessing(category)
