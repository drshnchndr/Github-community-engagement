import requests
import json

url = "https://api.github.com/repos/tensorflow/tensorflow/issues"
# header = {"Authorization": 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}
issue_response = requests.get(url,auth=('529b02d03f3320388992','5978b5a411d033c368795b11a815c921e46c20f6'))
print(issue_response.headers.get('Link'))
print(issue_response.headers.get('X-RateLimit-Remaining'))