from selenium import webdriver as wb
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from urllib.request import urlretrieve
from urllib.parse import urlparse
from difflib import SequenceMatcher
from datetime import datetime
from tqdm import tqdm
from string import digits, punctuation
import json
import time
import os
import re

class Beauty_CrawlingApp:
    def __init__(self) :
        self.options = wb.ChromeOptions()
        self.options.add_argument("--start-maximized")
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        self.options.add_experimental_option('useAutomationExtension', False)
        self.service = Service(ChromeDriverManager(path='Driver').install())
        self.Final_folder = r'C:\Final_Project_Files'
        self.productFolder = os.path.join(self.Final_folder, 'dataes', 'Cosmetic')
        self.tempDataFolder = os.path.join(self.productFolder, 'tempData')
        self.FinalDataFolder = os.path.join(self.productFolder, 'Final')
        self.categoryDict = {"Skin" : 50000437, "Cream" : 50000440, "Lotion" : 50000438}
        self.productFolderLi = []
    
    def Beauty_Ingredient_Crawling(self):
        """
            대한화장품협회 성분사전 크롤링
        """
        
        url = "https://kcia.or.kr/cid/search/ingd_list.php"
        destLi = []
        
        browser = wb.Chrome(service=self.service, options=self.options)
        browser.get(url)
        time.sleep(1)
        
        last_page = int(browser.find_element(By.XPATH, '//*[@id="content"]/div/div[3]/div/div/div[5]/div/a[12]').get_attribute("href").strip()[-4:])
        last_cnt = int(browser.find_element(By.XPATH, '//*[@id="content"]/div/div[3]/div/div/div[4]/p/b').text.strip().replace(',', ''))%10
   
        self.Cosmetic_ingredient(destLi, browser, 11)
        
        for page in tqdm(range(2, last_page+1)):
            self.Cosmetic_ingredient(destLi, browser, 11)
            browser.find_element(By.XPATH, f'//a[@href="?page={page}"]').click()
            time.sleep(1)
        
        self.Cosmetic_ingredient(destLi, browser, last_cnt + 1)
            
        browser.close()
        browser.quit()
        
        self.toJson("Beauty_Ingredient.json", destLi)

    def Cosmetic_ingredient(self, destLi, browser, last):
        for i in range(1, last):
            browser.find_element(By.XPATH, f'//*[@id="content"]/div/div[3]/div/div/table/tbody/tr[{i}]/td[2]/a').click()
            time.sleep(0.5)
                
            IngreCode = browser.find_element(By.XPATH, '//*[@id="content"]/div/div[3]/div/div/table/tbody/tr[1]/td/p').text.strip()
            IngreName = browser.find_element(By.XPATH, '//*[@id="content"]/div/div[3]/div/div/table[1]/tbody/tr[2]/td[1]/p/b').text.strip().split("\n")
            IngreOldName = browser.find_element(By.XPATH, '//*[@id="content"]/div/div[3]/div/div/table/tbody/tr[2]/td[2]').text.strip().split("\n")
            IngreEngName = self.my_findElement(browser, '영문명')
            IngreObj = self.my_findElement(browser, "배합목적")
            IngreProduct = self.my_findElement(browser, "상품명")
                
            destLi.append({"IngreCode" : IngreCode, "IngreName" : IngreName, "IngreOldName" : IngreOldName, "IngreEngName" : IngreEngName, "IngreObj" : IngreObj, "IngreProduct" : IngreProduct})
            browser.back()
                
            time.sleep(0.5)
        
    def my_findElement(self, browser, parser):
        try:
            # 특정 텍스트가 포함된 요소를 선택하고 거기에 형제 요소를 선택
            selected = browser.find_element(By.XPATH, f'//th[contains(text(), "{parser}")]/following-sibling::td')
            return selected.text.strip().split("\n")
        except:
            return ""
        
    def Beauty_Ingredient_Crawling_Final(self):
        url = "https://kcia.or.kr/cid/search/ingd_list.php?page=1"
        namesLi = []
        
        browser = wb.Chrome(service=self.service, options=self.options)
        browser.get(url)
        browser.implicitly_wait(5)
        time.sleep(1)
        
        ingreCnt = int(browser.find_element(By.XPATH, '//*[@id="content"]/div/div[3]/div/div/div[4]/p/b').text.strip().replace(",", ""))
        pageCnt = ingreCnt//10 if ingreCnt%10 == 0 else ingreCnt//10 + 1
        flag = True if ingreCnt%10 == 0 else False
        
        self.temp_Crawling(namesLi, browser, 11)
        
        for page in range(2, pageCnt+1):
            if not flag:
                lastcnt = 11 if page != pageCnt else ingreCnt%10 + 1 
            else:
                lastcnt = 11
            browser.find_element(By.XPATH, f'//a[@href="?page={page}"]').click()
            time.sleep(0.5)
            self.temp_Crawling(namesLi, browser, lastcnt)
        
        self.toJson(os.path.join(r'C:\Final_Project_Files', 'Final_Ingredient_Dictionary_31.json'), namesLi)
        
        browser.close()
        browser.quit()

    def temp_Crawling(self, namesLi, browser, lastCnt):
        for tr in range(1, lastCnt):
            ingreCode = browser.find_element(By.XPATH, f'//*[@id="content"]/div/div[3]/div/div/table/tbody/tr[{tr}]/td[1]/p').text.strip()
            ingreName = browser.find_element(By.XPATH, f'//*[@id="content"]/div/div[3]/div/div/table/tbody/tr[{tr}]/td[2]/a/p/b').text.strip()
            ingreEngName = browser.find_element(By.XPATH, f'//*[@id="content"]/div/div[3]/div/div/table/tbody/tr[{tr}]/td[3]/a/p').text.strip()
            ingreCas = browser.find_element(By.XPATH, f'//*[@id="content"]/div/div[3]/div/div/table/tbody/tr[{tr}]/td[4]/p').text.strip()
            ingreOldName = browser.find_element(By.XPATH, f'//*[@id="content"]/div/div[3]/div/div/table/tbody/tr[{tr}]/td[5]/p').text.strip()
            
            browser.find_element(By.XPATH, f'//*[@id="content"]/div/div[3]/div/div/table/tbody/tr[{tr}]/td[2]/a').click()
            IngreObj = sum([[j.strip() for j in i.split(",")] for i in self.my_findElement(browser, "배합목적")], [])
            
            namesLi.append({"ingreCode" : ingreCode, "ingreName" : ingreName, "ingreEngName" : ingreEngName, "ingreCas" : ingreCas, "ingreOldName" : ingreOldName, "IngreObj" : IngreObj})
            browser.back()
            
    def coos_crawling(self, IngreNameLi):
        url = "https://coos.kr/"
        destData = {}
        
        browser = wb.Chrome(service=self.service, options=self.options)
        browser.get(url)
        time.sleep(1)
 
        # Login       
        browser.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[1]/div[1]/div/div/div[2]/div[4]/div').click()
        time.sleep(0.5)
        
        email = browser.find_element(By.XPATH, '//*[@id="__next"]/div/div/main/div/div/div/form/div[1]/input')
        password = browser.find_element(By.XPATH, '//*[@id="__next"]/div/div/main/div/div/div/form/div[2]/input')
        login = browser.find_element(By.XPATH, '//*[@id="__next"]/div/div/main/div/div/div/form/div[4]/button')
        
        ActionChains(browser).click(email).send_keys("evil8676@naver.com").click(password).send_keys("q1w2e3r4!!").click(login).perform()
        time.sleep(1)
        
        # Search
        inputArea = browser.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div[1]/input')
        
        for key in tqdm(IngreNameLi):
            ActionChains(browser).click(inputArea).send_keys(key).pause(1).send_keys(Keys.ARROW_DOWN).pause(1).send_keys(Keys.ENTER).perform()
            time.sleep(2)
            
            try:
                checkName = browser.find_element(By.XPATH, '//*[@id="__next"]/div/div/main/div/div/div/div[1]/div[1]/table/tbody/tr[2]/td[2]') # flag
                
                if checkName.text.strip() == key:     
                    try:
                        ewgScore = browser.find_element(By.XPATH, '//*[@id="__next"]/div/div/main/div/div/div/div[1]/div[2]/table[1]/tbody/tr[1]/td[2]').text.strip().replace("\n", " ").split(" ")[1]
                        ewgGrade = browser.find_element(By.XPATH, '//*[@id="__next"]/div/div/main/div/div/div/div[1]/div[2]/table[1]/tbody/tr[2]/td[2]/div/p').text.strip()
                    except:
                        ewgScore = "등급없음"
                        ewgGrade = "등급없음"
                        
                    # For Product Variable
                    productLi = []
                    # materialCnt = int(browser.find_element(By.XPATH, '//*[@id="__next"]/div/div/main/div/div/div/div[2]/h4').text.strip().split(" ")[-1][1:-1])
                    
                    # if materialCnt != 0:    
                    #     nextCnt = materialCnt // 25
                    #     lastCnt = materialCnt % 25
                    #     markLi = ["NMPA", "COSMOS", "VEGAN", "REACH", "USDA", "ECOCERT", "특허/논문"]
                        
                    #     if nextCnt > 0:
                    #         for page in range(nextCnt+1):
                    #             cnt = lastCnt if page == nextCnt else 25
                    #             self.coos_product(browser, productLi, cnt, markLi)
                                
                    #             if page != nextCnt:
                    #                 browser.find_element(By.XPATH, '//*[@id="__next"]/div/div/main/div/div/div/div[2]/div/div/div[6]/div/div[3]/button[2]').click()
                    #                 time.sleep(0.3)
                    #     else:
                    #         self.coos_product(browser, productLi, lastCnt, markLi) 
                    
                    destData[key] = {"ewgScore" : ewgScore, "ewgGrade" : ewgGrade, "Products" : productLi}
                    browser.back()
                    time.sleep(0.75)
                else:
                    destData[key] = {}
                    browser.back()
                    time.sleep(0.75)    
            except:
                destData[key] = {}
                ActionChains(browser).double_click(inputArea).click(inputArea).send_keys(Keys.DELETE).perform()
                time.sleep(0.1)
        
        self.toJson("test1.json", destData)
        
        browser.close()
        browser.quit()

    def coos_product(self, browser, productLi, lastCnt, markLi):
        for idx in range(lastCnt):
            rowidx = idx*2 + 1
                    
            # Hover Click
            browser.find_element(By.XPATH, f'//*[@id="__next"]/div/div/main/div/div/div/div[2]/div/div/div[5]/table/tbody/tr[{rowidx}]/td[2]/button').click()
            time.sleep(0.1)
                    
            # product Name & ProductMark
            ProductName = browser.find_element(By.XPATH, f'//*[@id="enhanced-table-checkbox-{idx}"]').text.strip().split("\n")
                    
            ProductMark = []
            for v in ProductName[:]:
                if v in markLi:
                    ProductMark.append(v)
                    ProductName.remove(v)
                    
            ProductKind = browser.find_element(By.XPATH, f'//*[@id="__next"]/div/div/main/div/div/div/div[2]/div/div/div[5]/table/tbody/tr[{rowidx}]/td[3]').text.strip()
            ProductFunction = browser.find_element(By.XPATH, f'//*[@id="__next"]/div/div/main/div/div/div/div[2]/div/div/div[5]/table/tbody/tr[{rowidx}]/td[4]').text.strip()
            ProductManuFactor = browser.find_element(By.XPATH, f'//*[@id="__next"]/div/div/main/div/div/div/div[2]/div/div/div[5]/table/tbody/tr[{rowidx}]/td[5]').text.strip()
            
            ProductSupply = browser.find_element(By.XPATH, f'//*[@id="__next"]/div/div/main/div/div/div/div[2]/div/div/div[5]/table/tbody/tr[{rowidx}]/td[6]').text.strip().split("\n")
            if len(ProductSupply) > 1:
                ProductSupply = ProductSupply[:-1] if ProductSupply[-1][-4:].isnumeric() else ProductSupply # delete Phone number
                ProductSupply = [i for i in ProductSupply if i not in ['Sponsor', 'Premium Sponsor']] # delete Sponser

            Row_inner = browser.find_element(By.XPATH, f'//*[@id="__next"]/div/div/main/div/div/div/div[2]/div/div/div[5]/table/tbody/tr[{rowidx+1}]').text.strip().split("\n")
            if Row_inner.count("특징") != 0:
                character = Row_inner.index("특징")
                ProductINCI = Row_inner[1:character]
                ProductCharacter = [i[2:] for i in Row_inner[character+1:]]
            else:
                ProductINCI = Row_inner[1:]
                ProductCharacter = []
                    
            productLi.append({"ProductName" : ProductName[0], "ProductMark" : ProductMark, "ProductKind" : ProductKind, "ProductFunction" : ProductFunction,
                              "ProductManuFactor" : ProductManuFactor, "ProductSupply" : ProductSupply[0], "ProductINCI" : ProductINCI, "ProductCharacter" : ProductCharacter})
            
    def Naver_Cosmetic_product(self, categoryUrl, category):
        url = categoryUrl
        browser = wb.Chrome(service=self.service, options=self.options)
        browser.get(url)
        browser.implicitly_wait(10)
        browser.delete_all_cookies()
        
        for idx in range(1, 41):
            productTD = browser.find_element(By.XPATH, f'//*[@id="__next"]/div/div[2]/div/div[3]/div[1]/ul/div/div[{idx}]/li')
            
            # 해당인덱스의 상품으로 스크롤 이동
            ActionChains(browser).move_to_element(productTD).perform()
            time.sleep(0.3)
            
            productName = browser.find_element(By.XPATH, f'//*[@id="__next"]/div/div[2]/div/div[3]/div[1]/ul/div/div[{idx}]/li/div[1]/div[2]/div[1]').text.strip()
            folderName = productName.translate(str.maketrans('', '', punctuation))
            
            if not os.path.exists(os.path.join(self.Final_folder, category, folderName, "product.json")):
                
                # productID
                productID = urlparse(browser.find_element(By.XPATH, f'//*[@id="__next"]/div/div[2]/div/div[3]/div[1]/ul/div/div[{idx}]/li/div[1]/div[1]/div/a/img').get_attribute("src")).path.split("/")[-1].split(".")[0]
                                
                # productfolder 생성
                productfolder = self.product_folder(category, productName)
            
                # 제품 상세페이지로 이동 
                browser.find_element(By.XPATH, f'//*[@id="__next"]/div/div[2]/div/div[3]/div[1]/ul/div/div[{idx}]/li/div[1]/div[1]/div/a').click()
                time.sleep(2)
                
                # 새롭게 열린 탭으로 변경
                browser.switch_to.window(browser.window_handles[-1])
                errorCnt = 0
                
                while True:
                    try:
                        InnerData = self.Product_InnerPage(browser, productName, productfolder)
                    except Exception as e:
                        print(e)
                        errorCnt += 1
                        browser.refresh()
                        time.sleep(1)
                    else:
                        break
                    
                    if errorCnt > 5:
                        break
                        
                browser.close()
                browser.switch_to.window(browser.window_handles[0])
            
                # 상품별로 따로 json 파일 생성
                tempdata = {
                    productName : {
                        "productID" : productID, 
                        "projectImg" : InnerData['productImg'], 
                        'productCharacter' : InnerData['productCharacter'], 
                        'productStar' : InnerData['productStar'],
                        "productMaker" : InnerData['productMaker'], 
                        "productBrand" : InnerData['productBrand'], 
                        "productDate" : InnerData['productDate'], 
                        "productReviewCnt" : InnerData['productReviewCnt'], 
                        "allIngredient" : InnerData['allIngredient'], 
                        "analysisIngre" : InnerData['analysisIngre'], 
                        "productStarRatio" : InnerData['productStarRatio'],
                        "productAIReview" : InnerData['productAIReview'], 
                        "productAgeLikes" : InnerData['productAgeLikes'], 
                        "productSexLikes" : InnerData['productSexLikes']
                        }
                    }
                
                self.toJson(os.path.join(productfolder, "product.json"), tempdata)
                self.productFolderLi.append(os.path.split(productfolder)[-1])
                                
                print(idx, productName)
                
            # 맨 아래까지 스크롤 다운
            self.Scroll_bottom(browser)
        
        browser.close()
        browser.quit()

    def Product_InnerPage(self, browser, productName, productfolder):
        
        # productImg
        imgEle = WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div/div[2]/div[2]/div[2]/div[1]/div/div[1]/div/div/img')))
        
        productImg = imgEle.get_attribute("src").strip()
        
        productStar = float(browser.find_element(By.XPATH, '//*[@id="__next"]/div/div[2]/div[2]/div[1]/div[1]').text.strip().replace("평점", ""))
                
        topinfo = browser.find_elements(By.CSS_SELECTOR, 'span.top_cell__5KJK9 > em')
        productTopinfo = [i.text.strip() for i in topinfo]
        
        # productMaker, productBrand, productDate
        if len(productTopinfo) == 3:
            productMaker = productTopinfo[0]
            productBrand = productTopinfo[1]
            productDate = productTopinfo[2][:-1]
        elif len(productTopinfo) == 2:
            productMaker = "None"
            productBrand = productTopinfo[0]
            productDate = productTopinfo[1][:-1]   
        else:
            productMaker = "None"
            productBrand = "None"
            productDate = productTopinfo[0][:-1]
        
        innerinfo = browser.find_elements(By.CSS_SELECTOR, 'div.top_info_inner__aM_0Z + div > span')
        productCharacters = sum([[cs.strip() for cs in word.split(":")[1].split(",")] for word in [info.text.strip() for info in innerinfo] if re.match('주요제품특징|세부제품특징|피부타입', word) != None and word], [])
        
        # productCharacter
        if productCharacters:
            productCharacter = "|".join([re.sub('\([ㄱ-ㅎㅏ-ㅣ가-힣]+\)', '', i).strip() if re.search('\([ㄱ-ㅎㅏ-ㅣ가-힣]+\)', i.strip()) else i.strip() for i in productCharacters])
        else:
            productCharacter = "None"
            
        tabStrongele = browser.find_elements(By.CSS_SELECTOR, 'div.floatingTab_detail_tab__akl87 > ul > li > a > strong')
        tablen = len(tabStrongele)//2
        
        ingresEle, productinfo, shoppingReview = "", "", ""
        
        # 성분정보, 제품정보, 쇼핑몰 리뷰 tab a tag 찾기
        for idx, strong in enumerate(tabStrongele[:tablen]):
            eleText = strong.text.strip("1234567890,")
            if eleText == '성분정보':
                ingresEle = f'//*[@id="snb"]/ul/li[{idx+1}]/a'
            elif eleText == '제품정보':
                productinfo = f'//*[@id="snb"]/ul/li[{idx+1}]/a'
            elif eleText == '쇼핑몰리뷰':
                shoppingReview = f'//*[@id="snb"]/ul/li[{idx+1}]/a'
                
        if ingresEle:
            ingreTab = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, ingresEle)))
            ingreTab.send_keys(Keys.ENTER) # 성분정보 더보기 클릭
            time.sleep(0.05)
            
            try:
                ingres = browser.find_element(By.XPATH, '//*[@id="section_ingredient"]/div[5]/p').text.strip().split(',') # 전성분
                allIngredient = [i.strip() for i in ingres]
            except:
                allIngredient = []
            
            try:
                analysised = browser.find_elements(By.CSS_SELECTOR, 'ul.analysisIngredient_ingredient_list__YnLPO > li > div > div.analysisIngredient_ingredient_title__ImRzY')
                analysisIngre = [i.text.strip() for i in analysised]
            except:
                analysisIngre = []
        else:
            allIngredient = []
            analysisIngre = []
        
        if productinfo:
            productinfoTab = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, productinfo)))
            productinfoTab.send_keys(Keys.ENTER) # 제품정보 더보기 클릭
            time.sleep(0.05)

            try:
                # 제품 상세 이미지 저장
                productDesImg = browser.find_element(By.XPATH, '//*[@id="section_spec"]/div[2]/div/div/div/p/img').get_attribute('src')
                urlretrieve(productDesImg, os.path.join(productfolder, 'imgs', f"{productName}.png"))
            except:
                pass
        
        # 쇼핑몰리뷰 클릭
        if shoppingReview:
            shoppingReviewTab = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, shoppingReview)))
            shoppingReviewTab.send_keys(Keys.ENTER) 
            time.sleep(0.05)
        
        # productStarRatio
        starRatio = browser.find_elements(By.CSS_SELECTOR, 'span.totalArea_bar__FooPz')
        productStarRatio = "|".join([str(round(float(i.text.strip()[:-1]), 2)) for i in starRatio if i.text.strip()]) if starRatio else "None"
            
        # AI 리뷰
        try:
            browser.find_element(By.CSS_SELECTOR, 'div.bestReview_best_review__MGpEv')
            AIReview = browser.find_element(By.XPATH, '//*[@id="section_review"]/div[1]/div[2]/ul').text.strip().split("\n")[1::2]
            productAIReview = [i.strip() for i in AIReview]
        except:
            productAIReview = []
            
        # 리뷰 개수 저장
        reviewCnt = browser.find_element(By.XPATH, '//*[@id="section_review"]/div[1]/div/div[2]/div/div').text.strip()
        productReviewCnt = int(reviewCnt) if reviewCnt.find(",") == -1 else int(reviewCnt.replace(",", ""))
        
        # 리뷰 저장
        productReviews = []
        lastpage = 11 if productReviewCnt//20 > 10 else productReviewCnt//20 if productReviewCnt%20 == 0 else productReviewCnt//20 + 1
        for rp in range(1, lastpage):
            if rp != 1:
                browser.find_element(By.XPATH, f'//*[@id="section_review"]/div[3]/a[{rp}]').click()
                time.sleep(0.5)
            for i in range(1, 21):
                productReviews.append(browser.find_element(By.XPATH, f'//*[@id="section_review"]/ul/li[{i}]/div[2]/div[1]/p').text.strip())
                time.sleep(0.01)
                
        self.toJson(os.path.join(productfolder, 'Reviews.json'), productReviews) # 일단 json형태로 저장
            
        # productAgeLikes
        try:
            Likes = browser.find_element(By.XPATH, '//*[@id="__next"]/div/div[2]/div[2]/div[2]/div[2]/div[3]/div/div[2]/div[2]/div/ul').text.strip().split("\n")
            productLikes = "|".join([str(i[:-1]).strip() for i in Likes if i.find('%') != -1])
        except:
            productLikes = "None"
        
        # productSexLikes
        try:
            sexLikes = browser.find_element(By.XPATH, '//*[@id="_donut_chart_container"]').text.strip().split("\n")
            productSexLikes = "|".join([str(i[:-1]).strip() for i in sexLikes]) # 여자, 남자 순이라고 쳐야됨
        except:
            productSexLikes = "None"
        
        return {"productImg" : productImg,
                "productStar" : productStar, 
                "productReviewCnt" : productReviewCnt, 
                "productMaker" : productMaker, 
                "productBrand" : productBrand, 
                "productDate" : productDate,
                "productCharacter" : productCharacter, 
                "productStarRatio" : productStarRatio, 
                "allIngredient" : allIngredient,
                "analysisIngre" : analysisIngre,
                "productAIReview" : productAIReview, 
                "productAgeLikes" : productLikes, 
                "productSexLikes" : productSexLikes}
        
    def Scroll_bottom(self, browser):
        # Get scroll height
        last_height = browser.execute_script("return document.body.scrollHeight")
        while True:
            # Scroll down to bottom
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(0.3)

            # Calculate new scroll height and compare with last scroll height
            new_height = browser.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
    
    def Euri_Cosmetic_product(self, category, flag):
        url = "http://www.enuri.com/search.jsp?keyword=first"
        categoryPath = os.path.join(self.Final_folder, category)
        productNamesLi = self.list_chunk(self.productFolderLi, 120)
        
        for productNames in productNamesLi:    
            browser = wb.Chrome(service=self.service, options=self.options)
            browser.get(url)
            browser.delete_all_cookies()
            browser.implicitly_wait(5)
            time.sleep(1)
        
            for name in tqdm(productNames):
                productJsonPath = os.path.join(categoryPath, name, 'product.json')
                
                if os.path.exists(productJsonPath):
                    
                    productData = self.openJson(productJsonPath)
                    productName = list(productData.keys())[0]
                    
                    # 이미 최종 프로세스를 거친 경우
                    if 'Final' in productData[productName].keys():
                        continue
                    
                    # 이미 글로우픽까지 크롤링은 진행한 경우
                    if 'Crawl' in productData[productName].keys():
                        continue
                    
                    if productData[productName]['allIngredient'] and not flag:
                        continue
                    
                    try:
                        inputArea = browser.find_element(By.XPATH, '//*[@id="search_keyword"]')
                        inputArea.clear()
                        ActionChains(browser).click(inputArea).send_keys(self.make_justName(name)).send_keys(Keys.ENTER).perform()
                        time.sleep(0.5)
                    
                        browser.find_element(By.XPATH, '//*[@id="listBodyDiv"]/div[2]/div[1]/div[2]/div[1]/ul/li[2]/a').click()
                        time.sleep(0.3)
                        mainIngre = []
                    
                        if productData[productName]['allIngredient']:
                            if flag:
                                try:
                                    description = browser.find_element(By.XPATH, '//*[@id="listBodyDiv"]/div[2]/div[1]/div[3]/div[1]/ul/li/div/div[2]/div[1]/ul').text.strip().split("|")
                                    mainIngre = sum([i.split(":")[1].split(",") for i in description if i.find('성분') != -1], [])
                                except:
                                    pass
                                    
                                productData[productName]['analysisIngre'] = productData[productName]['analysisIngre'] + mainIngre
                        else:
                            if flag:
                                try:
                                    description = browser.find_element(By.XPATH, '//*[@id="listBodyDiv"]/div[2]/div[1]/div[3]/div[1]/ul/li/div/div[2]/div[1]/ul').text.strip().split("|")
                                    mainIngre = sum([i.split(":")[1].split(",") for i in description if i.find('성분') != -1], [])
                                except:
                                    pass
                            
                            try:
                                browser.find_element(By.XPATH, '//*[@id="listBodyDiv"]/div[2]/div[1]/div[3]/div[1]/ul/li[1]/div/div[2]/div[1]/div[1]/a').click()
                                time.sleep(1)
                                browser.switch_to.window(browser.window_handles[-1])
                                
                                if urlparse(browser.current_url).netloc != 'www.enuri.com':
                                    browser.close()
                                    browser.switch_to.window(browser.window_handles[0])
                                    raise Exception
                                    
                                try:
                                    Ingres = [i.strip() for i in browser.find_element(By.XPATH, '//*[@id="cosComponent"]/div/table/tbody/tr/td[4]/div/p').text.strip().split(",")]
                                except:
                                    Ingres = []
                                
                                browser.close()
                                browser.switch_to.window(browser.window_handles[0])
                            except:
                                Ingres = []
                            
                            productData[productName]['analysisIngre'] = productData[productName]['analysisIngre'] + mainIngre
                            productData[productName]['allIngredient'] = productData[productName]['allIngredient'] + Ingres
                            
                        self.toJson(productJsonPath, productData)
                        
                    except:
                        pass
            
            browser.close()
            browser.quit()
        
        print("Euri Crawling Done!!")
    
    def Euri_Cosmetic_product_temp(self, NaverCosPath, category):
        url = "http://www.enuri.com/search.jsp?keyword=first"
        allData = self.openJson(NaverCosPath)
        
        browser = wb.Chrome(service=self.service, options=self.options)
        browser.get(url)
        browser.delete_all_cookies()
        browser.implicitly_wait(5)
        time.sleep(1)
        
        for name in (allData):
            searchName = self.make_justName(name)
            inputArea = browser.find_element(By.XPATH, '//*[@id="search_keyword"]')
            inputArea.clear()
            ActionChains(browser).click(inputArea).send_keys(searchName).send_keys(Keys.ENTER).perform()
            time.sleep(0.5)
            
            browser.find_element(By.XPATH, '//*[@id="listBodyDiv"]/div[2]/div[1]/div[2]/div[1]/ul/li[2]/a').click()
            time.sleep(0.3)

            try:
                searchedLi = browser.find_elements(By.CSS_SELECTOR, 'div.item__model > a')
                
                if allData[name]['allIngredient']:
                    try:
                        description = browser.find_element(By.XPATH, '//*[@id="listBodyDiv"]/div[2]/div[1]/div[3]/div[1]/ul/li/div/div[2]/div[1]/ul').text.strip().split("|")
                        mainIngre = sum([i.split(":")[1].split(",") for i in description if i.find('성분') != -1], [])
                    except:
                        mainIngre = []
                    
                    allData[name]['analysisIngre'] = allData[name]['analysisIngre'] + mainIngre
                else:
                    try:
                        description = browser.find_element(By.XPATH, '//*[@id="listBodyDiv"]/div[2]/div[1]/div[3]/div[1]/ul/li/div/div[2]/div[1]/ul').text.strip().split("|")
                        mainIngre = sum([i.split(":")[1].split(",") for i in description if i.find('성분') != -1], [])
                    except:
                        mainIngre = []
                    
                    if len(searchedLi) > 1:
                        checkedLi = []
                        for ele in searchedLi:
                            check = ele.text.strip().replace(" ", "")
                            temp = SequenceMatcher(None, searchName.replace(" ", ""), check).ratio()
                            print(temp)
                            if temp >= 0.3:
                                checkedLi.append([ele, temp])
                        
                        if not checkedLi:
                            raise Exception
                        
                        
                        max(checkedLi, key=lambda x: x[1])[0].click()
                        print(max(checkedLi, key=lambda x: x[1])[0].text.strip())
                        time.sleep(1)
                        browser.switch_to.window(browser.window_handles[-1])
                        
                        if urlparse(browser.current_url).netloc != 'www.enuri.com':
                            browser.close()
                            browser.switch_to.window(browser.window_handles[0])
                            raise Exception
                        
                        try:
                            Ingres = [i.strip() for i in browser.find_element(By.XPATH, '//*[@id="cosComponent"]/div/table/tbody/tr/td[4]/div/p').text.strip().split(",")]
                        except:
                            Ingres = []
                            
                        browser.close()
                        browser.switch_to.window(browser.window_handles[0])
                    else:
                        check = searchedLi[0].text.strip().replace(" ", "")
                        temp = SequenceMatcher(None, searchName.replace(" ", ""), check).ratio()
                        if temp < 0.3:
                            raise Exception
                        
                        searchedLi[0].click()
                        time.sleep(1)
                        browser.switch_to.window(browser.window_handles[-1])
                        
                        if urlparse(browser.current_url).netloc != 'www.enuri.com':
                            browser.close()
                            browser.switch_to.window(browser.window_handles[0])
                            raise Exception
                        
                        try:
                            Ingres = [i.strip() for i in browser.find_element(By.XPATH, '//*[@id="cosComponent"]/div/table/tbody/tr/td[4]/div/p').text.strip().split(",")]
                        except:
                            Ingres = []
                            
                        browser.close()
                        browser.switch_to.window(browser.window_handles[0])
                        
                    allData[name]['analysisIngre'] = allData[name]['analysisIngre'] + mainIngre
                    allData[name]['allIngredient'] = allData[name]['allIngredient'] + Ingres
            except:
                pass

        browser.close()
        browser.quit()
        
        destpath = os.path.join(self.product_folder, 'tempData', f'Euri_Cosmetic_{category}.json')
        
        self.toJson(destpath, allData)
        
        return destpath
        
    def glowpick_Cosmetic_product(self, category):
        url = "https://www.glowpick.com/?tab=recommends"
        categoryPath = os.path.join(self.Final_folder, category)
        productNamesLi = self.list_chunk(self.productFolderLi, 80)
        
        for idx, productNames in enumerate(productNamesLi):
            
            browser = wb.Chrome(service=self.service, options=self.options)
            browser.get(url)
            browser.implicitly_wait(5)
            browser.delete_all_cookies()
            time.sleep(1)
        
            browser.find_element(By.CLASS_NAME,'buttons__button').click()
        
            for name in tqdm(productNames):
                
                productJsonPath = os.path.join(categoryPath, name, 'product.json')
                
                if os.path.exists(productJsonPath):
                    
                    productData = self.openJson(productJsonPath)                
                    search_name = self.make_justName(name)
                    productName = list(productData.keys())[0]
                    
                    # 이미 최종 프로세스까지 거친 경우
                    if 'Final' in productData[productName].keys():
                        continue
                    
                    # 이미 글로우픽까지 크롤링은 진행한 경우
                    if 'Crawl' in productData[productName].keys():
                        continue
                    
                    while True:
                        try:
                            menuEle = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'menu-search')))                
                            menuEle.click()
                            time.sleep(2)
                        
                            searchbar = browser.find_element(By.CLASS_NAME, 'header__input')
                            ActionChains(browser).click(searchbar).pause(1).send_keys(search_name).send_keys(Keys.ENTER).perform()
                            time.sleep(2)
                        
                            try:
                                searchLi = browser.find_elements(By.CLASS_NAME, 'font-normal')
                                onlyName = " ".join(search_name.split(" ")[1:]).replace(" ", "")
                                
                                if len(searchLi) > 1:
                                    checkLi = []
                                    for ele in searchLi:
                                        temp = ele.text.strip().replace(" ", "")
                                        check = SequenceMatcher(None, onlyName, temp).ratio()
                                        if check >= 0.6:
                                            checkLi.append([ele, check])
                                    
                                    if checkLi:
                                        max(checkLi, key=lambda x:x[1])[0].click()
                                    else:
                                        raise Exception
                                        
                                    time.sleep(1)
                                    
                                    browser.execute_script("window.scrollTo(0, 350)")
                                    browser.find_element(By.CSS_SELECTOR,'#contents > section > div.product__info.info > article.info__article.ingredient > h2 > button').click()
                                    time.sleep(0.5)
                                    
                                    allingre = browser.find_elements(By.CLASS_NAME,'item__wrapper__text__kor')
                                    productData[productName]['allIngredient'] = [i.text.strip() for i in allingre]
                                    productData[productName]['Crawl'] = "yes"
                                    
                                    browser.back()
                                else:
                                    temp = searchLi[0].text.strip().replace(" ", "")
                                    check = SequenceMatcher(None, onlyName, temp).ratio()
                                    if check >= 0.6:
                                        searchLi[0].click()
                                    else:
                                        raise Exception
                                        
                                    time.sleep(1)
                                    
                                    browser.execute_script("window.scrollTo(0, 350)")
                                    browser.find_element(By.CSS_SELECTOR,'#contents > section > div.product__info.info > article.info__article.ingredient > h2 > button').click()
                                    time.sleep(0.5)
                                    
                                    allingre = browser.find_elements(By.CLASS_NAME,'item__wrapper__text__kor')
                                    productData[productName]['allIngredient'] = [i.text.strip() for i in allingre]
                                    productData[productName]['Crawl'] = "yes"
                                
                                    browser.back()
                                time.sleep(1.5)
                            except:
                                productData[productName]['Crawl'] = "yes"
                        except Exception as e:
                            print(e)
                            browser.refresh()
                            time.sleep(1)
                        else:
                            break
                
                    self.toJson(productJsonPath, productData)
                    
            browser.close()
            browser.quit()
            
        print("GlowPick Crawling Done!!")
    
    def make_Final_Cosmetic(self, glowtempFolder, category):
        
        FinalData = self.openJson(os.path.join(self.productFolder, 'Final', f"Final_Cosmetic_{category}.json"))
        
        for glow in os.listdir(glowtempFolder):
            if glow.endswith(".json"):
                glowJson = os.path.join(glowtempFolder, glow)
                glowData = self.openJson(glowJson)
                for data in glowData:
                    if glowData[data]:
                        FinalData[data]['allIngredient'] = glowData[data]
                os.remove(glowJson)
                
        self.toJson(os.path.join(self.productFolder, 'Final', f"Final_Cosmetic_{category}2.json"), FinalData)
            
    def Naver_Best_Cosmetic(self, category):
        destFolder = os.path.join(r'C:\Final_Project_Files\dataes\Cosmetic\tempData', category)
        
        if not os.path.exists(destFolder):
            os.mkdir(destFolder)
        
        categoryID = self.categoryDict[category]
        
        url = f"https://search.shopping.naver.com/best/category/purchase?categoryCategoryId={categoryID}&categoryChildCategoryId={categoryID}&categoryDemo=A00&categoryMidCategoryId=50000190&categoryRootCategoryId=50000002&chartRank=1&period=P7D"
        
        browser = wb.Chrome(service=self.service, options=self.options)
        browser.get(url)
        browser.implicitly_wait(5)
        time.sleep(1)
            
        self.Scroll_bottom(browser)
        
        productNames = browser.find_elements(By.CSS_SELECTOR, 'div.category_list_wrap__tr_Zy > ul > li')
        NamesLi = [i.get_attribute("id").strip() for i in productNames]
        
        browser.close()
        browser.quit()
        
        txtName = datetime.today().strftime("%Y_%m_%d") + f"_{category}.txt"
        
        self.toTxt(os.path.join(destFolder, txtName), NamesLi)
        
        print(f"Naver Best {category} Done")
        
        return NamesLi
    
    def Naver_Month_Cosmetic(self, category):
        destFolder = os.path.join(r'C:\Final_Project_Files\dataes\Cosmetic\tempData', category)
        
        MonthLi = []
        for files in os.listdir(destFolder):
            if files.endswith(".txt"):
                data = self.openTxt(os.path.join(destFolder, files))
                MonthLi += data
                os.remove(os.path.join(destFolder, files))
                
        return MonthLi
    
    def toJson(self, JsonPath, destData):
        with open(JsonPath, 'w', encoding='utf-8') as f:
            json.dump(destData, f, ensure_ascii=False)
    
    def openJson(self, JsonPath):
        with open(JsonPath, 'r', encoding="utf-8") as f:
            Json_data = json.load(f)
        return Json_data
    
    def toTxt(self, txtPath, destData):
        with open(txtPath, 'w', encoding='utf-8') as f:
            for d in destData:
                f.write(d + "\n")
    
    def openTxt(self, txtPath):
        with open(txtPath, 'r', encoding='utf-8') as f:
            data = f.read().splitlines()
        return [i.strip() for i in data]
    
    def slight_process(self, JsonPath):
        json_data = self.openJson(JsonPath)
        
        for data in json_data:
            data['IngreName'] = data["IngreName"][0]
            if isinstance(data['IngreObj'], list):
                data['IngreObj'] = [i.strip() for i in data['IngreObj'][0].split(",")]
            else:
                data['IngreObj'] = []
                
        self.toJson("Beauty_Ingredient_pre.json", json_data)
        
    def product_folder(self, category, productName):
        folderName = productName.translate(str.maketrans('', '', punctuation))
        projectFolder = os.path.join(self.Final_folder, category, folderName)
        
        if not os.path.exists(projectFolder):
            os.mkdir(projectFolder)
        
        imgFolder = os.path.join(projectFolder, 'imgs')
        if not os.path.exists(imgFolder):
            os.mkdir(imgFolder)
        
        return projectFolder
    
    def make_Final_productData(self, category):
        allCosdata = {}
        tempCheckdata = {}
        category_path = os.path.join(self.Final_folder, category)
        result_path = os.path.join(self.FinalDataFolder, f"Final_{category}.json")
        
        for cos in tqdm(os.listdir(category_path)):
            cospath = os.path.join(category_path, cos, 'product.json')
            if os.path.exists(cospath):    
                jsonData = self.openJson(cospath)
                allCosdata.update(jsonData)
                for data in jsonData:
                    if jsonData[data]['allIngredient']:
                        tempCheckdata[self.make_justName(data)] = jsonData[data]['allIngredient']
        
        for cos in allCosdata:
            if not allCosdata[cos]['allIngredient']:
                temp = self.make_justName(cos)
                if temp in tempCheckdata.keys():
                    allCosdata[cos]['allIngredient'] = tempCheckdata[temp]
        
        self.toJson(result_path, allCosdata)
        print("make_all_Naver_productData Done!!")
        
        return result_path
        
    def make_justName(self, name):
        name_split = name.split(" ")
        DelCapacity = None
        for idx, word in enumerate(name_split):
            if re.search("[0-9]ml|[0-9]매|[0-9]g", word):
                DelCapacity = idx
                break
        return " ".join(name_split[:DelCapacity]) if DelCapacity else name
    
    def list_chunk(self, lst, n):
        return [lst[i:i+n] for i in range(0, len(lst), n)]
        
if __name__ == "__main__":
    app = Beauty_CrawlingApp()
    
    # app.Naver_Best_Cosmetic("Skin")
    
    app.Naver_Month_Cosmetic("Skin")
"""
    수정 사항
    
    - 크롤링에 대한 공부를 더 잘 해보고 싶음!!
    - Crawling 실행할시 오류가 나면 어떻게 대응해야되는지

"""
    