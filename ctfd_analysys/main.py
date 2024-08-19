from cli import parse_args
from github_data import GitHubRepo
from graph import GitHubGraph
from logging_setup import setup_logging
import logging


def main():
    args = parse_args()

    # Set up logging
    setup_logging(log_to=args.log_to, debug=args.debug)
    logger = logging.getLogger(__name__)

    # Initialize GitHubRepo instance
    repo = GitHubRepo(token=args.token, owner=args.owner, repo=args.repo)

    # Fetch and log repository data
    logger.info("Fetching repository data...")

    latest_releases = repo.get_latest_releases()
    logger.info(
        f"Latest 3 releases: {[release['tag_name'] for release in latest_releases]}"
    )

    repo_info = repo.get_repo_info()
    logger.info(
        "Forks: %s , Stars: %s , Contributors: %s",
        repo_info.get('forks_count'),
        repo_info.get('stargazers_count'),
        len(repo.get_contributors())
    )

    pr_counts = repo.get_contributors_by_pr()
    logger.info(f"Contributors by pull requests: {pr_counts})")

    # Create commit graph
    logger.info("Creating commit graph...")
    graph = GitHubGraph(token=args.token, owner=args.owner, repo=args.repo)
    graph.create_commit_graph(branch=args.branch, output_file="commit_graph.dot")
    logger.info("Commit graph created successfully.")


if __name__ == "__main__":
    main()
