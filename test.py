from github import Github
import requests
import json
import pprint as pprint

# First create a Github instance:

# using an access token
# g = Github("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")

# Github Enterprise with custom hostname
# g = Github(base_url="https://{hostname}/api/v3", login_or_token="access_token")

# Then play with your Github objects:
# for repo in g.get_user().get_repos():
#     print(repo.name)

# repo = g.get_repo("tensorflow/tensorflow")


stars_repo_response = requests.get("https://api.github.com/search/repositories?q=stars:>=200000")
json_data = json.loads(stars_repo_response.text)

# pprint.pprint(json_data)
# print(json_data["items"])

repo_list = []

for item in json_data["items"]:
    #print(item.get('full_name'))
    repo_list.append(item.get('full_name'))

print(repo_list)

for repos in repo_list:
    repo_response = requests.get("https://api.github.com/repos/"+repos)

    # print(repo_response)
    repo_json_data = json.loads(repo_response.text)
    # pprint.pprint(repo_json_data)
    print(repo_json_data['full_name'])
    print(repo_json_data['open_issues'])
    url = "https://api.github.com/repos/"+repo_json_data['full_name']+"/issues"
    headers = {"Authorization": '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'}
    issue_response = requests.get(url,headers)
    print(issue_response.headers)
    
    link = issue_response.headers.get('Link')
    if link is not None:
        print(link)