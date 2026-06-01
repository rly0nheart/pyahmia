import csv
import typing as t
from pathlib import Path

from rich.console import Console, Group
from rich.panel import Panel
from rich.rule import Rule

from . import __version__

console = Console(log_time=False)

__all__ = [
    "print_banner",
    "print_results",
    "export_csv",
    "console",
]


def print_banner(tor_mode: bool):
    console.print(
        f"""[bold]{"[red]" if tor_mode else "[#c7ff70]"}
 ▗▄▖ ▐▌   ▄▄▄▄  ▄ ▗▞▀▜▌
▐▌ ▐▌▐▌   █ █ █ ▄ ▝▚▄▟▌
▐▛▀▜▌▐▛▀▚▖█   █ █      
▐▌ ▐▌▐▌ ▐▌      █[/bold].{"onion" if tor_mode else "fi"}{"[/red]" if tor_mode else "[/]"} {__version__}
"""
    )


def print_results(search: dict, limit: int, show_all: bool = False):
    """
    Print search results to console.

    :param search: Search response object from ahmia.search
    :param limit: Maximum number of results to display
    :param show_all: Override the limit parameter and display all results
    """

    is_success = search["success"]

    if is_success:
        all_results: list = search["results"]
        sliced_results: list = all_results[:limit]

        results: list = all_results if show_all else sliced_results

        if show_all:
            console.log(f"[bold #c7ff70]✔[/bold #c7ff70] {search['message']}\n")
        else:
            console.log(f"[bold blue]*[/bold blue] Displaying {len(sliced_results)} of {len(all_results)} results.\n")

        with console.pager(styles=True):
            for index, result in enumerate(results, start=1):
                title = result["title"]
                about = result["about"]
                url = result["url"]
                last_seen = result["last_seen_rel"]

                # ----------------------------------------------------------------------- #
                content_items = [
                    # f"[bold][#c7ff70]{title}[/][/bold]",
                    # Rule(style="#444444"),
                    about,
                    f"[blue][link=http://{url}]{url}[/link][/blue]",
                    Rule(style="#444444"),
                    f"[italic]last seen[/italic], {last_seen}"
                ]
                console.print(
                    Panel(
                        Group(*content_items),
                        highlight=True,
                        border_style="dim #c7ff70",
                        title_align="left",
                        title=f"[italic]{title}[/italic]",
                    )
                )
                # ----------------------------------------------------------------------- #
    else:
        console.log(f"[bold yellow]✘[/bold yellow] {search['message']}")

def export_csv(results: t.Iterable[dict], path: str) -> str:
    """
    Exports search results to a csv file.

    :param results: A list of SimpleNamespace objects, each representing a search result.
    :param path: A path name/filename to which the results will be exported.
    :return: The pathname to the exported results file.
    """

    results_list = list(results)

    if not all(isinstance(item, dict) for item in results_list):
        raise TypeError(
            "export_csv expects an iterable of dict objects (e.g., result of Ahmia.search())"
        )

    dict_rows = [item for item in results_list]

    if not dict_rows:
        raise ValueError("No results to export")

    out: Path = Path().home() / "pyahmia" / f"{path}.csv"
    out.parent.mkdir(parents=True, exist_ok=True)

    with out.open(mode="w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=dict_rows[0].keys())
        writer.writeheader()
        writer.writerows(dict_rows)

    return str(out)
