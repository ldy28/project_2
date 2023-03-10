from urllib.parse import urlparse
from difflib import SequenceMatcher
from collections import Counter
from random import shuffle
from tqdm import tqdm
from datetime import datetime
import string, json, os, re

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

def make_all_Naver_productData(category):
        allSkindata = {}
        category_path = os.path.join(r'C:\Final_Project_Files', category)
        
        for skin in os.listdir(category_path):
            skinjson = os.path.join(category_path, skin, 'product.json')
            jsonData = openJson(skinjson)
            
            for data in jsonData:
                jsonData[data]['productID'] = urlparse(jsonData[data]['productImg']).path.split("/")[-1].split(".")[0]
                allSkindata[data] = jsonData[data]

            toJson(skinjson, jsonData)
        
        toJson(os.path.join(category_path, f"Naver_{category}.json"), allSkindata)
        
def Ingre_preprocessing(alldataPath):
    allData = openJson(alldataPath)
    isingre = {}
    notingre = {}

    for data in allData:
        if allData[data]['allIngredient']:
            isingre[data] = allData[data]
        else:
            notingre[data] = allData[data]
    
    for Nname in notingre:
        notingre_name = make_justName(Nname)
        for Iname in isingre:
            isingre_name = make_justName(Iname)
            if notingre_name == isingre_name:
                allData[Nname]['allIngredient'] = isingre[Iname]['allIngredient']
                allData[Nname]['analysisIngre'] = isingre[Iname]['analysisIngre']
                break
    
    re_savefile = os.path.split(alldataPath)
    toJson(os.path.join(re_savefile[0], f'{re_savefile[-1].split(".")[0]}_pre.json'), allData)
    
    return allData
    
def tempCheck(alldata):
    cnt = 0
    for data in alldata:
        if not alldata[data]['allIngredient']:
            cnt += 1
    return cnt

def make_justName(name):
    name_split = name.split(" ")
    capacity = None
    for idx, word in enumerate(name_split):
        if re.search("[0-9]ml|[0-9]???|[0-9]g", word):
            capacity = idx
    return " ".join(name_split[:capacity]) if capacity else name

def tempingre(alldata):
    namesLi = list(alldata.keys())
    shuffle(namesLi) 
    return {i:alldata[i]['allIngredient'] for i in namesLi[:10]} 

def one_parenthesis_check(s):
    return True if s.find("(") == -1 and s.find(")") != -1 else False

def punc_check(s):
    my_punc = "[" + "".join([i for i in string.punctuation if i not in ['-', '/', '(', ')', '%']]) + "]"
    return re.sub(my_punc, '', s) if re.search(my_punc, s) else s

def capacity_check(s):
    ingreCap = '\(ci|[0-9]ppm\)|[0-9]ppb\)|[0-9]%\)|[0-9]mg\)|[0-9]pom\)|[0-9]k\)|[0-9]ng\)|\([0-9]'
    if re.search(ingreCap, s.lower().replace(" ", "")):
        idx_finded = s.find("(")
        if idx_finded != -1:
            return s[:idx_finded].strip()
        else:
            return s
    else:
        return s
    
def mapping_ingre(s):
    result = ""
    if re.search("2-??????|2-??????|2 -??????|2 -??????|2??????|2??????|2 ??????|2 ??????|2-??????|2- ??????", s):
        result = '1,2-???????????????'
    elif re.search("????????? EDTA|???????????????????????????|????????????????????????|?????????????????????|?????????????????????", s):
        result = '???????????????????????????'
    elif re.search("?????????????????????|????????????????????????????????????", s):
        result = '?????????????????????'
    elif re.search("????????????????????????????????????????????????|???????????????????????????????????????|?????????????????????????????????????????????", s):
        result = '??????????????????????????????????????????'
    elif re.search("C13-16???????????????|C13-16??????????????????", s):
        result = 'C13-16??????????????????'
    elif re.search("C12-14???????????????|C12-14??????????????????", s):
        result = 'C12-14??????????????????'
    elif re.search("C13-14???????????????|C13-14??????????????????", s):
        result = 'C13-14??????????????????'
    elif re.search("??????????????????????????????", s):
        result = '???????????????????????????????????????'
    elif re.search("3-??????|3 -??????|3??????", s):
        result = '2,3-???????????????'
    elif re.search("???????????????|??????-?????????", s):
        result = '??????-?????????'
    elif re.search("?????????E", s):
        result = '????????????'
    elif re.search("????????????????????????", s):
        result = '??????????????????????????????'
    elif re.search("????????????????????????", s):
        result = '??????????????????????????????'
    elif re.search("????????? ?????????|??????????????????", s):
        result = '?????????'
    elif re.search("??????????????????????????????", s):
        result = '??????/??????????????????????????????'
    elif re.search("????????????????????????", s):
        result = '??????/????????????????????????'
    elif re.search("??????????????????", s):
        result = '??????????????????'
    elif re.search("?????????????????????", s):
        result = '?????????????????????'
    elif re.search("???????????????", s):
        result = '???????????????'
    elif re.search("??????????????????", s):
        result = '??????????????????'
    elif re.search("?????????", s):
        result = '?????????'
    else:
        result = s
    return result.strip()

def old_to_cur(s, ingreOldData):
    check = s.lower().replace(" ", "")
    if s in ingreOldData.keys():
        return ingreOldData[s]
    elif check in ingreOldData.keys():
        return ingreOldData[check]
    else:
        return s
    
def check_cur(s, ingreNames):
    check = s.lower().replace(" ", "")
    for name in ingreNames:
        if name.lower().replace(" ", "") == check:
            return name
    else:
        return s
    
def del_descript(s):
    check = re.search("\( ?[???-??????-??????-???]*", s)
    if check:
        return s[:check.span()[0]].strip()
    else:
        return s
    
def check_mistake(s, ingreLi):
    return sorted([[i, SequenceMatcher(None, s, i).ratio()] for i in ingreLi], key=lambda x:x[1], reverse=True)[0]

def del_digit(s):
    check = re.search('[???-??????-??????-???]+ ?[0-9]+[IU%]+', s)
    if check:
        digit = re.search('[0-9]+', s)
        return s[:digit.span()[0]].strip()
    else:
        return s
    
def Final_Preprocessing(category):
    categoryFolder = os.path.join(r'C:\Final_Project_Files', category)
    ingreFolder = os.path.join(r'C:\Final_Project_Files', 'dataes', 'Ingredient')

    IngreDictpath = os.path.join(ingreFolder, 'Final_Ingredient_Dictionary.json')
    ingreOldpath = os.path.join(ingreFolder, 'temp_old.json')

    IngreDict = openJson(IngreDictpath)
    ingreOldData = openJson(ingreOldpath)

    ingreNames = [i['ingreName'] for i in IngreDict]
    ingreOldName = list(ingreOldData.keys())
    scoreDict = {i['ingreName'] : i for i in IngreDict}

    for product in tqdm(os.listdir(categoryFolder)):
        
        productPath = os.path.join(categoryFolder, product, 'product.json')
        
        if os.path.exists(productPath):
            
            productData = openJson(productPath)
            productName = list(productData.keys())[0]

            tempDict = {}
            tempLi = []
            ewgLi, dryLi, oilLi, sensitiveLi, allergyLi = [], [], [], [], []
            
            if productData[productName]['allIngredient']:
                for ingre in productData[productName]['allIngredient'][:]:
                    if not ingre.isdigit() and not one_parenthesis_check(ingre):
                        ingre = capacity_check(punc_check(ingre))
                        ingre = mapping_ingre(ingre)
                        ingre = del_descript(ingre)
                        ingre = del_digit(ingre)
                        ingre = old_to_cur(check_cur(ingre, ingreNames), ingreOldData)
                        tempLi.append(ingre)
                tempDict[productName] = tempLi

                for idx, ingre in enumerate(tempDict[productName][:]):
                    if ingre not in ingreNames:
                        cur = check_mistake(ingre, ingreNames)
                        old = check_mistake(ingre, ingreOldName)
                        if cur[1] >= 0.85 or old[1] >= 0.85:
                            if cur[1] >= old[1]:
                                tempDict[productName][idx] = cur[0]
                            else:
                                tempDict[productName][idx] = ingreOldData[old[0]]
                                
                for ingre in tempDict[productName]:
                    if ingre in scoreDict.keys():
                        if scoreDict[ingre]['ewgScore'] != '????????????':
                            ewgLi.append(scoreDict[ingre]['ewgScore'])
                        else:
                            ewgLi.append("0")
                        
                        dryLi.append(str(scoreDict[ingre]['dryScore']))
                        oilLi.append(str(scoreDict[ingre]['oilScore']))
                        sensitiveLi.append(str(scoreDict[ingre]['sensitiveScore']))
                        allergyLi.append(str(scoreDict[ingre]['allergyScore']))
                    else:
                        ewgLi.append("0")
                        dryLi.append("0")
                        oilLi.append("0")
                        sensitiveLi.append("0")
                        allergyLi.append("0")
                    
                productData[productName]['allIngredient'] = tempDict[productName]
                productData[productName]['productEwgScore'] = "|".join(ewgLi)
                productData[productName]['productDryScore'] = "|".join(dryLi)
                productData[productName]['productOilScore'] = "|".join(oilLi)
                productData[productName]['productSensitiveScore'] = "|".join(sensitiveLi)
                productData[productName]['productAllegyScore'] = "|".join(allergyLi)
                productData[productName]['Final'] = "yes"
            else:
                productData[productName]['allIngredient'] = []
                productData[productName]['productEwgScore'] = "0"
                productData[productName]['productDryScore'] = "0"
                productData[productName]['productOilScore'] = "0"
                productData[productName]['productSensitiveScore'] = "0"
                productData[productName]['productAllegyScore'] = "0"
                productData[productName]['Final'] = "yes"
                
            toJson(productPath, productData)
                
    print("Final Preprocessing Done!!")
    
def make_Final_productData(category):
    FinalFolder = r'C:\Final_Project_Files'
    FinalDataFolder = os.path.join(FinalFolder, 'dataes', 'Cosmetic', 'Final')
    
    allCosdata = {}
    tempCheckdata = {}
    category_path = os.path.join(FinalFolder, category)
    result_path = os.path.join(FinalDataFolder, f"Final_{category}.json")
    
    for cos in tqdm(os.listdir(category_path)):
        cospath = os.path.join(category_path, cos, 'product.json')
        if os.path.exists(cospath):    
            jsonData = openJson(cospath)
            allCosdata.update(jsonData)
            for data in jsonData:
                if jsonData[data]['allIngredient']:
                    tempCheckdata[make_justName(data)] = jsonData[data]['allIngredient']
    
    for cos in allCosdata:
        if not allCosdata[cos]['allIngredient']:
            temp = make_justName(cos)
            if temp in tempCheckdata.keys():
                allCosdata[cos]['allIngredient'] = tempCheckdata[temp]
    
    toJson(result_path, allCosdata)
    print("make Final productData Done!!")

def Naver_Month_Cosmetic(category):
    destFolder = os.path.join(r'C:\Final_Project_Files\dataes\Cosmetic\tempData', category)
    
    MonthLi = []
    for files in os.listdir(destFolder):
        if files.endswith(".txt"):
            data = openTxt(os.path.join(destFolder, files))
            MonthLi += data
            # os.remove(os.path.join(destFolder, files))
    
    jsonName = datetime.today().strftime("%Y_%m_%d") + f"_Month_{category}.json"
    toJson(os.path.join(destFolder, jsonName), MonthLi)

    return MonthLi

def Final_Check_preprocessing(category):
    FinalFolder = r'C:\Final_Project_Files\dataes\Cosmetic\Final'
    IngreFolder = r'C:\Final_Project_Files\dataes\Ingredient'
    
    FinalData = openJson(os.path.join(FinalFolder, f"Final_{category}.json"))
    IngreDict = openJson(os.path.join(IngreFolder, 'Final_Ingredient_Dictionary.json'))
    ingreName = [i['ingreName'] for i in IngreDict]
    checkLi = []
    
    for product in FinalData:
        for ingreDient in FinalData[product]['allIngredient']:
            ingre = ingreDient.strip()
            if ingre not in ingreName:
                checkLi.append(ingre)
    
    resCheck = sorted(Counter(checkLi).items(), key=lambda x:x[1], reverse=True)
    
    for res in resCheck:
        print(res)

if __name__ == "__main__":
    Final_Preprocessing("Lotion")