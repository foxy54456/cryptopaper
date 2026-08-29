# cryptopaper

`cryptopaper` is a lightweight Bash script that turns current cryptocurrency prices and recent price history into a dynamically generated Linux desktop wallpaper.

It fetches market data from CoinGecko, generates a wallpaper with ImageMagick, detects your screen resolution automatically, and applies the wallpaper using the appropriate backend for your desktop environment.

cryptopaper also includes an optional GTK4 GUI. The GUI is a frontend for the Bash CLI, so the CLI remains fully usable without Python or GTK.

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
* Optional GTK4 GUI
* GUI controls for coin, currency, chart range, and update interval
* GUI current-price display
* Live GUI price updates while automatic updates are running
* GUI-managed automatic updater
* System tray support through StatusNotifierItem
* Tray icon can reopen the hidden GUI window
* Automatic updater stops when GUI settings are changed
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

Make the CLI and GUI scripts executable:

```bash
chmod +x cryptopaper
chmod +x cryptopaper-gui.py
```

Create a local bin directory:

```bash
mkdir -p ~/.local/bin
```

Create symbolic links for the CLI and GUI:

```bash
ln -sf "$PWD/cryptopaper" ~/.local/bin/cryptopaper
ln -sf "$PWD/cryptopaper-gui.py" ~/.local/bin/cryptopaper-gui
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

If that works, the CLI installation is complete.

If you installed the optional GUI dependencies, you can also verify the GUI command:

```bash
which cryptopaper-gui
cryptopaper-gui
```

Because cryptopaper is installed using symbolic links, editing either script inside the cloned repository automatically updates the corresponding command.

The GUI depends on the CLI command being available in your `PATH`.

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

## GUI requirements

The GUI is optional.

The Bash CLI does **not** require Python, GTK, or PyGObject.

To use the GUI, you need:

```text
python3
GTK4
PyGObject
GLib / Gio
GObject Introspection
```

Package names differ between Linux distributions. On Debian/Ubuntu-based systems, packages may have names similar to:

```text
python3-gi
gir1.2-gtk-4.0
```

On Arch-based systems, packages may have names similar to:

```text
python-gobject
gtk4
```

### NixOS / Home Manager example

A Home Manager package list can include:

```nix
home.packages = with pkgs; [
  gtk4
  pango
  harfbuzz
  cairo
  gdk-pixbuf
  glib
  graphene
  gobject-introspection
  pkg-config

  (python312.withPackages (ps: with ps; [
    pygobject3
  ]))
];
```

Depending on your NixOS setup, GObject Introspection typelibs may also need to be available through `GI_TYPELIB_PATH`.

The GUI uses GTK4 directly. It does not require GTK3 or AppIndicator libraries.

## GUI

Launch the graphical interface with:

```bash
cryptopaper-gui
```

Or run it directly from the cloned repository:

```bash
./cryptopaper-gui.py
```

The GUI controls the same settings and Bash commands used by the CLI.

It does not contain a second wallpaper generator or a separate CoinGecko implementation. The Bash `cryptopaper` command remains the main backend.

### GUI controls

The GUI currently provides controls for:

* Cryptocurrency
* Fiat currency
* Chart range
* Update interval
* Current price
* Set Wallpaper
* Start Auto Update
* Stop
* Refresh Price
* Quit Application

The default GUI selections are:

```text
coin=btc
currency=USD
range=1d
interval=2m
```

The GUI reads the same persistent configuration file as the CLI:

```text
~/.config/cryptopaper/config
```

Changing a GUI dropdown saves the new setting through the CLI.

### GUI chart ranges

The GUI currently exposes these chart-range choices:

```text
1d
3d
7d
14d
16d
30d
90d
```

The CLI still accepts any valid positive day range supported by the script.

If the saved CLI range is not one of the GUI choices, the GUI falls back to its default `1d` selection.

### GUI update intervals

The GUI currently exposes these update intervals:

```text
15s
30s
45s
1m
2m
5m
10m
30m
1h
```

The CLI remains more flexible and can accept other valid interval values.

If the saved CLI interval is not one of the GUI choices, the GUI falls back to its default `2m` selection.

### Set Wallpaper

Pressing **Set Wallpaper** saves the currently selected GUI settings and runs:

```bash
cryptopaper set
```

The wallpaper generation and desktop-backend detection are still handled by the Bash CLI.

### Automatic updates from the GUI

Pressing **Start Auto Update** launches the normal CLI auto-update loop:

```bash
cryptopaper
```

The updater runs as a separate process managed by the GUI.

The GUI can remain open while it runs, or the window can be hidden to the system tray when tray support is available.

Press **Stop** to stop the GUI-managed automatic updater.

### Changing settings while auto-update is running

If automatic updates are currently running and you change any of these GUI settings:

* Cryptocurrency
* Currency
* Chart range
* Update interval

the running updater is stopped before the new configuration is used.

The GUI displays:

```text
Automatic updates stopped because settings changed.
```

This prevents an old updater process from continuing with settings that no longer match what the GUI displays.

Press **Start Auto Update** again to start the updater with the new settings.

### Live GUI price updates

While automatic updates are running, the Bash CLI updates its normal cached market-price file.

The GUI watches the selected coin/currency market cache and updates the **Current Price** label when that cache changes.

For example:

```text
~/.cache/cryptopaper/btc-market-usd.json
~/.cache/cryptopaper/eth-market-eur.json
```

The cache watcher checks the local file only. It does not make an additional CoinGecko request merely to update the GUI label.

The **Refresh Price** button remains available for a manual price refresh.

### System tray

The GUI implements a StatusNotifierItem tray icon through D-Bus.

On desktops and panels with StatusNotifierItem support, closing the main window hides cryptopaper instead of fully exiting it.

Click the tray icon to reopen the GUI.

The automatic updater can continue running while the window is hidden.

Use **Quit Application** to fully exit the GUI and stop the automatic updater that the GUI started.

If no compatible tray host is available, closing the window exits the GUI rather than leaving an invisible background process running.

KDE Plasma supports StatusNotifierItem natively. Other desktop environments may require panel support or an extension for tray icons.

### GUI icon

The project icon is stored at:

```text
assets/icon.png
```

For local development, it can be installed into the user's hicolor icon theme:

```bash
mkdir -p ~/.local/share/icons/hicolor/256x256/apps

cp assets/icon.png \
  ~/.local/share/icons/hicolor/256x256/apps/cryptopaper.png

gtk-update-icon-cache ~/.local/share/icons/hicolor
```

The tray icon requests the icon name:

```text
cryptopaper
```

A future packaged installer can perform this icon installation automatically.

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
cryptopaper-gui

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

These settings are shared by both the CLI and GUI and are stored in:

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

to stop automatic updates when running the CLI directly.

When automatic updates are started from the GUI, use the GUI **Stop** button instead.

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

The GUI also uses the existing current-price cache for live display updates while the automatic updater is running. Watching the cache does not itself create another CoinGecko API request.

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

The GTK4 GUI and StatusNotifierItem tray behavior have been tested on KDE Plasma.

Not every Linux desktop environment or window manager has been tested yet, and GUI tray behavior depends on the desktop or panel providing StatusNotifierItem support.

## Current limitations

* Supported cryptocurrencies are currently limited to `btc`, `eth`, `sol`, `doge`, `xmr`, `bnb`, and `xrp`
* Supported fiat currencies are currently limited to USD, EUR, and GBP
* Multi-monitor support is still limited
* Not every Linux desktop environment or window manager has been tested
* Some Wayland compositors require an external wallpaper tool such as `swaybg` or `swww`
* The CLI automatic updater runs in the foreground when started directly from a terminal
* The GUI can manage the updater while its window is hidden to a supported system tray
* No systemd/background service mode yet
* GUI tray behavior depends on StatusNotifierItem support from the desktop environment or panel
* The GTK4 GUI has not yet been tested across every supported desktop environment

## Project structure

```text
cryptopaper/
├── cryptopaper
├── cryptopaper-gui.py
├── assets/
│   └── icon.png
├── README.md
└── LICENSE
```

`cryptopaper` is the main Bash CLI and contains the market-data, wallpaper-generation, caching, configuration, screen-detection, and wallpaper-backend logic.

`cryptopaper-gui.py` is the optional GTK4 frontend. It calls the Bash CLI instead of duplicating the core implementation.

`assets/icon.png` contains the application/tray icon.

## License

This project is released into the public domain under The Unlicense.

See the [LICENSE](LICENSE) file for details.
