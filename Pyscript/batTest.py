import sys, json, requests

if __name__ == "__main__":
    # Slack Message
    requests.post('https://hooks.slack.com/services/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',
                    headers={"Content-type" : "application/json"},
                    data=json.dumps({"text": f"Hello World!!"}), 
                    verify=False)

