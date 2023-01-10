from collections import Counter
import pymysql
import json
import os

def dbConnection():
    connection = pymysql.connect(host='project-db-stu.ddns.net', port=3307, user='Anjisu', password='12345', db='Anjisu', charset='utf8')
    cursor = connection.cursor()
    return connection, cursor

def dbConnection_dict():
    connection = pymysql.connect(host='project-db-stu.ddns.net', port=3307, user='Anjisu', password='12345', db='Anjisu', charset='utf8')
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    return connection, cursor
        
def Insert_Ingredient():
    ingreData = openJson(os.path.join(r'C:\Final_Project_Files\dataes', 'Ingredient', 'Final_Ingredient_Dictionary.json'))
    cosmeticInfo = Select_for_Ingredient()
    
    connection, cursor = dbConnection()
    
    try:
        sql = """
            insert into 
            ingredient(ingreCode, ingreName, ingreEngName, ingreCas, ingreOldName, ingreEwg, ingreEwgData,
                    IngreObj, ingreDryScore, ingreOilScore, ingreSensitiveScore, ingreAllegyScore, ingreProduct) 
            values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
        
        insertData = []
        for ingre in ingreData:
            ingreCode = int(ingre['ingreCode'])
            ingreName = ingre['ingreName']
            ingreEngName = ingre['ingreEngName'] if ingre['ingreEngName'] else "None"
            ingreCas = ingre['ingreCas'] if ingre['ingreCas'] else "None"
            ingreOldName = ingre['ingreOldName'] if ingre['ingreOldName'] else "None"
            ingreEwg = ingre['ewgScore'] if ingre['ewgScore'] != '등급없음' else "None"
            ingreEwgData = ingre['ewgGrade'] if ingre['ewgGrade'] != '등급없음' else "None"
            ingreObj = "|".join([i.strip() for i in ingre['ingreObj']]) if ingre['ingreObj'] else "None"
            ingreDryScore = int(ingre['dryScore'])
            ingreOilScore = int(ingre['oilScore'])
            ingreSensitiveScore = int(ingre['sensitiveScore'])
            ingreAllegyScore = int(ingre['allergyScore'])
            ingreProduct = make_IngreProduct(cosmeticInfo, ingre['ingreName'])
            insertData.append([ingreCode, ingreName, ingreEngName, ingreCas, ingreOldName, ingreEwg, ingreEwgData, ingreObj, ingreDryScore, ingreOilScore, ingreSensitiveScore, ingreAllegyScore, ingreProduct])
        
        cursor.executemany(sql, insertData)
        connection.commit()
        print("Insert Ingredient Done!!")
    except Exception as e:
        raise e
    
    cursor.close()
    connection.close()
        
def Insert_product(category):
    category_dict = {"Skin" : "S", "Cream" : "C", "Lotion" : "L", "Essence" : "E", "BodyLotion" : "B", "BodyCream" : "D"}
    curCosmetic = [i['productID'] for i in Select_Cur_Cosmetic()]
    connection, cursor = dbConnection()
    productData = openJson(os.path.join(r'C:\Final_Project_Files\dataes', 'Cosmetic', 'Final', f"Final_{category}.json"))
    
    try:
        sql = """
            insert into 
            cosmetic(productID, productNM, productImg, productCharacter, productStar, productMaker, productBrand, productDate, productReviewCnt,
                    productIngredient, productStarRatio, productAgeLikes, productSexLikes, productEwgScore, 
                    productDryScore, productOilScore, productSensitiveScore, productAllegyScore, productType)
            values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
        
        insertData = []
        for product in productData:
            if productData[product]['productID'] not in curCosmetic: # 현재 DB에 있는 값은 무시하고
                if productData[product]['allIngredient']: # 성분이 없는건 깔끔하게 무시.
                    productID = productData[product]['productID']
                    productNM = product.strip()
                    productImg = productData[product]['projectImg'].strip()
                    productCharacter = productData[product]['productCharacter']        
                    productStar = productData[product]['productStar']
                    productMaker = productData[product]['productMaker']
                    productBrand = productData[product]['productBrand']
                    productDate = productData[product]['productDate']
                    productReviewCnt = productData[product]['productReviewCnt']
                    productIngredient = "|".join([i.strip() for i in productData[product]['allIngredient']]) if productData[product]['allIngredient'] else "None"
                    productStarRatio = productData[product]['productStarRatio']
                    productAgeLikes = productData[product]['productAgeLikes']
                    productSexLikes = productData[product]['productSexLikes']
                    productEwgScore = productData[product]['productEwgScore']
                    productDryScore = productData[product]['productDryScore']
                    productOilScore = productData[product]['productOilScore']
                    productSensitiveScore = productData[product]['productSensitiveScore']
                    productAllegyScore = productData[product]['productAllegyScore']
                    productType = category_dict[category]
                    
                    insertData.append([productID, productNM, productImg, productCharacter, productStar, productMaker, productBrand, productDate,
                                    productReviewCnt, productIngredient, productStarRatio, productAgeLikes, productSexLikes, productEwgScore,
                                    productDryScore, productOilScore, productSensitiveScore, productAllegyScore, productType])
            
        cursor.executemany(sql, insertData)
        connection.commit()
        print("Insert Cosmetic Done!!")
        
    except Exception as e:
        raise e
    
    cursor.close()
    connection.close()

def Update_productRanking(category, weekProduct):
    result = [i['productID'] for i in Select_Cat_Cosmetic_productID(category)]
    checkLi = []
    rank = 0
    
    for productID in weekProduct:
        if productID in result:
            rank += 1
            checkLi.append((rank, int(productID)))
            
    connection, cursor = dbConnection()

    sql = "UPDATE cosmetic SET productRank = %s WHERE productID = %s"
    cursor.executemany(sql, checkLi)

    connection.commit()
    cursor.close()
    connection.close()
    
    print("Update prodcut Ranking Done")
    
def Update_ingredientRanking(category, MonthLi):
    categoryDict = {"Skin" : 'ingreSkinRanking', "Cream" : 'ingreCreamRanking', "Lotion" : 'ingreLotionRanking'}
    result = {i['productID'] : i for i in Select_All_Cosmetic(category)}
    ingreLi = []
    
    for productID in MonthLi:
        if productID in result.keys():
            ingreLi.append([i.strip() for i in result[productID]['productIngredient'].split("|")])
    
    countedLi = list(Counter(sum(ingreLi, [])).items())
    resultLi = [(idx+1, val[0]) for idx, val in enumerate(Ingre_Rank(countedLi))]
            
    connection, cursor = dbConnection()
    
    sql = f"UPDATE ingredient SET {categoryDict[category]} = %s WHERE ingreName = %s"
    cursor.executemany(sql, resultLi)
    
    connection.commit()
    cursor.close()
    connection.close()
    
    print(f"Update {category} Ranking Done")
    
def Update_ingredientProduct():
    cosmeticInfo = Select_for_Ingredient()
    curIngredient = Select_Cur_Ingredient()
    
    updateLi = [((make_IngreProduct(cosmeticInfo, ingre['ingreName']), ingre['ingreCode'])) for ingre in curIngredient]
    connection, cursor = dbConnection()

    sql = f"UPDATE ingredient SET ingreProduct = %s WHERE ingreCode = %s"
    cursor.executemany(sql, updateLi)

    connection.commit()
    cursor.close()
    connection.close()
    
    print("Update Ingredient Product Done")
        
def Select_Cat_Cosmetic_productID(category):
    categoryDict = {"Skin" : 'S', "Cream" : 'C', "Lotion" : 'L'}
    productType = categoryDict[category]
    connection, cursor = dbConnection_dict()
    
    sql = f"select productID from cosmetic where productType = '{productType}'"
    cursor.execute(sql)
    result = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return result

def Select_All_Cosmetic(category):
    categoryDict = {"Skin" : 'S', "Cream" : 'C', "Lotion" : 'L'}
    productType = categoryDict[category]
    connection, cursor = dbConnection_dict()
    
    sql = f"select * from cosmetic where productType = '{productType}'"
    cursor.execute(sql)
    result = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return result

def Select_for_Ingredient():
    connection, cursor = dbConnection_dict()
    
    sql = f"select productID, productReviewCnt, productIngredient from cosmetic"
    cursor.execute(sql)
    result = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return result

def Select_Cur_Cosmetic():
    connection, cursor = dbConnection_dict()
    
    sql = f"select productID from cosmetic"
    cursor.execute(sql)
    result = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return result
    
def Select_Cur_Ingredient():
    connection, cursor = dbConnection_dict()
    
    sql = f"select ingreCode, ingreName from ingredient"
    cursor.execute(sql)
    result = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return result

def openJson(Jsonpath):
    with open(Jsonpath, 'r', encoding='utf-8') as f:
        jsonData = json.load(f)
    return jsonData

def toJson(JsponPath, destData):
    with open(JsponPath, 'w', encoding='utf-8') as f:
        json.dump(destData, f, ensure_ascii=False)

def openTxt(txtPath):
    with open(txtPath, 'r', encoding='utf-8') as f:
        data = f.read().splitlines()
    return [i.strip() for i in data]

def make_IngreProduct(cosmeticInfo, ingre):
    IngreProductLi = []
    for cos in cosmeticInfo:
        prodcutIngredient = [i.strip() for i in cos['productIngredient'].split("|")]
        if ingre in prodcutIngredient:
            IngreProductLi.append([cos['productID'], cos['productReviewCnt']])
    
    if IngreProductLi:
        resultIngreProduct = sorted(IngreProductLi, key=lambda x:x[1], reverse=True)[:20]
        return "|".join([i[0] for i in resultIngreProduct])
    else:
        return ""
    
def Ingre_Rank(countedLi : list):
    delIngre = openTxt(os.path.join(r'C:\Final_Project_Files\dataes\Ingredient', 'NopeIngre.txt'))
    funcIngre = openTxt(os.path.join(r'C:\Final_Project_Files\dataes\Ingredient', 'funcIngre.txt'))
    vitaminIngre = ['레티놀', '판테놀', '아스코빅애씨드', '아스코빌글루코사이드', '에칠아스코빌에텔', '소듐아스코빌포스페이트', '토코페롤', '바이오틴', '베타-카로틴']
    resultLi = []
    
    for ing, count in countedLi:
        ingre = ing.strip()
        if ingre not in delIngre:
            # 특정 성분 추출물
            if ingre.endswith('추출물') or ingre.endswith('오일'):
                count *= 1.5
            # 히알루론산
            elif ingre.find('하이알루') != -1:
                count *= 1.3
            # 비타민 관련 성분
            elif ingre in vitaminIngre:
                count *= 1.3
            # 기능성 화장품 관련 성분
            elif ingre in funcIngre:
                count *= 1.3
            
            resultLi.append([ingre, count])
    
    # 상위 10개 반환
    return sorted(resultLi, key=lambda x: x[1], reverse=True)

def test():
    sql = "select * from ingredient"
    
    connection, cursor = dbConnection_dict()
    cursor.execute(sql)
    
    result = cursor.fetchall()
    
    cursor.close()
    connection.close()

    for res in result:
        print(res)
        
# if __name__ == "__main__":
