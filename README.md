# cryptopaper

`cryptopaper` is a Bash script that turns the current Bitcoin price and recent price history into a dynamically generated desktop wallpaper.

It fetches Bitcoin market data from CoinGecko, generates a wallpaper with ImageMagick, detects your screen resolution automatically, and applies the wallpaper using the appropriate backend for your desktop environment.

## Features

* Current Bitcoin price
* Bitcoin price chart
* Configurable chart range
* Automatic wallpaper updates
* Automatic screen resolution detection
* Persistent currency selection
* API caching
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

## Supported currencies

cryptopaper currently supports:

* USD — `$`
* EUR — `€`
* GBP — `£`

The default currency is:

```bash
USD
```

Your selected currency is saved permanently until you change it again.

## Requirements

Core dependencies:

```bash
curl
jq
imagemagick
```

On many distributions, the ImageMagick executable used by cryptopaper is:

```bash
magick
```

You also need a supported wallpaper backend for your desktop environment.

### KDE Plasma

```bash
plasma-apply-wallpaperimage
kscreen-doctor
```

### GNOME

```bash
gsettings
```

### Cinnamon

```bash
gsettings
```

### MATE

```bash
gsettings
```

### XFCE

```bash
xfconf-query
```

### LXQt

```bash
pcmanfm-qt
```

### Hyprland

At least one of:

```bash
hyprpaper
swww
swaybg
```

### Sway

At least one of:

```bash
swaybg
swww
```

### Generic X11

```bash
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

Run:

```bash
./cryptopaper help
```

## Usage

```bash
./cryptopaper price
./cryptopaper set [days]
./cryptopaper run [days] [update-time]
./cryptopaper cur USD|EUR|GBP
./cryptopaper info
./cryptopaper cache
./cryptopaper clear-cache
```

## Commands

### Show the current Bitcoin price

```bash
./cryptopaper price
```

Example:

```text
Bitcoin: $123456.78
```

The displayed currency depends on your currently selected currency.

---

### Generate and set the wallpaper once

```bash
./cryptopaper set
```

Use a custom chart range:

```bash
./cryptopaper set 7d
```

Other examples:

```bash
./cryptopaper set 1d
./cryptopaper set 16d
./cryptopaper set 30d
```

---

### Automatically update the wallpaper

```bash
./cryptopaper run
```

The default update interval is:

```text
2 minutes
```

Use a custom range:

```bash
./cryptopaper run 7d
```

Use a custom range and update interval:

```bash
./cryptopaper run 1d 30s
./cryptopaper run 7d 5m
./cryptopaper run 30d 1h
```

Press:

```text
Ctrl+C
```

to stop automatic updates.

## Currency

Change the active currency with:

```bash
./cryptopaper cur USD
./cryptopaper cur EUR
./cryptopaper cur GBP
```

For example:

```bash
./cryptopaper cur EUR
```

cryptopaper will then use EUR for both the current Bitcoin price and chart data.

The selected currency persists across future runs until you change it again.

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

```bash
1d
7d
16d
30d
```

The default chart range is:

```text
1d
```

## Update intervals

Automatic update intervals support:

```text
s = seconds
m = minutes
h = hours
```

Examples:

```bash
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

## Cache

cryptopaper caches CoinGecko API responses to avoid unnecessary requests.

View cache information:

```bash
./cryptopaper cache
```

Clear cached API data:

```bash
./cryptopaper clear-cache
```

Chart data is kept separate for different ranges and currencies so data from one currency is not accidentally reused for another.

Changing the active currency also prevents stale data from the previous currency being displayed.

## Screen resolution

cryptopaper automatically attempts to detect your active screen resolution.

It supports detection through tools including:

* `kscreen-doctor`
* `hyprctl`
* `swaymsg`
* `xrandr`
* `xdpyinfo`

If detection fails, cryptopaper falls back to:

```text
1920x1080
```

For testing, the resolution can also be overridden:

```bash
CRYPTOPAPER_RESOLUTION=2560x1440 ./cryptopaper set
```

## Wallpaper backends

cryptopaper automatically selects a wallpaper backend based on the current desktop environment.

Supported backends include:

| Environment     | Backend                          |
| --------------- | -------------------------------- |
| KDE Plasma      | `plasma-apply-wallpaperimage`    |
| GNOME           | `gsettings`                      |
| Cinnamon        | `gsettings`                      |
| MATE            | `gsettings`                      |
| XFCE            | `xfconf-query`                   |
| LXQt            | `pcmanfm-qt`                     |
| Hyprland        | `hyprpaper`, `swww`, or `swaybg` |
| Sway            | `swaybg` or `swww`               |
| Generic Wayland | `swww` or `swaybg`               |
| Generic X11     | `feh`                            |

## Examples

Show the current price:

```bash
./cryptopaper price
```

Use euros:

```bash
./cryptopaper cur EUR
./cryptopaper price
```

Generate a one-day wallpaper:

```bash
./cryptopaper set 1d
```

Generate a seven-day wallpaper:

```bash
./cryptopaper set 7d
```

Continuously update every 30 seconds:

```bash
./cryptopaper run 1d 30s
```

Use GBP and update a seven-day chart every five minutes:

```bash
./cryptopaper cur GBP
./cryptopaper run 7d 5m
```

Show detected system information:

```bash
./cryptopaper info
```

Clear the API cache:

```bash
./cryptopaper clear-cache
```

## Data source

Bitcoin pricing and chart data are retrieved from the CoinGecko API.
