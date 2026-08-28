# cryptopaper

A lightweight Bash script that displays the current Bitcoin price and price history as your Linux wallpaper.

## Features

- Current Bitcoin price
- Percentage change for the selected time range
- Green/red price movement graph
- Custom graph ranges such as `1d`, `7d`, `16d`, `30d`, or any other positive number of days
- Automatic wallpaper updates with the `run` command
- Custom refresh intervals such as `30s`, `2m`, `10m`, or `1h`
- Separate price and chart caching to reduce API calls and avoid rate limits
- Cached-data fallback when the API is temporarily unavailable
- KDE Plasma wallpaper support
- Lightweight Bash implementation

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

Show help:

```bash
./cryptopaper help
```

Show the current Bitcoin price:

```bash
./cryptopaper price
```

Generate and set the wallpaper once using the default 1-day graph:

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

### Automatic updates

Keep the wallpaper updated automatically:

```bash
./cryptopaper run
```

By default, this uses a 1-day graph and refreshes every 2 minutes.

Use a custom graph range:

```bash
./cryptopaper run 7d
```

Use a custom refresh interval:

```bash
./cryptopaper run 1d 30s
./cryptopaper run 7d 5m
./cryptopaper run 30d 10m
./cryptopaper run 90d 1h
```

Supported refresh units:

- `s` — seconds
- `m` — minutes
- `h` — hours

For example:

```bash
./cryptopaper run 7d 5m
```

uses a 7-day graph and refreshes the wallpaper every 5 minutes.

Press `Ctrl+C` to stop automatic updates.

## Caching

Cryptopaper stores API data in:

```text
~/.cache/cryptopaper/
```

It keeps separate cached data for:

- the current Bitcoin price
- historical chart data for each selected range

For example:

```text
market.json
chart-1d.json
chart-7d.json
chart-30d.json
```

Caching reduces unnecessary API requests and helps avoid CoinGecko rate limits.

When using:

```bash
./cryptopaper run
```

the default refresh interval is 2 minutes.

A custom refresh interval can also be used:

```bash
./cryptopaper run 1d 30s
./cryptopaper run 7d 5m
./cryptopaper run 30d 10m
```

While `run` is active, cached price and chart data are refreshed according to the selected update interval.

If CoinGecko is temporarily unavailable or rate-limited, Cryptopaper will reuse the most recent cached data when possible.

## Current Limitations

- Only Bitcoin/USD is supported
- Wallpaper setting currently supports KDE Plasma only
- Wallpaper output is currently fixed at 1920x1080

## Data

Price and historical market data are fetched from the CoinGecko API.

## Status

Early development.
