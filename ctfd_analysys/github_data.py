from utils import exception_handler_wrapper
from request_utils import RequestUtils
from constants import BASE_URL, PER_PAGE, TIMEOUT


class GitHubRepo:

    def __init__(self, token: str, owner: str, repo: str):
        self.token = token
        self.owner = owner
        self.repo = repo
        self.headers = {"Authorization": f"token {self.token}"}
        self.request_utils = RequestUtils(self.headers, TIMEOUT)

    @exception_handler_wrapper
    def get_latest_releases(self, n: int = 3) -> list:
        url = f"{BASE_URL}/repos/{self.owner}/{self.repo}/releases"
        return self.request_utils.with_pagination_handling(url)[:n]
    
    @exception_handler_wrapper
    def get_repo_info(self) -> dict:
        url = f"{BASE_URL}/repos/{self.owner}/{self.repo}"
        return self.request_utils.make_request(url).json()

    @exception_handler_wrapper
    def get_contributors(self) -> list:
        url = f"{BASE_URL}/repos/{self.owner}/{self.repo}/contributors"
        return self.request_utils.make_request(url).json()

    @exception_handler_wrapper
    def get_pull_requests(self, state: str = "all") -> list:
        url = f"{BASE_URL}/repos/{self.owner}/{self.repo}/pulls?state={state}&per_page={PER_PAGE}"
        return self.request_utils.with_pagination_handling(url)

    @exception_handler_wrapper
    def get_contributors_by_pr(self) -> list[tuple[str, int]]:
        contributors = self.get_contributors()
        pr_counts = {contributor["login"]: 0 for contributor in contributors}

        pull_requests = self.get_pull_requests()
        for pr in pull_requests:
            author = pr["user"]["login"]
            if author in pr_counts:
                pr_counts[author] += 1

        sorted_contributors = sorted(
            pr_counts.items(), key=lambda item: item[1], reverse=True
        )
        return sorted_contributors
