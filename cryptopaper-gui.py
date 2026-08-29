#!/usr/bin/env python3

import gi

gi.require_version("Gtk", "4.0")

from gi.repository import Gtk, GLib, Gio

import json
import os
import signal
import subprocess
import threading
from pathlib import Path


# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

CONFIG_FILE = (
    Path.home()
    / ".config"
    / "cryptopaper"
    / "config"
)

CACHE_DIR = (
    Path.home()
    / ".cache"
    / "cryptopaper"
)


# ---------------------------------------------------------
# cryptopaper settings
# ---------------------------------------------------------

COINS = {
    "Bitcoin": "btc",
    "Ethereum": "eth",
    "Solana": "sol",
    "Dogecoin": "doge",
    "Monero": "xmr",
    "BNB": "bnb",
    "XRP": "xrp",
}

COIN_IDS = {
    "btc": "bitcoin",
    "eth": "ethereum",
    "sol": "solana",
    "doge": "dogecoin",
    "xmr": "monero",
    "bnb": "binancecoin",
    "xrp": "ripple",
}

COIN_LABELS = {
    "btc": "BITCOIN",
    "eth": "ETHEREUM",
    "sol": "SOLANA",
    "doge": "DOGECOIN",
    "xmr": "MONERO",
    "bnb": "BNB",
    "xrp": "XRP",
}

CURRENCY_SYMBOLS = {
    "USD": "$",
    "EUR": "€",
    "GBP": "£",
}

CURRENCIES = [
    "USD",
    "EUR",
    "GBP",
]

RANGES = [
    "1d",
    "3d",
    "7d",
    "14d",
    "16d",
    "30d",
    "90d",
]

INTERVALS = [
    "15s",
    "30s",
    "45s",
    "1m",
    "2m",
    "5m",
    "10m",
    "30m",
    "1h",
]


DEFAULT_COIN = "btc"
DEFAULT_CURRENCY = "USD"
DEFAULT_RANGE = "1d"
DEFAULT_INTERVAL = "2m"


# ---------------------------------------------------------
# StatusNotifierItem D-Bus interface
# ---------------------------------------------------------

STATUS_NOTIFIER_XML = """
<node>
  <interface name="org.kde.StatusNotifierItem">

    <method name="Activate">
      <arg type="i" name="x" direction="in"/>
      <arg type="i" name="y" direction="in"/>
    </method>

    <method name="SecondaryActivate">
      <arg type="i" name="x" direction="in"/>
      <arg type="i" name="y" direction="in"/>
    </method>

    <method name="ContextMenu">
      <arg type="i" name="x" direction="in"/>
      <arg type="i" name="y" direction="in"/>
    </method>

    <method name="Scroll">
      <arg type="i" name="delta" direction="in"/>
      <arg type="s" name="orientation" direction="in"/>
    </method>

    <property
      name="Category"
      type="s"
      access="read"/>

    <property
      name="Id"
      type="s"
      access="read"/>

    <property
      name="Title"
      type="s"
      access="read"/>

    <property
      name="Status"
      type="s"
      access="read"/>

    <property
      name="WindowId"
      type="u"
      access="read"/>

    <property
      name="IconName"
      type="s"
      access="read"/>

    <property
      name="OverlayIconName"
      type="s"
      access="read"/>

    <property
      name="AttentionIconName"
      type="s"
      access="read"/>

    <property
      name="ItemIsMenu"
      type="b"
      access="read"/>

    <property
      name="Menu"
      type="o"
      access="read"/>

    <signal name="NewTitle"/>

    <signal name="NewIcon"/>

    <signal name="NewStatus">
      <arg type="s" name="status"/>
    </signal>

  </interface>
</node>
"""


class StatusNotifierItem:
    def __init__(self, app):
        self.app = app

        self.connection = None
        self.registration_id = 0

        self.available = False
        self.registered_with_watcher = False

        self.running = False

        self.object_path = "/StatusNotifierItem"

        self.service_name = (
            f"org.kde.StatusNotifierItem-"
            f"{os.getpid()}-1"
        )

        self.node_info = (
            Gio.DBusNodeInfo.new_for_xml(
                STATUS_NOTIFIER_XML
            )
        )

        self.interface_info = (
            self.node_info.interfaces[0]
        )

        self.setup()

    def setup(self):
        try:
            self.connection = (
                Gio.bus_get_sync(
                    Gio.BusType.SESSION,
                    None,
                )
            )

            self.request_bus_name()

            self.registration_id = (
                self.connection.register_object(
                    self.object_path,
                    self.interface_info,
                    self.on_method_call,
                    self.on_get_property,
                    None,
                )
            )

            self.try_register_with_watcher()

            GLib.timeout_add_seconds(
                5,
                self.check_watcher,
            )

        except Exception as error:
            print(
                f"Tray support unavailable: {error}"
            )

            self.available = False

    def request_bus_name(self):
        result = self.connection.call_sync(
            "org.freedesktop.DBus",
            "/org/freedesktop/DBus",
            "org.freedesktop.DBus",
            "RequestName",
            GLib.Variant(
                "(su)",
                (
                    self.service_name,
                    0,
                ),
            ),
            GLib.VariantType("(u)"),
            Gio.DBusCallFlags.NONE,
            -1,
            None,
        )

        reply = result.unpack()[0]

        if reply not in (1, 4):
            raise RuntimeError(
                "Could not acquire tray D-Bus name."
            )

    def watcher_exists(self):
        if self.connection is None:
            return False

        try:
            result = self.connection.call_sync(
                "org.freedesktop.DBus",
                "/org/freedesktop/DBus",
                "org.freedesktop.DBus",
                "NameHasOwner",
                GLib.Variant(
                    "(s)",
                    (
                        "org.kde.StatusNotifierWatcher",
                    ),
                ),
                GLib.VariantType("(b)"),
                Gio.DBusCallFlags.NONE,
                2000,
                None,
            )

            return bool(
                result.unpack()[0]
            )

        except Exception:
            return False

    def try_register_with_watcher(self):
        if not self.watcher_exists():
            self.available = False
            self.registered_with_watcher = False
            return False

        try:
            self.connection.call_sync(
                "org.kde.StatusNotifierWatcher",
                "/StatusNotifierWatcher",
                "org.kde.StatusNotifierWatcher",
                "RegisterStatusNotifierItem",
                GLib.Variant(
                    "(s)",
                    (
                        self.service_name,
                    ),
                ),
                None,
                Gio.DBusCallFlags.NONE,
                2000,
                None,
            )

            self.available = True
            self.registered_with_watcher = True

            return True

        except Exception as error:
            print(
                f"Could not register tray icon: {error}"
            )

            self.available = False
            self.registered_with_watcher = False

            return False

    def check_watcher(self):
        exists = self.watcher_exists()

        if (
            exists
            and not self.registered_with_watcher
        ):
            self.try_register_with_watcher()

        elif not exists:
            self.available = False
            self.registered_with_watcher = False

        return True

    def on_get_property(
        self,
        connection,
        sender,
        object_path,
        interface_name,
        property_name,
    ):
        if property_name == "Category":
            return GLib.Variant(
                "s",
                "ApplicationStatus",
            )

        if property_name == "Id":
            return GLib.Variant(
                "s",
                "cryptopaper",
            )

        if property_name == "Title":
            if self.running:
                title = (
                    "cryptopaper — "
                    "Auto Update Running"
                )
            else:
                title = "cryptopaper"

            return GLib.Variant(
                "s",
                title,
            )

        if property_name == "Status":
            return GLib.Variant(
                "s",
                "Active",
            )

        if property_name == "WindowId":
            return GLib.Variant(
                "u",
                0,
            )

        if property_name == "IconName":
            return GLib.Variant(
                "s",
                "cryptopaper",
            )

        if property_name == "OverlayIconName":
            return GLib.Variant(
                "s",
                "",
            )

        if property_name == "AttentionIconName":
            return GLib.Variant(
                "s",
                "",
            )

        if property_name == "ItemIsMenu":
            return GLib.Variant(
                "b",
                False,
            )

        if property_name == "Menu":
            return GLib.Variant(
                "o",
                "/NO_DBUSMENU",
            )

        return None

    def on_method_call(
        self,
        connection,
        sender,
        object_path,
        interface_name,
        method_name,
        parameters,
        invocation,
    ):
        if method_name in (
            "Activate",
            "SecondaryActivate",
            "ContextMenu",
        ):
            GLib.idle_add(
                self.app.show_main_window
            )

            invocation.return_value(
                None
            )

            return

        if method_name == "Scroll":
            invocation.return_value(
                None
            )

            return

        invocation.return_dbus_error(
            "org.cryptopaper.Error.UnknownMethod",
            f"Unknown method: {method_name}",
        )

    def set_running(self, running):
        self.running = running

        if self.connection is None:
            return

        try:
            self.connection.emit_signal(
                None,
                self.object_path,
                "org.kde.StatusNotifierItem",
                "NewTitle",
                None,
            )

            self.connection.emit_signal(
                None,
                self.object_path,
                "org.kde.StatusNotifierItem",
                "NewIcon",
                None,
            )

        except Exception:
            pass

    def cleanup(self):
        if (
            self.connection is not None
            and self.registration_id
        ):
            try:
                self.connection.unregister_object(
                    self.registration_id
                )

            except Exception:
                pass

            self.registration_id = 0


# ---------------------------------------------------------
# Main window
# ---------------------------------------------------------

class CryptoPaperWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(
            application=app
        )

        self.set_title(
            "cryptopaper"
        )

        self.set_default_size(
            520,
            590,
        )

        self.auto_process = None

        self.stopping_auto = False
        self.stopped_for_settings_change = False
        self.loading_settings = True

        self.last_cache_path = None
        self.last_cache_signature = None

        self.main_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=18,
        )

        self.main_box.set_margin_top(24)
        self.main_box.set_margin_bottom(24)
        self.main_box.set_margin_start(24)
        self.main_box.set_margin_end(24)

        self.set_child(
            self.main_box
        )

        self.build_header()
        self.build_settings()
        self.build_price()
        self.build_buttons()
        self.build_status()

        self.stop_button.set_sensitive(
            False
        )

        self.load_current_settings()

        GLib.timeout_add(
            1000,
            self.check_price_cache,
        )

    # -----------------------------------------------------
    # UI
    # -----------------------------------------------------

    def build_header(self):
        title = Gtk.Label(
            label="CRYPTOPAPER"
        )

        title.add_css_class(
            "title-1"
        )

        title.set_halign(
            Gtk.Align.CENTER
        )

        subtitle = Gtk.Label(
            label=(
                "Cryptocurrency wallpaper "
                "controller"
            )
        )

        subtitle.add_css_class(
            "dim-label"
        )

        subtitle.set_halign(
            Gtk.Align.CENTER
        )

        self.main_box.append(
            title
        )

        self.main_box.append(
            subtitle
        )

    def build_settings(self):
        frame = Gtk.Frame()

        grid = Gtk.Grid()

        grid.set_row_spacing(14)
        grid.set_column_spacing(18)

        grid.set_margin_top(18)
        grid.set_margin_bottom(18)
        grid.set_margin_start(18)
        grid.set_margin_end(18)

        frame.set_child(
            grid
        )

        coin_label = Gtk.Label(
            label="Cryptocurrency"
        )

        coin_label.set_halign(
            Gtk.Align.START
        )

        self.coin_dropdown = (
            Gtk.DropDown.new_from_strings(
                list(
                    COINS.keys()
                )
            )
        )

        currency_label = Gtk.Label(
            label="Currency"
        )

        currency_label.set_halign(
            Gtk.Align.START
        )

        self.currency_dropdown = (
            Gtk.DropDown.new_from_strings(
                CURRENCIES
            )
        )

        range_label = Gtk.Label(
            label="Chart range"
        )

        range_label.set_halign(
            Gtk.Align.START
        )

        self.range_dropdown = (
            Gtk.DropDown.new_from_strings(
                RANGES
            )
        )

        interval_label = Gtk.Label(
            label="Update interval"
        )

        interval_label.set_halign(
            Gtk.Align.START
        )

        self.interval_dropdown = (
            Gtk.DropDown.new_from_strings(
                INTERVALS
            )
        )

        grid.attach(
            coin_label,
            0,
            0,
            1,
            1,
        )

        grid.attach(
            self.coin_dropdown,
            1,
            0,
            1,
            1,
        )

        grid.attach(
            currency_label,
            0,
            1,
            1,
            1,
        )

        grid.attach(
            self.currency_dropdown,
            1,
            1,
            1,
            1,
        )

        grid.attach(
            range_label,
            0,
            2,
            1,
            1,
        )

        grid.attach(
            self.range_dropdown,
            1,
            2,
            1,
            1,
        )

        grid.attach(
            interval_label,
            0,
            3,
            1,
            1,
        )

        grid.attach(
            self.interval_dropdown,
            1,
            3,
            1,
            1,
        )

        self.coin_dropdown.connect(
            "notify::selected",
            self.on_setting_changed,
        )

        self.currency_dropdown.connect(
            "notify::selected",
            self.on_setting_changed,
        )

        self.range_dropdown.connect(
            "notify::selected",
            self.on_setting_changed,
        )

        self.interval_dropdown.connect(
            "notify::selected",
            self.on_setting_changed,
        )

        self.main_box.append(
            frame
        )

    def build_price(self):
        price_title = Gtk.Label(
            label="Current Price"
        )

        price_title.add_css_class(
            "heading"
        )

        price_title.set_halign(
            Gtk.Align.CENTER
        )

        self.price_label = Gtk.Label(
            label="Loading..."
        )

        self.price_label.add_css_class(
            "title-2"
        )

        self.price_label.set_halign(
            Gtk.Align.CENTER
        )

        self.main_box.append(
            price_title
        )

        self.main_box.append(
            self.price_label
        )

    def build_buttons(self):
        self.set_button = Gtk.Button(
            label="Set Wallpaper"
        )

        self.set_button.add_css_class(
            "suggested-action"
        )

        self.set_button.connect(
            "clicked",
            self.on_set_wallpaper,
        )

        auto_box = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=12,
        )

        auto_box.set_homogeneous(
            True
        )

        self.start_button = Gtk.Button(
            label="Start Auto Update"
        )

        self.start_button.connect(
            "clicked",
            self.on_start_auto,
        )

        self.stop_button = Gtk.Button(
            label="Stop"
        )

        self.stop_button.add_css_class(
            "destructive-action"
        )

        self.stop_button.connect(
            "clicked",
            self.on_stop_auto,
        )

        auto_box.append(
            self.start_button
        )

        auto_box.append(
            self.stop_button
        )

        self.refresh_button = Gtk.Button(
            label="Refresh Price"
        )

        self.refresh_button.connect(
            "clicked",
            self.on_refresh_price,
        )

        self.quit_button = Gtk.Button(
            label="Quit Application"
        )

        self.quit_button.connect(
            "clicked",
            self.on_quit_application,
        )

        self.main_box.append(
            self.set_button
        )

        self.main_box.append(
            auto_box
        )

        self.main_box.append(
            self.refresh_button
        )

        self.main_box.append(
            self.quit_button
        )

    def build_status(self):
        separator = Gtk.Separator(
            orientation=(
                Gtk.Orientation.HORIZONTAL
            )
        )

        self.status_label = Gtk.Label(
            label="Ready"
        )

        self.status_label.add_css_class(
            "dim-label"
        )

        self.status_label.set_halign(
            Gtk.Align.START
        )

        self.status_label.set_wrap(
            True
        )

        self.main_box.append(
            separator
        )

        self.main_box.append(
            self.status_label
        )

    # -----------------------------------------------------
    # CLI
    # -----------------------------------------------------

    def run_command(self, args):
        try:
            result = subprocess.run(
                [
                    "cryptopaper",
                    *args,
                ],
                capture_output=True,
                text=True,
            )

        except FileNotFoundError:
            raise RuntimeError(
                "The cryptopaper command "
                "was not found in PATH."
            )

        if result.returncode != 0:
            message = (
                result.stderr.strip()
                or result.stdout.strip()
                or "Unknown error"
            )

            raise RuntimeError(
                message
            )

        return result.stdout.strip()

    def run_async(
        self,
        work,
        on_success=None,
        on_error=None,
    ):
        def worker():
            try:
                result = work()

                if on_success is not None:
                    GLib.idle_add(
                        self._finish_success,
                        on_success,
                        result,
                    )

            except Exception as error:
                if on_error is not None:
                    GLib.idle_add(
                        self._finish_error,
                        on_error,
                        str(error),
                    )

        threading.Thread(
            target=worker,
            daemon=True,
        ).start()

    def _finish_success(
        self,
        callback,
        result,
    ):
        callback(result)

        return False

    def _finish_error(
        self,
        callback,
        message,
    ):
        callback(message)

        return False

    # -----------------------------------------------------
    # Config
    # -----------------------------------------------------

    def load_config(self):
        settings = {
            "coin": DEFAULT_COIN,
            "currency": DEFAULT_CURRENCY,
            "range": DEFAULT_RANGE,
            "interval": DEFAULT_INTERVAL,
        }

        if CONFIG_FILE.exists():
            try:
                with CONFIG_FILE.open(
                    "r",
                    encoding="utf-8",
                ) as file:

                    for line in file:
                        line = line.strip()

                        if not line:
                            continue

                        if "=" not in line:
                            continue

                        key, value = (
                            line.split(
                                "=",
                                1,
                            )
                        )

                        key = key.strip()
                        value = value.strip()

                        if key in settings:
                            settings[key] = value

            except OSError:
                pass

        if (
            settings["coin"]
            not in COINS.values()
        ):
            settings["coin"] = (
                DEFAULT_COIN
            )

        if (
            settings["currency"]
            not in CURRENCIES
        ):
            settings["currency"] = (
                DEFAULT_CURRENCY
            )

        if (
            settings["range"]
            not in RANGES
        ):
            settings["range"] = (
                DEFAULT_RANGE
            )

        if (
            settings["interval"]
            not in INTERVALS
        ):
            settings["interval"] = (
                DEFAULT_INTERVAL
            )

        return settings

    def load_current_settings(self):
        settings = self.load_config()

        coin_values = list(
            COINS.values()
        )

        try:
            coin_index = (
                coin_values.index(
                    settings["coin"]
                )
            )

        except ValueError:
            coin_index = 0

        self.coin_dropdown.set_selected(
            coin_index
        )

        self.set_dropdown_value(
            self.currency_dropdown,
            CURRENCIES,
            settings["currency"],
            DEFAULT_CURRENCY,
        )

        self.set_dropdown_value(
            self.range_dropdown,
            RANGES,
            settings["range"],
            DEFAULT_RANGE,
        )

        self.set_dropdown_value(
            self.interval_dropdown,
            INTERVALS,
            settings["interval"],
            DEFAULT_INTERVAL,
        )

        self.loading_settings = False

        self.status_label.set_text(
            "Loaded saved cryptopaper "
            "settings."
        )

        self.refresh_price_async()

    # -----------------------------------------------------
    # Dropdown helpers
    # -----------------------------------------------------

    def set_dropdown_value(
        self,
        dropdown,
        values,
        value,
        fallback,
    ):
        try:
            index = values.index(
                value
            )

        except ValueError:
            index = values.index(
                fallback
            )

        dropdown.set_selected(
            index
        )

    def get_selected_coin(self):
        index = (
            self.coin_dropdown
            .get_selected()
        )

        names = list(
            COINS.keys()
        )

        if index >= len(names):
            return DEFAULT_COIN

        return COINS[
            names[index]
        ]

    def get_selected_currency(self):
        index = (
            self.currency_dropdown
            .get_selected()
        )

        if index >= len(
            CURRENCIES
        ):
            return DEFAULT_CURRENCY

        return CURRENCIES[index]

    def get_selected_range(self):
        index = (
            self.range_dropdown
            .get_selected()
        )

        if index >= len(
            RANGES
        ):
            return DEFAULT_RANGE

        return RANGES[index]

    def get_selected_interval(self):
        index = (
            self.interval_dropdown
            .get_selected()
        )

        if index >= len(
            INTERVALS
        ):
            return DEFAULT_INTERVAL

        return INTERVALS[index]

    def get_current_settings(self):
        return {
            "coin": (
                self.get_selected_coin()
            ),
            "currency": (
                self.get_selected_currency()
            ),
            "range": (
                self.get_selected_range()
            ),
            "interval": (
                self.get_selected_interval()
            ),
        }

    # -----------------------------------------------------
    # Cache price watcher
    # -----------------------------------------------------

    def get_market_cache_path(self):
        coin = self.get_selected_coin()

        currency = (
            self.get_selected_currency()
            .lower()
        )

        return (
            CACHE_DIR
            / f"{coin}-market-{currency}.json"
        )

    def format_price(
        self,
        coin,
        currency,
        price,
    ):
        if price >= 100:
            formatted = f"{price:.2f}"

        elif price >= 1:
            formatted = f"{price:.4f}"

        else:
            formatted = f"{price:.6f}"

        symbol = CURRENCY_SYMBOLS.get(
            currency,
            "",
        )

        coin_label = COIN_LABELS.get(
            coin,
            coin.upper(),
        )

        return (
            f"{coin_label}: "
            f"{symbol}{formatted}"
        )

    def read_price_from_cache(
        self,
        cache_path,
    ):
        try:
            with cache_path.open(
                "r",
                encoding="utf-8",
            ) as file:
                data = json.load(
                    file
                )

        except (
            OSError,
            json.JSONDecodeError,
        ):
            return None

        coin = self.get_selected_coin()

        currency = (
            self.get_selected_currency()
        )

        coin_id = COIN_IDS.get(
            coin
        )

        if not coin_id:
            return None

        coin_data = data.get(
            coin_id
        )

        if not isinstance(
            coin_data,
            dict,
        ):
            return None

        price = coin_data.get(
            currency.lower()
        )

        if not isinstance(
            price,
            (int, float),
        ):
            return None

        return self.format_price(
            coin,
            currency,
            float(price),
        )

    def check_price_cache(self):
        cache_path = (
            self.get_market_cache_path()
        )

        if cache_path != self.last_cache_path:
            self.last_cache_path = (
                cache_path
            )

            self.last_cache_signature = None

        if not cache_path.exists():
            return True

        try:
            stat = cache_path.stat()

            signature = (
                stat.st_mtime_ns,
                stat.st_size,
            )

        except OSError:
            return True

        if (
            signature
            == self.last_cache_signature
        ):
            return True

        self.last_cache_signature = (
            signature
        )

        price_text = (
            self.read_price_from_cache(
                cache_path
            )
        )

        if price_text:
            self.price_label.set_text(
                price_text
            )

        return True

    # -----------------------------------------------------
    # Save settings
    # -----------------------------------------------------

    def save_settings_values(
        self,
        settings,
    ):
        self.run_command(
            [
                "coin",
                settings["coin"],
            ]
        )

        self.run_command(
            [
                "cur",
                settings["currency"],
            ]
        )

        self.run_command(
            [
                "range",
                settings["range"],
            ]
        )

        self.run_command(
            [
                "interval",
                settings["interval"],
            ]
        )

    def auto_is_running(self):
        return (
            self.auto_process is not None
            and self.auto_process.poll() is None
        )

    def stop_auto_for_settings_change(self):
        if not self.auto_is_running():
            return False

        self.stopped_for_settings_change = True
        self.stopping_auto = True

        self.stop_button.set_sensitive(
            False
        )

        self.stop_auto_process_group(
            force=False
        )

        GLib.timeout_add(
            2000,
            self.force_stop_auto_if_needed,
        )

        return True

    def on_setting_changed(
        self,
        dropdown,
        param,
    ):
        if self.loading_settings:
            return

        auto_was_running = (
            self.stop_auto_for_settings_change()
        )

        self.last_cache_path = None
        self.last_cache_signature = None

        settings = (
            self.get_current_settings()
        )

        if auto_was_running:
            self.status_label.set_text(
                "Automatic updates stopped "
                "because settings changed."
            )
        else:
            self.status_label.set_text(
                "Saving settings..."
            )

        self.run_async(
            lambda: (
                self.save_settings_values(
                    settings
                )
            ),
            self.on_settings_saved,
            self.on_settings_save_error,
        )

    def on_settings_saved(
        self,
        result,
    ):
        if self.stopped_for_settings_change:
            self.status_label.set_text(
                "Automatic updates stopped "
                "because settings changed."
            )
        else:
            self.status_label.set_text(
                "Settings saved."
            )

        self.refresh_price_async(
            preserve_status=(
                self.stopped_for_settings_change
            )
        )

    def on_settings_save_error(
        self,
        message,
    ):
        self.status_label.set_text(
            f"Could not save settings: "
            f"{message}"
        )

    # -----------------------------------------------------
    # Price
    # -----------------------------------------------------

    def refresh_price_async(
        self,
        preserve_status=False,
    ):
        self.price_label.set_text(
            "Loading..."
        )

        self.run_async(
            lambda: self.run_command(
                ["price"]
            ),
            lambda output: (
                self.on_price_loaded(
                    output,
                    preserve_status,
                )
            ),
            lambda message: (
                self.on_price_error(
                    message,
                    preserve_status,
                )
            ),
        )

    def on_price_loaded(
        self,
        output,
        preserve_status=False,
    ):
        if output:
            self.price_label.set_text(
                output
            )

        else:
            self.price_label.set_text(
                "Price unavailable"
            )

        if not preserve_status:
            self.status_label.set_text(
                "Price refreshed."
            )

    def on_price_error(
        self,
        message,
        preserve_status=False,
    ):
        self.price_label.set_text(
            "Price unavailable"
        )

        if not preserve_status:
            self.status_label.set_text(
                f"Could not fetch price: "
                f"{message}"
            )

    def on_refresh_price(
        self,
        button,
    ):
        self.stopped_for_settings_change = False

        self.status_label.set_text(
            "Refreshing price..."
        )

        self.refresh_price_async()

    # -----------------------------------------------------
    # Wallpaper
    # -----------------------------------------------------

    def set_busy(
        self,
        busy,
    ):
        self.set_button.set_sensitive(
            not busy
        )

        self.refresh_button.set_sensitive(
            not busy
        )

        if not self.auto_is_running():
            self.start_button.set_sensitive(
                not busy
            )

    def on_set_wallpaper(
        self,
        button,
    ):
        self.stopped_for_settings_change = False

        settings = (
            self.get_current_settings()
        )

        self.status_label.set_text(
            "Generating wallpaper..."
        )

        self.set_busy(
            True
        )

        def work():
            self.save_settings_values(
                settings
            )

            return self.run_command(
                ["set"]
            )

        self.run_async(
            work,
            self.on_wallpaper_set,
            self.on_wallpaper_error,
        )

    def on_wallpaper_set(
        self,
        output,
    ):
        self.set_busy(
            False
        )

        if output:
            self.status_label.set_text(
                output
            )

        else:
            self.status_label.set_text(
                "Wallpaper updated."
            )

        self.refresh_price_async()

    def on_wallpaper_error(
        self,
        message,
    ):
        self.set_busy(
            False
        )

        self.status_label.set_text(
            f"Wallpaper update failed: "
            f"{message}"
        )

    # -----------------------------------------------------
    # Auto updater
    # -----------------------------------------------------

    def on_start_auto(
        self,
        button,
    ):
        if self.auto_is_running():
            self.status_label.set_text(
                "Automatic updates are "
                "already running."
            )

            return

        self.stopped_for_settings_change = False

        settings = (
            self.get_current_settings()
        )

        self.status_label.set_text(
            "Starting automatic updates..."
        )

        self.start_button.set_sensitive(
            False
        )

        self.stopping_auto = False

        def work():
            self.save_settings_values(
                settings
            )

            self.auto_process = (
                subprocess.Popen(
                    ["cryptopaper"],
                    stdout=(
                        subprocess.DEVNULL
                    ),
                    stderr=(
                        subprocess.DEVNULL
                    ),
                    start_new_session=True,
                )
            )

            return True

        self.run_async(
            work,
            self.on_auto_started,
            self.on_auto_start_error,
        )

    def on_auto_started(
        self,
        result,
    ):
        self.status_label.set_text(
            "Automatic updates started."
        )

        self.start_button.set_sensitive(
            False
        )

        self.stop_button.set_sensitive(
            True
        )

        self.get_application().set_tray_running(
            True
        )

        GLib.timeout_add(
            250,
            self.check_auto_process,
        )

    def on_auto_start_error(
        self,
        message,
    ):
        self.auto_process = None

        self.start_button.set_sensitive(
            True
        )

        self.stop_button.set_sensitive(
            False
        )

        self.get_application().set_tray_running(
            False
        )

        self.status_label.set_text(
            "Could not start automatic "
            f"updates: {message}"
        )

    def stop_auto_process_group(
        self,
        force=False,
    ):
        if self.auto_process is None:
            return

        if (
            self.auto_process.poll()
            is not None
        ):
            return

        try:
            process_group = (
                os.getpgid(
                    self.auto_process.pid
                )
            )

            if force:
                os.killpg(
                    process_group,
                    signal.SIGKILL,
                )

            else:
                os.killpg(
                    process_group,
                    signal.SIGTERM,
                )

        except ProcessLookupError:
            pass

        except Exception as error:
            self.status_label.set_text(
                "Could not stop automatic "
                f"updates: {error}"
            )

    def on_stop_auto(
        self,
        button,
    ):
        self.stopped_for_settings_change = False

        if not self.auto_is_running():
            self.status_label.set_text(
                "Automatic updates are "
                "not running."
            )

            self.start_button.set_sensitive(
                True
            )

            self.stop_button.set_sensitive(
                False
            )

            self.get_application().set_tray_running(
                False
            )

            return

        self.stopping_auto = True

        self.stop_button.set_sensitive(
            False
        )

        self.status_label.set_text(
            "Stopping automatic updates..."
        )

        self.stop_auto_process_group(
            force=False
        )

        GLib.timeout_add(
            2000,
            self.force_stop_auto_if_needed,
        )

    def force_stop_auto_if_needed(
        self
    ):
        if self.auto_is_running():
            self.stop_auto_process_group(
                force=True
            )

        return False

    def check_auto_process(
        self
    ):
        if self.auto_process is None:
            return False

        return_code = (
            self.auto_process.poll()
        )

        if return_code is None:
            return True

        self.start_button.set_sensitive(
            True
        )

        self.stop_button.set_sensitive(
            False
        )

        self.get_application().set_tray_running(
            False
        )

        if self.stopped_for_settings_change:
            self.status_label.set_text(
                "Automatic updates stopped "
                "because settings changed."
            )

        elif self.stopping_auto:
            self.status_label.set_text(
                "Automatic updates stopped."
            )

        elif return_code == 0:
            self.status_label.set_text(
                "Automatic updates stopped."
            )

        else:
            self.status_label.set_text(
                "cryptopaper stopped "
                "unexpectedly."
            )

        self.auto_process = None
        self.stopping_auto = False

        return False

    # -----------------------------------------------------
    # Closing / quitting
    # -----------------------------------------------------

    def on_quit_application(
        self,
        button,
    ):
        self.get_application().quit_completely()

    def do_close_request(
        self
    ):
        app = self.get_application()

        if (
            app.status_notifier is not None
            and app.status_notifier.available
        ):
            self.set_visible(
                False
            )

            return True

        app.quit_completely()

        return True


# ---------------------------------------------------------
# Application
# ---------------------------------------------------------

class CryptoPaperApplication(
    Gtk.Application
):
    def __init__(self):
        super().__init__(
            application_id=(
                "com.cryptopaper.app"
            )
        )

        self.window = None
        self.status_notifier = None

        self.quitting = False

    def do_activate(self):
        if self.window is None:
            self.window = (
                CryptoPaperWindow(
                    self
                )
            )

            self.status_notifier = (
                StatusNotifierItem(
                    self
                )
            )

        self.show_main_window()

    def show_main_window(self):
        if self.window is None:
            return False

        self.window.set_visible(
            True
        )

        self.window.present()

        return False

    def set_tray_running(
        self,
        running,
    ):
        if self.status_notifier is None:
            return

        self.status_notifier.set_running(
            running
        )

    def quit_completely(self):
        if self.quitting:
            return

        self.quitting = True

        if self.window is not None:
            if self.window.auto_is_running():
                self.window.stop_auto_process_group(
                    force=True
                )

        if self.status_notifier is not None:
            self.status_notifier.cleanup()

        self.quit()


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():
    app = CryptoPaperApplication()

    app.run(None)


if __name__ == "__main__":
    main()
