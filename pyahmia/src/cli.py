import argparse
import time

from rich.status import Status

from . import __pkg__, __version__
from .api import Ahmia
from .lib import console, print_results, export_csv, print_banner


def create_parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog=__pkg__,
        description="Search hidden services on the Tor network.",
    )
    parser.add_argument("query", type=str, help="Search query")
    parser.add_argument(
        "-a",
        "--all",
        action="store_true",
        help="Override --limit and show all results",
    )
    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="Disable response caching",
    )
    parser.add_argument(

        "--timeout",
        type=int,
        default=10,
        help="Response timeout in seconds (default: %(default)s)",
    )
    parser.add_argument(
        "-t",
        "--use-tor",
        action="store_true",
        help="Route traffic through the Tor network",
    )
    parser.add_argument(
        "-l",
        "--limit",
        type=int,
        default=100,
        help="Maximum number of results to display (defaults to %(default)s)",
    )
    parser.add_argument(
        "-e",
        "--export",
        action="store_true",
        help="Export the output to a file",
    )
    parser.add_argument(
        "-p",
        "--period",
        type=str,
        choices=["day", "week", "month", "all"],
        default="all",
        help="Show results from a specified time period (default: all)",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"{__pkg__} {__version__}, by Ritchie Mwewa",
    )

    return parser.parse_args()


def cli():
    """
    Search hidden services on the Tor network.
    """

    args = create_parser()

    console.set_window_title(f"{__pkg__}, {__version__}")
    now: float = time.time()
    try:
        print_banner(tor_mode=args.use_tor)

        ahmia = Ahmia(
            user_agent=f"{__pkg__}/{__version__}; +https://codeberg.org/rly0nheart/{__pkg__}",
            use_tor=args.use_tor, no_cache=args.no_cache, timeout=args.timeout,
        )

        with Status(
            "[dim]Initialising[/dim][yellow]…[/yellow]", console=console
        ) as status:
            ahmia.check_updates(status=status)
            search = ahmia.search(
                query=args.query, time_period=args.period, status=status
            )

        print_results(search=search, limit=args.limit, show_all=args.all)

        if args.export and (search.get("results") is not None):
            outfile: str = export_csv(results=search.get("results"), path=args.query)
            console.log(
                f"[bold #c7ff70]🖫[/bold #c7ff70] {search['total_count']} results exported: [link file://{outfile}]{outfile}"
            )


    except KeyboardInterrupt:
        console.log("\n[bold yellow]✘[/bold yellow] User interruption detected ([bold yellow]CTRL+C[/bold yellow])")
    except OSError as e:
        console.log(f"[bold red]✘[/bold red] An error occurred:  {e}")
    finally:
        elapsed: float = time.time() - now
        console.log(f"[bold #c7ff70]✔[/bold #c7ff70] Finished in {elapsed:.2f} seconds.")
