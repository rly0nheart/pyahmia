# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.11.1] - 2026-02-04

### Added

- `-a/--all` option to override limit and show all results
- `--no-cache` option to disable response caching
- `--timeout` option to set response timeout in seconds
- `-l/--limit` option to set maximum number of results to display

### Changed

- Renamed `enable_cache` parameter to `no_cache` (inverted logic)
- CI workflow to auto-publish on push to master

## [0.11.0] - 2026-01-15

### Changed

- Replaced rich-click with argparse for CLI
- Migrated from Poetry to UV for dependency management
- Added Makefile for common tasks
- Added caching for search results

### Removed

- rich-click dependency

## [0.8.0] - 2025-12-01

### Changed

- Migrated repository from GitHub to Codeberg

## [0.7.3] - 2025-11-28

### Fixed

- Issue #9

### Changed

- Bumped brotli from 1.1.0 to 1.2.0

## [0.7.2] - 2025-09-30

### Fixed

- Minor bug fixes

## [0.7.1] - 2025-09-30

### Added

- Tor installation scripts
- Dockerfile for containerized usage

## [0.7.0] - 2025-09-30

### Fixed

- Improved handling of empty results

## [0.6.1] - 2025-09-29

### Changed

- Added color to result panel

## [0.6.0] - 2025-09-29

### Added

- Banner display
- Code refactoring

## [0.5.1] - 2025-09-28

### Fixed

- Minor changes

## [0.5.0] - 2025-09-28

### Added

- `-p, --period` option for time-based filtering

### Removed

- `-l, --limit` option

## [0.4.0] - 2025-09-28

### Changed

- Version bump with improvements

## [0.3.1] - 2025-09-28

### Fixed

- Minor changes

## [0.3.0] - 2025-09-28

### Changed

- Minor changes

## [0.2.0] - 2025-09-28

### Changed

- Minor changes and improvements

## [0.1.2] - 2025-09-28

### Fixed

- ImportError fix

## [0.1.1] - 2025-09-28

### Fixed

- ImportError fix

## [0.1.0] - 2025-09-28

### Added

- Initial release
- CSV export using csv module
- Results displayed in panels instead of table
- Console output instead of logging

[Unreleased]: https://codeberg.org/rly0nheart/pyahmia/compare/0.11.1...HEAD

[0.11.1]: https://codeberg.org/rly0nheart/pyahmia/compare/0.11.0...0.11.1

[0.11.0]: https://codeberg.org/rly0nheart/pyahmia/compare/0.8.0...0.11.0

[0.8.0]: https://codeberg.org/rly0nheart/pyahmia/compare/0.7.3...0.8.0

[0.7.3]: https://codeberg.org/rly0nheart/pyahmia/compare/0.7.2...0.7.3

[0.7.2]: https://codeberg.org/rly0nheart/pyahmia/compare/0.7.1...0.7.2

[0.7.1]: https://codeberg.org/rly0nheart/pyahmia/compare/0.7.0...0.7.1

[0.7.0]: https://codeberg.org/rly0nheart/pyahmia/compare/0.6.1...0.7.0

[0.6.1]: https://codeberg.org/rly0nheart/pyahmia/compare/0.6.0...0.6.1

[0.6.0]: https://codeberg.org/rly0nheart/pyahmia/compare/0.5.1...0.6.0

[0.5.1]: https://codeberg.org/rly0nheart/pyahmia/compare/0.5.0...0.5.1

[0.5.0]: https://codeberg.org/rly0nheart/pyahmia/compare/0.4.0...0.5.0

[0.4.0]: https://codeberg.org/rly0nheart/pyahmia/compare/0.3.1...0.4.0

[0.3.1]: https://codeberg.org/rly0nheart/pyahmia/compare/0.3.0...0.3.1

[0.3.0]: https://codeberg.org/rly0nheart/pyahmia/compare/0.2.0...0.3.0

[0.2.0]: https://codeberg.org/rly0nheart/pyahmia/compare/0.1.2...0.2.0

[0.1.2]: https://codeberg.org/rly0nheart/pyahmia/compare/0.1.1...0.1.2

[0.1.1]: https://codeberg.org/rly0nheart/pyahmia/compare/0.1.0...0.1.1

[0.1.0]: https://codeberg.org/rly0nheart/pyahmia/releases/tag/0.1.0