import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Used to analyze CTFd GitHub repository")

    parser.add_argument(
        "--log-to", 
        choices=["stdout", "file"],
        default="stdout",
        help="Specify logging output: stdout or file"
    )
    parser.add_argument(
        "--debug", 
        action="store_true",
        help="Enable debug mode"
    )
    parser.add_argument(
        "--token", 
        required=True,
        help="GitHub access token"
    )
    parser.add_argument(
        "--owner",
        required=True,
        help="GitHub repository owner"
    )
    parser.add_argument(
        "--repo",
        required=True,
        help="GitHub repository name"
    )
    parser.add_argument(
        "--branch",
        default="master",
        help="GitHub repository branch"
    )

    return parser.parse_args()
