from Preprocessing import product_pre
from DBcontrol import projectDAO
import sys, requests, json

if __name__ == '__main__':
    categoryLi = ["Skin", "Cream", "Lotion"]
    
    for cat in categoryLi:
        MonthLi = product_pre.Naver_Month_Cosmetic(cat) # 현재 텍스트 파일 안 지움
        
        projectDAO.Update_ingredientRanking(cat, MonthLi)
        
        # Slack Message
        requests.post('https://hooks.slack.com/services/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', data=json.dumps({"text": f"Month {cat} Update Done!!"}))
        
    sys.exit()