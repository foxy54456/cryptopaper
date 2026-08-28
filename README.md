# cryptopaper

`cryptopaper` is a lightweight Bash script that turns current cryptocurrency prices and recent price history into a dynamically generated Linux desktop wallpaper.

It fetches market data from CoinGecko, generates a wallpaper with ImageMagick, detects your screen resolution automatically, and applies the wallpaper using the appropriate backend for your desktop environment.

## Features

* Multiple cryptocurrency support
* Multiple fiat currencies
* Current cryptocurrency price
* Cryptocurrency price chart
* Percentage change for the selected chart range
* Configurable chart range
* Automatic wallpaper updates
* Configurable update intervals
* Automatic screen resolution detection
* Automatic wallpaper backend detection
* Persistent currency selection
* Adaptive price precision
* API caching
* Cached-data fallback when CoinGecko is temporarily unavailable
* KDE Plasma support
* GNOME support
* Cinnamon support
* MATE support
* XFCE support
* LXQt support
* Hyprland support
* Sway support
* Generic Wayland support
* Generic X11 support

## Supported cryptocurrencies

cryptopaper currently supports the following aliases:

| Alias | Cryptocurrency |
| ----- | -------------- |
| `btc` | Bitcoin |
| `eth` | Ethereum |
| `sol` | Solana |
| `doge` | Dogecoin |
| `xmr` | Monero |
| `bnb` | BNB |
| `xrp` | XRP |

Bitcoin is the default cryptocurrency.

For example:

```bash
./cryptopaper price
```

is equivalent to:

```bash
./cryptopaper price btc
```

## Supported currencies

cryptopaper currently supports:

* USD — `$`
* EUR — `€`
* GBP — `£`

The default currency is:

```text
USD
```

Your selected currency is saved permanently until you change it again.

For example:

```bash
./cryptopaper cur EUR
```

changes cryptopaper to euros.

After that:

```bash
./cryptopaper price eth
```

will display the Ethereum price in euros.

To switch back to US dollars:

```bash
./cryptopaper cur USD
```

## Price precision

cryptopaper automatically adjusts price precision depending on the value of the cryptocurrency.

Prices of 100 or more use 2 decimal places:

```text
$79308.00
€2510.67
£469.45
```

Prices from 1 up to 99.99... use 4 decimal places:

```text
$2.1847
```

Prices below 1 use 6 decimal places:

```text
$0.091234
```

This gives lower-priced cryptocurrencies such as Dogecoin and XRP more useful precision.

The same precision rules apply when using EUR or GBP.

## Requirements

Core dependencies:

```text
bash
curl
jq
imagemagick
awk
```

On many distributions, the ImageMagick executable used by cryptopaper is:

```bash
magick
```

You also need a supported wallpaper backend for your desktop environment.

### KDE Plasma

```text
plasma-apply-wallpaperimage
kscreen-doctor
```

### GNOME

```text
gsettings
```

### Cinnamon

```text
gsettings
```

### MATE

```text
gsettings
```

### XFCE

```text
xfconf-query
```

### LXQt

```text
pcmanfm-qt
```

### Hyprland

At least one of:

```text
hyprpaper
swww
swaybg
```

### Sway

At least one of:

```text
swaybg
swww
```

### Generic Wayland

At least one of:

```text
swww
swaybg
```

### Generic X11

```text
feh
```

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd cryptopaper
```

Make the script executable:

```bash
chmod +x cryptopaper
```

Show the help page:

```bash
./cryptopaper help
```

## Usage

```bash
./cryptopaper price [coin]
./cryptopaper set [coin] [days]
./cryptopaper run [coin] [days] [update-time]
./cryptopaper cur USD|EUR|GBP
./cryptopaper info
./cryptopaper cache
./cryptopaper clear-cache
```

## Commands

### Show the current cryptocurrency price

Bitcoin is used by default:

```bash
./cryptopaper price
```

Example:

```text
BITCOIN: $79308.00
```

Specify another cryptocurrency using its alias:

```bash
./cryptopaper price eth
./cryptopaper price sol
./cryptopaper price doge
./cryptopaper price xmr
./cryptopaper price bnb
./cryptopaper price xrp
```

Examples:

```text
ETHEREUM: $2510.67
SOLANA: $105.37
DOGECOIN: $0.091234
MONERO: $469.45
XRP: $2.1847
```

The displayed fiat currency depends on your currently selected currency.

For example:

```bash
./cryptopaper cur EUR
./cryptopaper price eth
```

may display:

```text
ETHEREUM: €2310.42
```

---

### Generate and set the wallpaper once

Use Bitcoin with the default 1-day chart:

```bash
./cryptopaper set
```

Use another cryptocurrency:

```bash
./cryptopaper set eth
```

Use another cryptocurrency with a custom chart range:

```bash
./cryptopaper set eth 7d
./cryptopaper set sol 30d
./cryptopaper set doge 2d
```

Bitcoin-only shorthand is still supported:

```bash
./cryptopaper set 7d
```

This is equivalent to:

```bash
./cryptopaper set btc 7d
```

Other examples:

```bash
./cryptopaper set btc 1d
./cryptopaper set xmr 16d
./cryptopaper set bnb 30d
./cryptopaper set xrp 7d
```

The wallpaper displays:

* Cryptocurrency name
* Current price
* Selected fiat currency
* Percentage change
* Price history graph
* Selected chart range

---

### Automatically update the wallpaper

Start automatic updates using Bitcoin:

```bash
./cryptopaper run
```

The defaults are:

```text
Coin: BTC
Currency: USD
Chart range: 1 day
Update interval: 2 minutes
```

Use another cryptocurrency:

```bash
./cryptopaper run eth
```

Use a custom chart range:

```bash
./cryptopaper run sol 7d
```

Use a custom range and update interval:

```bash
./cryptopaper run btc 1d 30s
./cryptopaper run eth 7d 5m
./cryptopaper run doge 30d 10m
./cryptopaper run xmr 90d 1h
```

Bitcoin-only shorthand is still supported:

```bash
./cryptopaper run 7d 5m
```

which is equivalent to:

```bash
./cryptopaper run btc 7d 5m
```

Press:

```text
Ctrl+C
```

to stop automatic updates.

### Refresh interval note

Very short update intervals are supported.

For example:

```bash
./cryptopaper run doge 1d 15s
```

However, CoinGecko may return the same price for multiple requests, so very short intervals do not guarantee that the displayed price will change every update.

Frequent requests may also trigger CoinGecko API rate limits.

If CoinGecko responds with HTTP `429`, wait briefly before making additional requests.

The default update interval is:

```text
2m
```

## Currency

Change the active fiat currency with:

```bash
./cryptopaper cur USD
./cryptopaper cur EUR
./cryptopaper cur GBP
```

For example:

```bash
./cryptopaper cur EUR
```

cryptopaper will then use EUR for both current cryptocurrency prices and chart data.

The selected currency persists across future runs until you change it again.

For example:

```bash
./cryptopaper cur GBP
./cryptopaper price btc
./cryptopaper set eth 7d
./cryptopaper run sol 30d 5m
```

will use GBP for all three cryptocurrencies.

To switch back to the default:

```bash
./cryptopaper cur USD
```

Unsupported currencies are rejected.

For example:

```bash
./cryptopaper cur CAD
```

will fail because only USD, EUR, and GBP are currently supported.

## Time ranges

Chart ranges use the following format:

```text
<number>d
```

Examples:

```text
1d
7d
16d
30d
90d
```

The default chart range is:

```text
1d
```

Any positive number of days can be used.

Examples:

```bash
./cryptopaper set eth 14d
./cryptopaper set sol 45d
./cryptopaper set xmr 90d
```

## Update intervals

Automatic update intervals support:

```text
s = seconds
m = minutes
h = hours
```

Examples:

```text
30s
2m
10m
1h
```

The default update interval is:

```text
2m
```

## System information

To see what cryptopaper detected:

```bash
./cryptopaper info
```

This shows information such as:

* Screen resolution
* Desktop environment
* Session type
* Wallpaper backend
* Active currency

Example:

```text
cryptopaper info

Resolution: 1920x1080
Desktop: GNOME
Session: wayland
Wallpaper backend: GNOME
Currency: EUR (€)
```

## Cache

cryptopaper caches CoinGecko API responses to avoid unnecessary requests and provide fallback data when the API is temporarily unavailable.

View cache information:

```bash
./cryptopaper cache
```

Clear cached API data:

```bash
./cryptopaper clear-cache
```

Cache files are separated by:

* Cryptocurrency
* Fiat currency
* Chart range

This prevents data from one cryptocurrency or currency from accidentally being reused for another.

Examples:

```text
btc-market-usd.json
btc-chart-1d-usd.json
btc-chart-7d-usd.json

eth-market-eur.json
eth-chart-1d-eur.json
eth-chart-7d-eur.json

sol-market-gbp.json
sol-chart-30d-gbp.json
```

For example, Bitcoin in USD and Bitcoin in EUR have completely separate cache files:

```text
btc-market-usd.json
btc-market-eur.json
```

The same applies to chart data:

```text
btc-chart-7d-usd.json
btc-chart-7d-eur.json
```

Changing the active currency therefore cannot accidentally display cached data from the previous currency.

Generated wallpapers are stored in:

```text
~/.cache/cryptopaper/
```

with names similar to:

```text
wallpaper-1787918370.png
```

## swaybg process file

When cryptopaper uses `swaybg`, it also creates:

```text
swaybg.pid
```

`swaybg` must remain running to keep the wallpaper visible.

cryptopaper records the process ID of the `swaybg` instance it started so that the next update can safely stop and replace only its own previous wallpaper process.

Other desktop backends do not require a PID file because the desktop environment manages the wallpaper itself.

## Configuration

Persistent cryptopaper settings are stored under:

```text
~/.config/cryptopaper/
```

The selected fiat currency is stored in:

```text
~/.config/cryptopaper/config
```

For example:

```text
currency=EUR
```

This allows your currency selection to remain active after closing the terminal, restarting cryptopaper, or logging out.

## Screen resolution

cryptopaper automatically attempts to detect your active screen resolution.

It supports detection through tools including:

* `kscreen-doctor`
* `hyprctl`
* `swaymsg`
* `xrandr`
* `xdpyinfo`

Detected resolutions are validated before being used.

If detection fails, cryptopaper falls back to:

```text
1920x1080
```

The wallpaper layout, text sizes, graph dimensions, and spacing automatically scale to the detected resolution.

For testing, the resolution can also be overridden:

```bash
CRYPTOPAPER_RESOLUTION=2560x1440 ./cryptopaper set
```

Other examples:

```bash
CRYPTOPAPER_RESOLUTION=3840x2160 ./cryptopaper set eth 7d
CRYPTOPAPER_RESOLUTION=3440x1440 ./cryptopaper set sol 30d
CRYPTOPAPER_RESOLUTION=1366x768 ./cryptopaper set doge
```

The override only changes the generated wallpaper size.

It does not change your monitor resolution.

## Wallpaper backends

cryptopaper automatically selects a wallpaper backend based on the current desktop environment and session.

| Environment | Backend |
| ----------- | ------- |
| KDE Plasma | `plasma-apply-wallpaperimage` |
| GNOME | `gsettings` |
| Cinnamon | `gsettings` |
| MATE | `gsettings` |
| XFCE | `xfconf-query` |
| LXQt | `pcmanfm-qt` |
| Hyprland | `hyprpaper`, `swww`, or `swaybg` |
| Sway | `swaybg` or `swww` |
| Generic Wayland | `swww` or `swaybg` |
| Generic X11 | `feh` |

The wallpaper backend is selected based on the currently running desktop environment, not simply on which wallpaper tools happen to be installed.

## Tested environments

cryptopaper has been tested successfully on:

* KDE Plasma
* GNOME
* Cinnamon
* MATE
* XFCE
* LXQt
* Hyprland
* Niri
* i3

Not every Linux desktop environment or window manager has been tested yet.

## XFCE

Fresh XFCE profiles may initially have no wallpaper configuration properties.

cryptopaper attempts to detect existing XFCE wallpaper properties and can initialize the required wallpaper property when necessary.

## Examples

Show the Bitcoin price in the current currency:

```bash
./cryptopaper price
```

Show Ethereum:

```bash
./cryptopaper price eth
```

Show Dogecoin with extra decimal precision:

```bash
./cryptopaper price doge
```

Switch to euros:

```bash
./cryptopaper cur EUR
```

Show Ethereum in euros:

```bash
./cryptopaper price eth
```

Generate an Ethereum seven-day wallpaper in euros:

```bash
./cryptopaper set eth 7d
```

Switch to GBP:

```bash
./cryptopaper cur GBP
```

Generate a Monero 30-day wallpaper in pounds:

```bash
./cryptopaper set xmr 30d
```

Continuously update XRP every two minutes:

```bash
./cryptopaper run xrp 1d 2m
```

Switch back to USD:

```bash
./cryptopaper cur USD
```

Generate a Bitcoin one-day wallpaper:

```bash
./cryptopaper set btc 1d
```

Generate a Solana 30-day wallpaper:

```bash
./cryptopaper set sol 30d
```

Continuously update Dogecoin every 30 seconds:

```bash
./cryptopaper run doge 1d 30s
```

Show detected system information:

```bash
./cryptopaper info
```

View the cache:

```bash
./cryptopaper cache
```

Clear the API cache:

```bash
./cryptopaper clear-cache
```

## Data source

Cryptocurrency pricing and chart data are retrieved from the CoinGecko API.

cryptopaper uses separate requests for:

* Current cryptocurrency price
* Historical chart data

This keeps the displayed current price independent from the selected chart range.

The selected fiat currency is sent directly to CoinGecko, so USD, EUR, and GBP prices and charts use CoinGecko's corresponding market data.

## Current limitations

* Supported cryptocurrencies are currently limited to `btc`, `eth`, `sol`, `doge`, `xmr`, `bnb`, and `xrp`
* Supported fiat currencies are currently limited to USD, EUR, and GBP
* Multi-monitor support is still limited
* Not every Linux desktop environment or window manager has been tested
* Some Wayland compositors require an external wallpaper tool such as `swaybg` or `swww`
* `run` currently runs in the foreground
* No systemd/background service mode yet

## License

This project is released into the public domain under The Unlicense.

See the [LICENSE](LICENSE) file for details.
