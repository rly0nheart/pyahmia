import typing as t
from contextlib import suppress

import requests
from bs4 import BeautifulSoup
from requests import Response
from requests.exceptions import RequestException
from requests_tor import RequestsTor
from rich.status import Status
from update_checker import UpdateChecker

from pyahmia.src.api.cache import CacheManager
from pyahmia.src.lib import console

TIME_PERIODS = t.Literal["day", "week", "month", "all"]
BASE_URL_CLEARNET = "https://ahmia.fi"
BASE_URL_DARKNET = "https://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion"

__all__ = ["Ahmia"]


class Ahmia:
    def __init__(
        self, user_agent: str, timeout: int = 10, use_tor: bool = False, no_cache: bool = False,
    ):
        self.user_agent = user_agent
        self.use_tor = use_tor
        self.no_cache = no_cache
        self.timeout = timeout
        self.cache = None if no_cache else CacheManager()

        if self.use_tor:
            self.search_endpoint: str = (
                f"{BASE_URL_DARKNET}/search"
            )
            self.session = RequestsTor(tor_ports=(9050,), tor_cport=(9051,))
        else:
            self.search_endpoint: str = f"{BASE_URL_CLEARNET}/search"
            self.session = requests.Session()

    def search(
        self,
        query: str,
        time_period: TIME_PERIODS = "all",
        status: t.Optional[Status] = None,
    ) -> dict:
        """
        Search Ahmia.fi for hidden services on the Tor network, that match with the `query`.

        :param query: Search query.
        :param time_period: Time period to get results from
          (expects either: `day`, `week`, `month`, and/or `all`)
        :param status:
        :return: A SimpleNamespace containing the search summary, total results count,
        and a list of SimpleNamespace objects, each containing info on an individual search result.
        """
        # Check cache first
        if not self.no_cache and self.cache:
            cache_key = self.cache.get_search_cache_key(
                query, time_period, self.use_tor
            )
            cached_result = self.cache.get(cache_key)
            if cached_result is not None:
                if isinstance(status, Status):
                    console.log("[bold #c7ff70]✔[/bold #c7ff70] Results loaded from cache.")
                return cached_result

        token = self.get_token(status=status)

        if isinstance(status, Status):
            status.update(
                f"[dim]Searching for [#c7ff70]{query}[/][/dim][yellow]…[/yellow]"
            )

        if token[0] is None or token[1] is None:
            console.log(
                f"[bold red]✘[/bold red] Token appears to be invalid ({token}), this might return empty results."
            )
            return {"success": False, "message": "Failed to obtain session token."}

        params = {"q": query}
        period_to_days = {"day": "1", "week": "7", "month": "30"}
        if time_period in period_to_days:
            params["d"] = period_to_days[time_period]
        params[token[0]] = token[1]

        results_soup = self._get_soup(url=self.search_endpoint, params=params)

        items = results_soup.find_all("li", {"class": "result"})
        total_count = len(items)

        if not items:
            return {
                "success": False,
                "message": f"Sorry, but PyAhmia couldn't find results for {query}.",
            }

        message_tag = results_soup.find("div", {"class": "resultsSubheader"})
        message = " ".join(message_tag.text.split())

        results = []

        for item in items:
            last_seen_tag = item.find("span", {"class": "lastSeen"})
            last_seen_text = (
                last_seen_tag.get_text(strip=True) if last_seen_tag else "NaN"
            )
            last_seen_timestamp = (
                last_seen_tag.get("data-timestamp") if last_seen_tag else "NaN"
            )

            title: list[str] = item.find("h4").text.split() or ["No title provided"]
            description: list[str] = item.find("p").text.split()
            url: list[str] = item.find("cite").text.split()
            last_seen_relative: str = last_seen_text.replace("\xa0", " ")

            results.append(
                {
                    "title": " ".join(title),
                    "about": " ".join(description),
                    "url": " ".join(url),
                    "last_seen_rel": last_seen_relative,
                    "last_seen_ts": last_seen_timestamp,
                }
            )

        result = {
            "success": True,
            "message": message,
            "total_count": total_count,
            "results": results,
        }

        # Cache the successful result
        if not self.no_cache and self.cache:
            cache_key = self.cache.get_search_cache_key(
                query, time_period, self.use_tor
            )
            self.cache.set(cache_key, result)

        return result

    def get_token(self, status: t.Optional[Status] = None) -> tuple:
        """
        Get the Ahmia homepage and capture the dynamic hidden
        anti-bot token used as additional GET parameters.

        :return: If successful, a tuple of TOKEN_NAME, TOKEN_VALUE, otherwise NONE, NONE
        """
        # Check cache for token first
        if not self.no_cache and self.cache:
            cache_key = self.cache.get_token_cache_key(self.use_tor)
            cached_token = self.cache.get(cache_key)
            if cached_token is not None:
                console.log("[bold #c7ff70]✔[/bold #c7ff70] Token loaded from cache")
                return tuple(cached_token)

        if isinstance(status, Status):
            status.update(
                f"[dim]Capturing session token[/dim][yellow]…[/yellow]"
            )
        try:
            soup = self._get_soup(url="https://ahmia.fi/")
        except ConnectionError:
            return None, None
        except RequestException:
            return None, None

        hidden_input = soup.find("input", {"type": "hidden"})

        if hidden_input is None:
            return None, None

        token_name: t.Optional[str] = hidden_input.get("name")
        token_value: t.Optional[str] = hidden_input.get("value")

        # We only check if token_name and token_value are not None because the tokens come in pairs
        if token_name and token_value is not None:
            console.log(f"[bold #c7ff70]✔[/bold #c7ff70] Token capture successful.")
            # Cache the token with a shorter TTL (10 minutes)
            if not self.no_cache and self.cache:
                cache_key = self.cache.get_token_cache_key(self.use_tor)
                self.cache.set(cache_key, [token_name, token_value], ttl=600)
        else:
            console.log(f"[bold red]✘[/bold red] Token capture failed.")

        return token_name, token_value

    @staticmethod
    def check_updates(status: Status):
        """
        Checks for program (pyahmia) updates.

        :param status: A rich.status.Status object to show a live status message.
        """

        from .. import __pkg__, __version__

        with suppress(RequestException):
            if isinstance(status, Status):
                status.update("[dim]Checking for updates[/dim][yellow]…[/yellow]")

            checker = UpdateChecker()
            check = checker.check(package_name=__pkg__, package_version=__version__)

            if check is not None:
                console.print(f"[bold blue]🡅[/bold blue] {check}")

    def _get_soup(
        self, url: str, params: t.Optional[dict] = None
    ) -> BeautifulSoup:
        response: Response = self.session.get(
            url=url, timeout=self.timeout, params=params, headers={"User-Agent": self.user_agent}
        )
        response.raise_for_status()
        soup: BeautifulSoup = BeautifulSoup(response.content, "html.parser")

        return soup

