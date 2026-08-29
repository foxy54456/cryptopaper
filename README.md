# cryptopaper

`cryptopaper` is a lightweight Bash script that turns current cryptocurrency prices and recent price history into a dynamically generated Linux desktop wallpaper.

It fetches market data from CoinGecko, generates a wallpaper with ImageMagick, detects your screen resolution automatically, and applies the wallpaper using the appropriate backend for your desktop environment.

## Features

* Multiple cryptocurrency support
* Multiple fiat currencies
* Current cryptocurrency price
* Cryptocurrency price chart
* Percentage change for the selected chart range
* Persistent cryptocurrency selection
* Persistent fiat currency selection
* Persistent chart range
* Persistent update interval
* Automatic wallpaper updates
* Configurable update intervals
* Automatic screen resolution detection
* Automatic wallpaper backend detection
* Adaptive price precision
* API caching
* Cached-data fallback when CoinGecko is temporarily unavailable
* Improved cache safety and error handling
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

## Installation

Clone the repository:

```bash
git clone https://github.com/foxy54456/cryptopaper.git
cd cryptopaper
```

Make the script executable:

```bash
chmod +x cryptopaper
```

Create a local bin directory:

```bash
mkdir -p ~/.local/bin
```

Create a symbolic link:

```bash
ln -sf "$PWD/cryptopaper" ~/.local/bin/cryptopaper
```

Now add `~/.local/bin` to your shell PATH.

### Bash

Copy and paste:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

Verify:

```bash
which cryptopaper
```

You should see something similar to:

```text
/home/your-user/.local/bin/cryptopaper
```

### Zsh

Copy and paste:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

Verify:

```bash
which cryptopaper
```

### Fish

Copy and paste:

```fish
fish_add_path ~/.local/bin
```

Verify:

```fish
which cryptopaper
```

## Test the installation

Run:

```bash
cryptopaper help
```

Then close the terminal completely, open a new terminal, and run:

```bash
cryptopaper help
```

If that works, the installation is complete.

Because cryptopaper is installed using a symbolic link, editing the script inside the cloned repository automatically updates the `cryptopaper` command.

## Requirements

Core dependencies:

```text
bash
curl
jq
imagemagick
awk
```

The script also uses common Linux utilities such as:

```text
find
sort
head
stat
timeout
pgrep
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

Change the active cryptocurrency with:

```bash
cryptopaper coin btc
cryptopaper coin eth
cryptopaper coin sol
cryptopaper coin doge
cryptopaper coin xmr
cryptopaper coin bnb
cryptopaper coin xrp
```

For example:

```bash
cryptopaper coin eth
```

Ethereum will remain selected until you change it again.

Commands such as:

```bash
cryptopaper price
cryptopaper set
cryptopaper
```

will now use Ethereum.

## Supported currencies

cryptopaper currently supports:

* USD — `$`
* EUR — `€`
* GBP — `£`

The default currency is:

```text
USD
```

Change the active currency with:

```bash
cryptopaper cur USD
cryptopaper cur EUR
cryptopaper cur GBP
```

For example:

```bash
cryptopaper cur EUR
```

The selected currency remains active until you change it again.

Unsupported currencies are rejected.

For example:

```bash
cryptopaper cur CAD
```

will fail because only USD, EUR, and GBP are currently supported.

## Usage

```bash
cryptopaper
cryptopaper [days]
cryptopaper [days] [update-time]

cryptopaper price
cryptopaper set
cryptopaper set [days]

cryptopaper coin btc|eth|sol|doge|xmr|bnb|xrp
cryptopaper cur USD|EUR|GBP
cryptopaper range <days>
cryptopaper interval <time>

cryptopaper info
cryptopaper cache
cryptopaper clear-cache
cryptopaper help
```

## Persistent settings

cryptopaper remembers:

* Active cryptocurrency
* Active fiat currency
* Chart range
* Update interval

These settings are stored in:

```text
~/.config/cryptopaper/config
```

For example:

```text
coin=eth
currency=EUR
range=3d
interval=45s
```

On a fresh installation, the defaults are:

```text
coin=btc
currency=USD
range=1d
interval=2m
```

Once your settings are configured, simply run:

```bash
cryptopaper
```

cryptopaper will start the automatic wallpaper updater using the saved settings.

## Automatic updates

Start cryptopaper using the currently saved settings:

```bash
cryptopaper
```

For example, if your saved configuration is:

```text
coin=eth
currency=EUR
range=3d
interval=45s
```

then:

```bash
cryptopaper
```

starts the Ethereum wallpaper updater in EUR using a 3-day chart and updating every 45 seconds.

You can also set the range and interval while starting cryptopaper:

```bash
cryptopaper 3d 45s
```

This saves:

```text
range=3d
interval=45s
```

and immediately starts the updater.

The next time you run:

```bash
cryptopaper
```

those saved values are used automatically.

You can also provide only the chart range:

```bash
cryptopaper 7d
```

This saves:

```text
range=7d
```

while keeping your previously saved update interval, then starts the updater.

Press:

```text
Ctrl+C
```

to stop automatic updates.

## Refresh interval

Update intervals use one of the following units:

```text
s = seconds
m = minutes
h = hours
```

Examples:

```bash
cryptopaper interval 30s
cryptopaper interval 2m
cryptopaper interval 10m
cryptopaper interval 1h
```

You can also set the interval while starting cryptopaper:

```bash
cryptopaper 1d 30s
```

Very short update intervals are supported.

However, CoinGecko may return the same price for multiple requests, so a short interval does not guarantee that the displayed price will change every update.

Frequent requests may also trigger CoinGecko API rate limits.

The default update interval is:

```text
2m
```

## Show the current price

Show the current price of the selected cryptocurrency:

```bash
cryptopaper price
```

Example:

```text
BITCOIN: $79308.00
```

If Ethereum and EUR are selected:

```bash
cryptopaper coin eth
cryptopaper cur EUR
cryptopaper price
```

you may see something like:

```text
ETHEREUM: €2310.42
```

## Set the wallpaper once

Generate and set the wallpaper once using the currently saved settings:

```bash
cryptopaper set
```

Use a one-time chart range:

```bash
cryptopaper set 7d
```

Other examples:

```bash
cryptopaper set 1d
cryptopaper set 3d
cryptopaper set 16d
cryptopaper set 30d
```

This does not start the automatic update loop.

## Change cryptocurrency

Set the persistent cryptocurrency:

```bash
cryptopaper coin eth
```

Other examples:

```bash
cryptopaper coin btc
cryptopaper coin sol
cryptopaper coin doge
cryptopaper coin xmr
cryptopaper coin bnb
cryptopaper coin xrp
```

The selected cryptocurrency is used by:

```bash
cryptopaper price
cryptopaper set
cryptopaper
```

until you change it again.

## Change currency

Set the persistent fiat currency:

```bash
cryptopaper cur EUR
```

Other examples:

```bash
cryptopaper cur USD
cryptopaper cur GBP
```

The selected currency is used for both the current price and chart data.

## Change chart range

Set the persistent chart range:

```bash
cryptopaper range 7d
```

Other examples:

```bash
cryptopaper range 1d
cryptopaper range 3d
cryptopaper range 16d
cryptopaper range 30d
cryptopaper range 90d
```

Chart ranges use this format:

```text
<number>d
```

Any positive number of days can be used.

The default range is:

```text
1d
```

## Change update interval

Set the persistent update interval:

```bash
cryptopaper interval 45s
```

Other examples:

```bash
cryptopaper interval 30s
cryptopaper interval 2m
cryptopaper interval 10m
cryptopaper interval 1h
```

The default interval is:

```text
2m
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

## System information

Show the current configuration and detected system information:

```bash
cryptopaper info
```

This includes information such as:

* Screen resolution
* Desktop environment
* Session type
* Wallpaper backend
* Active cryptocurrency
* Active currency
* Saved chart range
* Saved update interval

Example:

```text
Resolution: 1920x1080
Desktop: KDE
Session: wayland
Wallpaper backend: KDE Plasma
Coin: ETHEREUM (eth)
Currency: EUR (€)
Saved range: 3d
Saved interval: 45s
```

## Cache

cryptopaper caches CoinGecko API responses to avoid unnecessary requests and provide fallback data when the API is temporarily unavailable.

View cached data:

```bash
cryptopaper cache
```

Clear cached API data:

```bash
cryptopaper clear-cache
```

Cache files are separated by:

* Cryptocurrency
* Fiat currency
* Chart range

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

For example, Bitcoin in USD and Bitcoin in EUR use separate cache files:

```text
btc-market-usd.json
btc-market-eur.json
```

The same applies to chart data:

```text
btc-chart-7d-usd.json
btc-chart-7d-eur.json
```

Changing cryptocurrency or currency therefore cannot accidentally reuse cached data from another selection.

Generated wallpapers are also stored under:

```text
~/.cache/cryptopaper/
```

## Configuration

Persistent settings are stored in:

```text
~/.config/cryptopaper/config
```

Example:

```text
coin=eth
currency=EUR
range=3d
interval=45s
```

These settings remain active after closing the terminal, restarting cryptopaper, logging out, or rebooting.

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

For testing, the resolution can be overridden:

```bash
CRYPTOPAPER_RESOLUTION=2560x1440 cryptopaper set
```

Other examples:

```bash
CRYPTOPAPER_RESOLUTION=3840x2160 cryptopaper set 7d
CRYPTOPAPER_RESOLUTION=3440x1440 cryptopaper set 30d
CRYPTOPAPER_RESOLUTION=1366x768 cryptopaper set
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

The wallpaper backend is selected based on the currently running desktop environment and session rather than simply using whichever wallpaper utility happens to be installed.

## swaybg process handling

When cryptopaper uses `swaybg`, it creates:

```text
swaybg.pid
```

`swaybg` must remain running to keep the wallpaper visible.

cryptopaper records the process ID of the `swaybg` instance it started so that the next update can replace only its own previous process.

Before stopping the saved process, cryptopaper verifies that the process is actually `swaybg`.

Other desktop backends do not require this because the desktop environment manages the wallpaper itself.

## XFCE

Fresh XFCE profiles may initially have no wallpaper configuration properties.

cryptopaper attempts to detect existing XFCE wallpaper properties and can initialize the required wallpaper property when necessary.

When possible, it also attempts to detect the current XFCE workspace before creating a new wallpaper property.

## Examples

### Bitcoin in USD with defaults

Set the default configuration:

```bash
cryptopaper coin btc
cryptopaper cur USD
cryptopaper range 1d
cryptopaper interval 2m
```

Start cryptopaper:

```bash
cryptopaper
```

### Ethereum in EUR

```bash
cryptopaper coin eth
cryptopaper cur EUR
```

Show the current price:

```bash
cryptopaper price
```

Set the wallpaper once:

```bash
cryptopaper set
```

Start automatic updates:

```bash
cryptopaper
```

### 3-day chart updating every 45 seconds

Set each option separately:

```bash
cryptopaper range 3d
cryptopaper interval 45s
cryptopaper
```

Or configure both while starting:

```bash
cryptopaper 3d 45s
```

### Change only the range while starting

```bash
cryptopaper 7d
```

This saves the 7-day range, keeps your existing interval, and starts cryptopaper.

### Dogecoin wallpaper

```bash
cryptopaper coin doge
cryptopaper set 7d
```

### Monero in GBP

```bash
cryptopaper coin xmr
cryptopaper cur GBP
cryptopaper range 30d
cryptopaper interval 5m
cryptopaper
```

### Switch back to defaults

```bash
cryptopaper coin btc
cryptopaper cur USD
cryptopaper range 1d
cryptopaper interval 2m
```

### Show current settings

```bash
cryptopaper info
```

### Show cached data

```bash
cryptopaper cache
```

### Clear cached API data

```bash
cryptopaper clear-cache
```

## Data source

Cryptocurrency pricing and chart data are retrieved from the CoinGecko API.

cryptopaper uses separate requests for:

* Current cryptocurrency price
* Historical chart data

This keeps the displayed current price independent from the selected chart range.

The selected fiat currency is sent directly to CoinGecko, so USD, EUR, and GBP prices and charts use CoinGecko's corresponding market data.

CoinGecko's public API may rate-limit clients making many requests in a short period of time.

cryptopaper uses caching to reduce unnecessary API requests and can fall back to previously cached data when the API is temporarily unavailable.

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

## Current limitations

* Supported cryptocurrencies are currently limited to `btc`, `eth`, `sol`, `doge`, `xmr`, `bnb`, and `xrp`
* Supported fiat currencies are currently limited to USD, EUR, and GBP
* Multi-monitor support is still limited
* Not every Linux desktop environment or window manager has been tested
* Some Wayland compositors require an external wallpaper tool such as `swaybg` or `swww`
* The automatic updater currently runs in the foreground
* No systemd/background service mode yet

## License

This project is released into the public domain under The Unlicense.

See the [LICENSE](LICENSE) file for details.
