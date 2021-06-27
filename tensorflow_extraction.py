import requests
import json
from credentials import *

url = "https://api.github.com/repos/tensorflow/tensorflow/issues"
# header = {"Authorization": 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}
issue_response = requests.get(url,auth=(client_id,client_secret))
print(issue_response.headers.get('Link'))
print(issue_response.headers.get('X-RateLimit-Remaining'))