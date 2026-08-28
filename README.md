# cryptopaper

A lightweight Bash script that displays the current Bitcoin price and price history as your Linux wallpaper.

## Features

- Current Bitcoin price
- Percentage change for the selected time range
- Green/red price movement graph
- Custom graph ranges such as `1d`, `7d`, `16d`, `30d`, or any other positive number of days
- Local caching to reduce API calls and avoid rate limits
- KDE Plasma wallpaper support
- Lightweight Bash-only implementation

## Dependencies

- Bash
- curl
- jq
- ImageMagick
- awk
- KDE Plasma (`plasma-apply-wallpaperimage`)

### NixOS / Home Manager

```nix
home.packages = with pkgs; [
  curl
  jq
  imagemagick
  gawk
];
```

## Usage

Show the current Bitcoin price:

```bash
./cryptopaper price
```

Generate and set the wallpaper using the default 1-day graph:

```bash
./cryptopaper set
```

Use a custom history range:

```bash
./cryptopaper set 7d
./cryptopaper set 30d
./cryptopaper set 90d
```

Any positive number of days can be used:

```bash
./cryptopaper set 16d
```

The percentage shown on the wallpaper matches the selected graph range.

For example:

```bash
./cryptopaper set 7d
```

will show:

- a 7-day Bitcoin price graph
- the percentage change over that same 7-day period

## Caching

Cryptopaper stores API data in:

```text
~/.cache/cryptopaper/
```

Current price data is refreshed every 2 minutes.

Historical chart data is refreshed every 5 minutes.

If CoinGecko is temporarily unavailable or rate-limited, Cryptopaper will reuse cached data when possible.

## Current Limitations

- Only Bitcoin/USD is supported
- Wallpaper setting currently supports KDE Plasma only
- Wallpaper output is currently fixed at 1920x1080

## Data

Price and historical market data are fetched from the CoinGecko API.

## Status

Early development.
