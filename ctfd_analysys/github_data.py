import requests
import logging
from utils import exception_handler_wrapper
from constants import BASE_URL

class GitHubRepo:

    def __init__(self, token, owner, repo):
        self.token = token
        self.owner = owner
        self.repo = repo
        self.headers = {"Authorization": f"token {self.token}"}
        self.timeout = 3000

    @exception_handler_wrapper
    def get_latest_releases(self, n=3):
        url = f"{BASE_URL}/repos/{self.owner}/{self.repo}/releases"
        response = requests.get(url, headers=self.headers, timeout=self.timeout)
        response.raise_for_status()
        releases = response.json()
        return releases[:n]
    
    @exception_handler_wrapper
    def get_repo_info(self):
        url = f"{BASE_URL}/repos/{self.owner}/{self.repo}"
        response = requests.get(url, headers=self.headers, timeout=self.timeout)
        response.raise_for_status()
        return response.json()
    
    @exception_handler_wrapper
    def get_contributors(self):
        url = f"{BASE_URL}/repos/{self.owner}/{self.repo}/contributors"
        response = requests.get(url, headers=self.headers, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    @exception_handler_wrapper
    def get_pull_requests(self, state="all"):
        url = f"{BASE_URL}/repos/{self.owner}/{self.repo}/pulls?state={state}"
        response = requests.get(url, headers=self.headers, timeout=self.timeout)
        response.raise_for_status()
        return response.json()
    
    @exception_handler_wrapper
    def get_contributors_by_pr(self):
        contributors = self.get_contributors()
        pr_counts = {contributor['login']: 0 for contributor in contributors}

        pull_requests = self.get_pull_requests()
        for pr in pull_requests:
            author = pr['user']['login']
            if author in pr_counts:
                pr_counts[author] += 1

        sorted_contributors = sorted(pr_counts.items(), key=lambda item: item[1], reverse=True)
        return sorted_contributors
