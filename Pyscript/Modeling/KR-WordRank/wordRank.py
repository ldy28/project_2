from krwordrank.word import summarize_with_keywords
from krwordrank.hangle import normalize
from wordcloud import WordCloud
from PIL import Image
from tqdm import tqdm
import numpy as np
import os, shutil, json, re, pymysql

def toJson(JsponPath, destData):
    with open(JsponPath, 'w', encoding='utf-8') as f:
        json.dump(destData, f, ensure_ascii=False)

def openJson(JsonPath):
    with open(JsonPath, 'r', encoding='utf-8') as f:
        JsonData = json.load(f)
    return JsonData

def toTxt(txtPath, destData):
    with open(txtPath, 'w', encoding='utf-8') as f:
        for d in destData:
            f.write(d + "\n")

def openTxt(txtPath):
    with open(txtPath, 'r', encoding='utf-8') as f:
        data = f.read().splitlines()
    return [i.strip() for i in data]

def dbConnection():
    connection = pymysql.connect(host='project-db-stu.ddns.net', port=3307, user='Anjisu', password='12345', db='Anjisu', charset='utf8')
    cursor = connection.cursor()
    return connection, cursor

def dbConnection_dict():
    connection = pymysql.connect(host='project-db-stu.ddns.net', port=3307, user='Anjisu', password='12345', db='Anjisu', charset='utf8')
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    return connection, cursor

def Select_IngreProdcut():
    connection, cursor = dbConnection_dict()
    
    sql = "SELECT ingreCode, ingreName, ingreProduct FROM ingredient i WHERE ingreProduct != ''"
    cursor.execute(sql)
    result = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return result

def Update_ProductKeyword():
    ReviewPath = r'C:\Final_Project_Files\ProductReviews'
    UpdateLi = [("yes", productID) for productID in os.listdir(ReviewPath)]

    connection, cursor = dbConnection()
    
    sql = "UPDATE cosmetic SET productKeyword = %s WHERE productID = %s"
    cursor.executemany(sql, UpdateLi)
    
    connection.commit()
    cursor.close()
    connection.close()
    
    print("Update ProductKeyword Done")

def Update_ingreKeyword():
    ingreReviewPath = r'C:\Final_Project_Files\IngreReviews'
    UpdateLi = [("yes", ingreCode) for ingreCode in os.listdir(ingreReviewPath)]
    
    connection, cursor = dbConnection()
    
    sql = "UPDATE ingredient SET ingreKeyword = %s WHERE ingreCode = %s"
    cursor.executemany(sql, UpdateLi)
    
    connection.commit()
    cursor.close()
    connection.close()
    
    print("Update IngreKeyword")

def Preprocessing_Reviews():
    FinalFolder = r'C:\Final_Project_Files'
    FinalJsonFolder = r'C:\Final_Project_Files\dataes\Cosmetic\Final'
    categoryLi = ["Skin", "Cream", "Lotion"]

    FinalCheck = []
    for jsonfile in os.listdir(FinalJsonFolder):
        if jsonfile.endswith(".json"):
            jsonData = openJson(os.path.join(FinalJsonFolder, jsonfile))
            for data in jsonData:
                if jsonData[data]['allIngredient']:
                    FinalCheck.append(jsonData[data]['productID'])

    for cat in tqdm(categoryLi):
        categoryPath = os.path.join(FinalFolder, cat)
        for files in os.listdir(categoryPath):
            productsJson = openJson(os.path.join(categoryPath, files, 'product.json'))
            reviewJson = openJson(os.path.join(categoryPath, files, 'Reviews.json'))
            
            productName = list(productsJson.keys())[0]
            productID = productsJson[productName]['productID']
            
            if (productsJson[productName]['allIngredient']) or (productID in FinalCheck):
                reviewDestFolder = os.path.join(FinalFolder, 'ProductReviews', productID)
                if not os.path.exists(reviewDestFolder):
                    os.mkdir(reviewDestFolder)

                preReviews = [sentence for sentence in sum([[re.sub("[^ 가-힣]+", "", i).strip() for i in review.split("\n")] for review in reviewJson], []) if sentence != '']
                
                destData = {"productID" : productID, "productName" : productName, "productReviews" : preReviews}
                
                # os.remove(os.path.join(categoryPath, files, 'Reviews.json'))
                toJson(os.path.join(reviewDestFolder, 'preReviews.json'), destData)
                
def ProductReivews():
    ReviewPath = r'C:\Final_Project_Files\ProductReviews'
    stopwords = set(openJson(r"C:\Team_Undefined\Pyscript\Modeling\KR-WordRank\stopwords.json"))
    fontPath, mask = ele_WordCloud()
    
    for files in tqdm(os.listdir(ReviewPath)):
        # 리뷰데이터
        preReviewsJson = openJson(os.path.join(ReviewPath, files, 'preReviews.json'))
        destReviews = [normalize(reviews) for reviews in preReviewsJson['productReviews']]
                
        try:    
            # KR-WordRank 키워드 추출
            keywords = summarize_with_keywords(
                destReviews, min_count=10, max_length=10,
                num_keywords= 100, verbose=True, stopwords=stopwords
            )
            
            if keywords:
                # 추출한 키워드 저장
                toJson(os.path.join(ReviewPath, files, 'Keywords.json'), {"productID" : preReviewsJson['productID'], "Keywords" : keywords})
                
                # 워드 클라우드 저장
                make_WordCloud(fontPath, mask, keywords, ReviewPath, files)
            else:
                # 키워드 추출이 안되면 해당 상품폴더 삭제
                shutil.rmtree(os.path.join(ReviewPath, files))            
        except ValueError:
            # 키워드 추출이 안되면 해당 상품폴더 삭제
            shutil.rmtree(os.path.join(ReviewPath, files))

def IngreReviews():
    productReviewPath = r'C:\Final_Project_Files\ProductReviews'
    ingreReviewPath = r'C:\Final_Project_Files\IngreReviews'
    stopwords = set(openJson(r"C:\Team_Undefined\Pyscript\Modeling\KR-WordRank\stopwords.json"))
    fontPath, mask = ele_WordCloud()
    
    IngreProduct = Select_IngreProdcut()
    
    for ingre in tqdm(IngreProduct):

        IngreProductReivews = []
        for product in ingre['ingreProduct'].split("|"):
            if os.path.exists(os.path.join(productReviewPath, product)):
                # 리뷰데이터
                preReviewJson = openJson(os.path.join(productReviewPath, product, 'preReviews.json'))
                IngreProductReivews += [normalize(review) for review in preReviewJson['productReviews']]
        
        try:
            # KR-WordRank 키워드 추출
            keywords = summarize_with_keywords(
                IngreProductReivews, min_count=10, max_length=10,
                num_keywords=100, verbose=True, stopwords=stopwords
            )
            
            if keywords:
                ingrePath = os.path.join(ingreReviewPath, str(ingre['ingreCode']))
                if not os.path.exists(ingrePath):
                    os.mkdir(ingrePath)
                    
                # 추출한 키워드 저장
                toJson(os.path.join(ingrePath, 'Keywords.json'), {'IngreCode' : ingre['ingreCode'], 'Keywords' : keywords})
                
                # 워드클라우드 저장
                make_WordCloud(fontPath, mask, keywords, ingreReviewPath, str(ingre['ingreCode']))
        except ValueError:
            pass
            
def ele_WordCloud():
    fontPath =  r'C:\Users\evil8\AppData\Local\Microsoft\Windows\Fonts\NanumBarunGothicBold.ttf'
    mask = Image.new("RGBA", (500, 500), (255, 255, 255))
    image = Image.open('C:\Team_Undefined\Pyscript\Modeling\KR-WordRank\mask.png').convert("RGBA").resize((500, 500))
    mask.paste(image,(0,0,image.size[0], image.size[1]),image)
    mask = np.array(mask)
    return fontPath,mask

def make_WordCloud(fontPath, mask, keywords, ReviewPath, files):
    Wc = WordCloud(
                max_font_size=300, font_path=fontPath, 
                background_color='white', mask=mask,
                ).generate_from_frequencies(keywords)
            
    # plt.figure(figsize=(5, 5))
    # plt.tight_layout(pad=0)
    # plt.axis('off')
    # plt.imshow(Wc, interpolation='bilinear')
    # plt.savefig('pltTest.png', format='png')
    Wc.to_file(os.path.join(ReviewPath, files, 'WordCloud.png'))

def copyFolders(ReviewsFolderPath, destFolder):
    staticImgFolder = r'C:\Team_Undefined\Project2-1\src\main\resources\static\assets\img'
    for pkey in tqdm(os.listdir(ReviewsFolderPath)):
        imgPath = os.path.join(ReviewsFolderPath, pkey, 'WordCloud.png')
        if os.path.exists(imgPath):
            shutil.copy(imgPath, os.path.join(staticImgFolder, destFolder, f"{pkey}.png"))