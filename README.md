# cryptopaper

A lightweight Bash script that displays the current Bitcoin price and price history as your Linux wallpaper.

## Features

- Current Bitcoin price
- Percentage change for the selected time range
- Green/red price movement graph
- Custom graph ranges such as `1d`, `7d`, `16d`, `30d`, or any other positive number of days
- Automatic wallpaper updates with the `run` command
- Custom refresh intervals such as `30s`, `2m`, `10m`, or `1h`
- Separate price and chart caching
- Cached-data fallback when the API is temporarily unavailable
- Automatic screen resolution detection
- Wallpaper layout automatically scales to the detected resolution
- Automatic desktop environment and wallpaper backend detection
- Multi-desktop and multi-window-manager support
- Lightweight Bash implementation

## Supported desktops and wallpaper backends

cryptopaper automatically detects the current desktop environment and selects an appropriate wallpaper backend.

| Desktop / WM | Wallpaper backend |
| --- | --- |
| KDE Plasma | `plasma-apply-wallpaperimage` |
| GNOME | `gsettings` |
| Cinnamon | `gsettings` |
| MATE | `gsettings` |
| XFCE | `xfconf-query` |
| LXQt | `pcmanfm-qt` |
| Hyprland | `hyprpaper`, `swww`, or `swaybg` |
| Sway / compatible Wayland compositors | `swaybg` or `swww` |
| Generic Wayland | `swww` or `swaybg` |
| Generic X11 / i3 | `feh` |

Tested successfully on:

- KDE Plasma
- GNOME
- Cinnamon
- MATE
- XFCE
- LXQt
- Hyprland
- Niri
- i3

Not every Linux desktop environment or window manager has been tested yet.

## Dependencies

### Core dependencies

- Bash
- curl
- jq
- ImageMagick
- awk

### Wallpaper backend dependencies

You only need the backend used by your desktop environment.

#### KDE Plasma

```text
plasma-apply-wallpaperimage
```

#### GNOME

```text
gsettings
```

#### Cinnamon

```text
gsettings
```

#### MATE

```text
gsettings
```

#### XFCE

```text
xfconf-query
```

#### LXQt

```text
pcmanfm-qt
```

#### Hyprland

At least one of:

```text
hyprpaper
swww
swaybg
```

#### Wayland compositors

At least one of:

```text
swww
swaybg
```

#### Generic X11 / i3

```text
feh
```

## NixOS / Home Manager

Core dependencies:

```nix
home.packages = with pkgs; [
  curl
  jq
  imagemagick
  gawk
];
```

Optional wallpaper tools can be added separately if your desktop does not already provide one:

```nix
home.packages = with pkgs; [
  curl
  jq
  imagemagick
  gawk

  # Optional wallpaper backends
  swaybg
  swww
  feh
];
```

You do not need every wallpaper backend installed.

## Usage

Show help:

```bash
./cryptopaper help
```

Show detected desktop, resolution, session type, and wallpaper backend:

```bash
./cryptopaper info
```

Example:

```text
cryptopaper info

Resolution: 1920x1080
Desktop: GNOME
Session: wayland
Wallpaper backend: GNOME
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

shows:

- a 7-day Bitcoin price graph
- the percentage change over the same 7-day period

## Automatic updates

Keep the wallpaper updated automatically:

```bash
./cryptopaper run
```

By default, this uses:

```text
Graph range: 1 day
Refresh interval: 2 minutes
```

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

Example:

```bash
./cryptopaper run 7d 5m
```

This uses a 7-day graph and refreshes every 5 minutes.

Press `Ctrl+C` to stop.

### Refresh interval note

Very short refresh intervals are supported.

However, the API may return the same price for multiple requests, so very short refresh intervals may not always show a different price.

Frequent requests may also increase the chance of hitting API rate limits.

The default refresh interval is:

```text
2m
```

## Cache commands

Show cached API data:

```bash
./cryptopaper cache
```

Clear cached API data:

```bash
./cryptopaper clear-cache
```

`clear-cache` removes API cache files but does not remove generated wallpaper images.

## Caching

cryptopaper stores its cache in:

```text
~/.cache/cryptopaper/
```

Example contents:

```text
market.json
chart-1d.json
chart-7d.json
wallpaper-1787918370.png
swaybg.pid
```

### Cache files

`market.json` stores the current Bitcoin price.

Files such as:

```text
chart-1d.json
chart-7d.json
chart-30d.json
```

store historical graph data for different time ranges.

Generated wallpapers are stored as:

```text
wallpaper-<timestamp>.png
```

For example:

```text
wallpaper-1787918370.png
```

### swaybg PID file

When cryptopaper uses `swaybg`, it also creates:

```text
swaybg.pid
```

`swaybg` must remain running in the background to keep the wallpaper visible.

cryptopaper stores the process ID of the `swaybg` instance it started so that it can safely stop and replace only its own previous wallpaper process.

Other desktop backends do not need PID files because the desktop environment manages the wallpaper itself.

## Screen resolution

cryptopaper automatically detects the current screen resolution.

It uses desktop/session-specific methods where possible, including:

- `kscreen-doctor` on KDE Plasma
- `hyprctl` on Hyprland
- `swaymsg` on Sway
- `xrandr` on X11
- `xdpyinfo` as an X11 fallback

Invalid or unusually small detected resolutions are rejected.

If automatic detection fails, cryptopaper falls back to:

```text
1920x1080
```

The wallpaper layout, text, graph, and spacing automatically scale to the detected resolution.

### Resolution override

You can manually override resolution detection for testing:

```bash
CRYPTOPAPER_RESOLUTION=2560x1440 ./cryptopaper set
```

Examples:

```bash
CRYPTOPAPER_RESOLUTION=3840x2160 ./cryptopaper set
CRYPTOPAPER_RESOLUTION=3440x1440 ./cryptopaper set
CRYPTOPAPER_RESOLUTION=1366x768 ./cryptopaper set
```

This only changes the generated wallpaper resolution.

It does not change your monitor resolution.

## XFCE note

Fresh XFCE profiles may initially have no wallpaper configuration properties.

cryptopaper attempts to detect existing XFCE wallpaper properties and can initialize a wallpaper property when necessary.

## Wallpaper files

Generated wallpapers are stored in:

```text
~/.cache/cryptopaper/
```

Old generated wallpapers are periodically cleaned up.

## Data source

Bitcoin market data is provided by the CoinGecko API.

cryptopaper uses separate API data for:

- current Bitcoin price
- historical chart data

This keeps the displayed current price independent from the selected chart range.

## Current limitations

- Bitcoin only
- USD only
- Multi-monitor support is still limited
- Not every Linux desktop environment or window manager has been tested
- Some Wayland compositors require an external wallpaper tool such as `swaybg` or `swww`
- `run` currently runs in the foreground
- No systemd/background service mode yet

## Status

Early development.

Desktop compatibility and wallpaper backend support are still being expanded.
