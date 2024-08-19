import pydot

from utils import exception_handler_wrapper
from request_utils import RequestUtils
from constants import BASE_URL, TIMEOUT


class GitHubGraph:

    def __init__(self, token: str, owner: str, repo: str):
        self.token = token
        self.owner = owner
        self.repo = repo
        self.headers = {"Authorization": f"token {self.token}"}
        self.request_utils = RequestUtils(self.headers, TIMEOUT)

    @exception_handler_wrapper
    def get_commits(self, branch: str = "master") -> str:
        url = f"{BASE_URL}/repos/{self.owner}/{self.repo}/commits?sha={branch}"
        return self.request_utils.make_request(url).json()

    @exception_handler_wrapper
    def create_commit_graph(
        self, branch: str = "master", output_file: str = "commit_graph.dot"
    ) -> None:
        commits = self.get_commits(branch)
        graph = pydot.Dot(graph_type="digraph")
        commit_nodes = {}  # Store nodes by commit SHA to add edges later

        # Create nodes for each commit
        for commit in commits:
            commit_sha = commit['sha']
            commit_message = commit['commit']['message'].split('\n')[0]
            node = pydot.Node(commit_sha, label=commit_message)
            graph.add_node(node)
            commit_nodes[commit_sha] = node
        
        # Create edges between commits and handle merges
        for commit in commits:
            commit_sha = commit['sha']
            parents = commit['parents']
            
            for parent in parents:
                parent_sha = parent['sha']
                if parent_sha in commit_nodes:
                    graph.add_edge(pydot.Edge(commit_nodes[parent_sha], commit_nodes[commit_sha]))
        

        graph.write(output_file)
