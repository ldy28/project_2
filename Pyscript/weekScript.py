from Crawling import Crawling_Service
from DBcontrol import projectDAO
import sys, requests, json

if __name__ == "__main__":
    app = Crawling_Service.Crawling_process()
    
    categoryLi = ["Skin", "Cream", "Lotion"]
    
    for cat in categoryLi:
        weekProduct = app.week_Crawling_process(cat)
        projectDAO.Update_productRanking(cat, weekProduct)
    
        # Slack Message
        requests.post('https://hooks.slack.com/services/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', data=json.dumps({"text": f"Week {cat} Update Done!!"}))
    
    print("week Crawling process Done")
    sys.exit()
    