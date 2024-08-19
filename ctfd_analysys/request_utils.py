import logging
import time
import requests


class RequestUtils():
    def __init__(self, headers: dict, timeout: int) -> None:
        self.headers = headers
        self.timeout = timeout

    def make_request(self, url: str) -> requests.Response:
        logging.info("Making request to %s", url)
        response = requests.get(url, headers=self.headers, timeout=self.timeout)
        self.update_rate_limit(response)
        response.raise_for_status()
        return response

    def get_next_page(self, response):
        link = response.headers.get("Link", None)
        if link:
            for part in link.split(","):
                if 'rel="next"' in part:
                    np = part.split(";")[0].strip("<> ")
                    logging.info("Found next page %s", np)
                    return np
        return None

    def with_pagination_handling(self, url: str) -> list:
        data = []
        while url:
            response = self.make_request(url)
            data.extend(response.json())
            url = self.get_next_page(response)
        return data

    def update_rate_limit(self, response) -> None:
        rate_limit_remaining = int(
            response.headers.get("X-RateLimit-Remaining", 0)
        )
        rate_limit_reset = int(response.headers.get("X-RateLimit-Reset", 0))
        if rate_limit_remaining == 0:
            reset_time = rate_limit_reset - int(time.time())
            logging.warning(
                "Rate limit exceeded. Waiting %s seconds for reset.",
                reset_time
            )
            time.sleep(reset_time)
