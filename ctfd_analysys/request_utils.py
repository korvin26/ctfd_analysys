import logging
import time
import requests


class RequestUtils():
    def __init__(self, headers: dict, timeout: int) -> None:
        self.headers = headers
        self.timeout = timeout

    def make_request(self, url: str) -> requests.Response:
        logging.info(f"Making request to {url}")
        response = requests.get(url, headers=self.headers, timeout=self.timeout)
        self.update_rate_limit(response)
        response.raise_for_status()
        return response

    def get_next_page(self, response):
        link = response.headers.get("Link", None)
        if link:
            for part in link.split(","):
                if 'rel="next"' in part:
                    logging.info("Found next page")
                    return part.split(";")[0].strip("<> ")
        return None
    
    def with_pagination_handling(self, url: str) -> list:
        data = []
        while url:
            response = self.make_request(url)
            data.extend(response.json())
            url = self.get_next_page(response)
        return data

    def update_rate_limit(self, response) -> None:
        self.rate_limit_remaining = int(
            response.headers.get("X-RateLimit-Remaining", 0)
        )
        self.rate_limit_reset = int(response.headers.get("X-RateLimit-Reset", 0))
        if self.rate_limit_remaining == 0:
            reset_time = self.rate_limit_reset - int(time.time())
            logging.warning(
                f"Rate limit exceeded. Waiting {reset_time} seconds for reset."
            )
            time.sleep(reset_time)
