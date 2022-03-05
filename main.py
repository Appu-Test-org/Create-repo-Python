import argparse
import os, json
import logging
# import urllib3
import requests
from requests.auth import HTTPBasicAuth
print("Hello its a ----main.py-----")

class GitHubConnect():
    def __init__(self, github_url, organisation_name, github_user, github_pat, repo_name, branch_name):
        self.github_url = github_url
        self.github_organisation_name = organisation_name
        self.github_user = github_user
        self.github_pat = github_pat
#         self.repo_name = repo_name
        self.branch_name = branch_name
        
    def create_repository(self):
        # https://docs.github.com/en/rest/reference/repos#create-a-repository-using-a-template
        data = {'name':self.repo_name, "owner": self.github_organisation_name, "private": True}
        URL = self.github_url + "/orgs/" + self.github_organisation_name + "/repos"
        response_data, response_code = self.post_api_call(URL, json.dumps(data))
        logging.debug(response_data)
        if response_code == 201:
            self.patch_repository_to_internal()
        else:
            logging.error("Unable to create the repository: " + self.repo_name)
            exit(1)

  
    def patch_repository_to_internal(self):
        data = {"visibility": "internal"}
        URL = self.github_url + "/repos/" + self.github_organisation_name + "/" + self.repo_name
        response_data, response_code = self.post_api_call(URL, json.dumps(data))
        logging.debug(response_data)
        if response_code != 200:
            logging.error("Unable to update repository to internal group")
            exit(1)
def main():
   
    github_url = "https://api.github.com"
    organisation_name = args["org_name"]
    github_user = args["user_name"]
    github_pat = args["pat"]

    repo_name = args["repo_name"]
    branch_name = args["branch_name"]
    template_repo_name = args["template_repo_name"]
    request_type = args["request_type"]
    issue_number= args["issue_number"]
    repo_name = "Appu"

    github = GitHubConnect(github_url, organisation_name, github_user, github_pat, repo_name, branch_name)
    
    if request_type == "Onboard":
        if template_repo_name == "None":
            github.create_repository()
        else:
            github.create_repository_from_template_repository(template_repo_name)
    elif request_type == "Offboard":
        github.delete_repository()
        
    github.update_issue(request_type, issue_number)

if __name__ == '__main__':
    main()
