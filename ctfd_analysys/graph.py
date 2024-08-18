import requests
import pydot
from utils import exception_handler_wrapper
from constants import BASE_URL

class GitHubGraph:

    def __init__(self, token, owner, repo):
        self.token = token
        self.owner = owner
        self.repo = repo
        self.headers = {"Authorization": f"token {self.token}"}
        self.timeout = 3000

    @exception_handler_wrapper
    def get_commits(self, branch="master"):
        url = f"{BASE_URL}/repos/{self.owner}/{self.repo}/commits?sha={branch}"
        response = requests.get(url, headers=self.headers, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    @exception_handler_wrapper
    def create_commit_graph(self, branch="master", output_file="commit_graph.dot"):
        commits = self.get_commits(branch)
        graph = pydot.Dot(graph_type="digraph")

        previous_node = None

        for commit in commits:
            commit_hash = commit['sha']
            commit_message = commit['commit']['message'].split('\n')[0]
            node = pydot.Node(commit_hash, label=commit_message)
            graph.add_node(node)

            if previous_node:
                graph.add_edge(pydot.Edge(previous_node, node))

            previous_node = node

        graph.write(output_file)
