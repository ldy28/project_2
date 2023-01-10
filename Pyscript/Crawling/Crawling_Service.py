from Crawling import Crawling_Beauty
import os

class Crawling_process:
    def __init__(self):
        self.__app = Crawling_Beauty.Beauty_CrawlingApp()
        self.categoryDict = {
            "Skin" : [100000928, 50000437],
            "Cream" : [100000931, 50000440],
            "Lotion" : [100000929, 50000438],
            "Essence" : [100000930, 50000439],
            "BodyLotion" : [100001008, 50000408],
            "BodyCream" : [100000992, 50000281]
        }
        
    def __Naver_Crawling_process(self, category, urlcategory, startpage, endpage):
        category_path = os.path.join(self.__app.Final_folder, category)
        
        if not os.path.exists(category_path):
            os.mkdir(category_path)
         
        for page in range(startpage, endpage+1):  
            print("CurPage is", page)
            url = f"https://search.shopping.naver.com/search/category/{urlcategory[0]}?catId={urlcategory[1]}&frm=NVSHMDL&origQuery&pagingIndex={page}&pagingSize=40&productSet=model&query&sort=review_rel&timestamp=&viewType=list"
            self.__app.Naver_Cosmetic_product(url, category)
    
    def __Enuri_Crawling_process(self, category, flag):
        self.__app.Euri_Cosmetic_product(category, flag)
        
    def __GlowPick_Crawling_process(self, category):
        self.__app.glowpick_Cosmetic_product(category)

    def ALL_Crawling_process(self, category, starpage, endpage, EnuriFlag = True):
        destCategory = self.categoryDict[category]
        self.__Naver_Crawling_process(category, destCategory, starpage, endpage)
        self.__Enuri_Crawling_process(category, EnuriFlag)
        self.__GlowPick_Crawling_process(category)
        
    def week_Crawling_process(self, category):
        return self.__app.Naver_Best_Cosmetic(category)
        
if __name__ == "__main__":
    cpApp = Crawling_process()
    
    cpApp.ALL_Crawling_process("Skin", 1, 1, True)