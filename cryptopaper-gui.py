#!/usr/bin/env python3

import gi
gi.require_version("Gtk", "4.0")

from gi.repository import Gtk, GLib

import os
import signal
import subprocess
import threading
from pathlib import Path


CONFIG_FILE = (
    Path.home()
    / ".config"
    / "cryptopaper"
    / "config"
)


COINS = {
    "Bitcoin": "btc",
    "Ethereum": "eth",
    "Solana": "sol",
    "Dogecoin": "doge",
    "Monero": "xmr",
    "BNB": "bnb",
    "XRP": "xrp",
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


class CryptoPaperWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app)

        self.set_title("cryptopaper")
        self.set_default_size(520, 560)

        self.auto_process = None
        self.stopping_auto = False
        self.loading_settings = True

        self.main_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=18,
        )

        self.main_box.set_margin_top(24)
        self.main_box.set_margin_bottom(24)
        self.main_box.set_margin_start(24)
        self.main_box.set_margin_end(24)

        self.set_child(self.main_box)

        self.build_header()
        self.build_settings()
        self.build_price()
        self.build_buttons()
        self.build_status()

        self.stop_button.set_sensitive(False)

        self.load_current_settings()

    # ---------------------------------------------------------
    # UI
    # ---------------------------------------------------------

    def build_header(self):
        title = Gtk.Label(
            label="CRYPTOPAPER"
        )

        title.add_css_class("title-1")
        title.set_halign(Gtk.Align.CENTER)

        subtitle = Gtk.Label(
            label="Cryptocurrency wallpaper controller"
        )

        subtitle.add_css_class("dim-label")
        subtitle.set_halign(Gtk.Align.CENTER)

        self.main_box.append(title)
        self.main_box.append(subtitle)

    def build_settings(self):
        frame = Gtk.Frame()

        grid = Gtk.Grid()

        grid.set_row_spacing(14)
        grid.set_column_spacing(18)

        grid.set_margin_top(18)
        grid.set_margin_bottom(18)
        grid.set_margin_start(18)
        grid.set_margin_end(18)

        frame.set_child(grid)

        coin_label = Gtk.Label(
            label="Cryptocurrency"
        )

        coin_label.set_halign(
            Gtk.Align.START
        )

        self.coin_dropdown = (
            Gtk.DropDown.new_from_strings(
                list(COINS.keys())
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

        self.main_box.append(frame)

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

        auto_box.set_homogeneous(True)

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

        self.main_box.append(
            self.set_button
        )

        self.main_box.append(
            auto_box
        )

        self.main_box.append(
            self.refresh_button
        )

    def build_status(self):
        separator = Gtk.Separator(
            orientation=Gtk.Orientation.HORIZONTAL
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

        self.status_label.set_wrap(True)

        self.main_box.append(
            separator
        )

        self.main_box.append(
            self.status_label
        )

    # ---------------------------------------------------------
    # CLI helpers
    # ---------------------------------------------------------

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
                "The cryptopaper command was not found in PATH."
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

        thread = threading.Thread(
            target=worker,
            daemon=True,
        )

        thread.start()

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

    # ---------------------------------------------------------
    # Config
    # ---------------------------------------------------------

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

                        key, value = line.split(
                            "=",
                            1,
                        )

                        key = key.strip()
                        value = value.strip()

                        if key in settings:
                            settings[key] = value

            except OSError:
                pass

        if settings["coin"] not in COINS.values():
            settings["coin"] = DEFAULT_COIN

        if settings["currency"] not in CURRENCIES:
            settings["currency"] = DEFAULT_CURRENCY

        if settings["range"] not in RANGES:
            settings["range"] = DEFAULT_RANGE

        if settings["interval"] not in INTERVALS:
            settings["interval"] = DEFAULT_INTERVAL

        return settings

    def load_current_settings(self):
        settings = self.load_config()

        coin = settings["coin"]
        currency = settings["currency"]
        chart_range = settings["range"]
        interval = settings["interval"]

        coin_values = list(
            COINS.values()
        )

        try:
            coin_index = (
                coin_values.index(
                    coin
                )
            )

        except ValueError:
            coin_index = (
                coin_values.index(
                    DEFAULT_COIN
                )
            )

        self.coin_dropdown.set_selected(
            coin_index
        )

        self.set_dropdown_value(
            self.currency_dropdown,
            CURRENCIES,
            currency,
            DEFAULT_CURRENCY,
        )

        self.set_dropdown_value(
            self.range_dropdown,
            RANGES,
            chart_range,
            DEFAULT_RANGE,
        )

        self.set_dropdown_value(
            self.interval_dropdown,
            INTERVALS,
            interval,
            DEFAULT_INTERVAL,
        )

        self.loading_settings = False

        self.status_label.set_text(
            "Loaded saved cryptopaper settings."
        )

        self.refresh_price_async()

    # ---------------------------------------------------------
    # Dropdown helpers
    # ---------------------------------------------------------

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

        name = names[index]

        return COINS[name]

    def get_selected_currency(self):
        index = (
            self.currency_dropdown
            .get_selected()
        )

        if index >= len(CURRENCIES):
            return DEFAULT_CURRENCY

        return CURRENCIES[index]

    def get_selected_range(self):
        index = (
            self.range_dropdown
            .get_selected()
        )

        if index >= len(RANGES):
            return DEFAULT_RANGE

        return RANGES[index]

    def get_selected_interval(self):
        index = (
            self.interval_dropdown
            .get_selected()
        )

        if index >= len(INTERVALS):
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

    # ---------------------------------------------------------
    # Save settings
    # ---------------------------------------------------------

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

    def on_setting_changed(
        self,
        dropdown,
        param,
    ):
        if self.loading_settings:
            return

        settings = (
            self.get_current_settings()
        )

        self.status_label.set_text(
            "Saving settings..."
        )

        self.run_async(
            lambda: self.save_settings_values(
                settings
            ),
            self.on_settings_saved,
            self.on_settings_save_error,
        )

    def on_settings_saved(
        self,
        result,
    ):
        self.status_label.set_text(
            "Settings saved."
        )

        self.refresh_price_async()

    def on_settings_save_error(
        self,
        message,
    ):
        self.status_label.set_text(
            f"Could not save settings: {message}"
        )

    # ---------------------------------------------------------
    # Price
    # ---------------------------------------------------------

    def refresh_price_async(self):
        self.price_label.set_text(
            "Loading..."
        )

        self.run_async(
            lambda: self.run_command(
                ["price"]
            ),
            self.on_price_loaded,
            self.on_price_error,
        )

    def on_price_loaded(
        self,
        output,
    ):
        if output:
            self.price_label.set_text(
                output
            )

        else:
            self.price_label.set_text(
                "Price unavailable"
            )

        self.status_label.set_text(
            "Price refreshed."
        )

    def on_price_error(
        self,
        message,
    ):
        self.price_label.set_text(
            "Price unavailable"
        )

        self.status_label.set_text(
            f"Could not fetch price: {message}"
        )

    def on_refresh_price(
        self,
        button,
    ):
        self.status_label.set_text(
            "Refreshing price..."
        )

        self.refresh_price_async()

    # ---------------------------------------------------------
    # Set wallpaper
    # ---------------------------------------------------------

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

        if (
            self.auto_process is None
            or self.auto_process.poll()
            is not None
        ):
            self.start_button.set_sensitive(
                not busy
            )

    def on_set_wallpaper(
        self,
        button,
    ):
        settings = (
            self.get_current_settings()
        )

        self.status_label.set_text(
            "Generating wallpaper..."
        )

        self.set_busy(True)

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
        self.set_busy(False)

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
        self.set_busy(False)

        self.status_label.set_text(
            f"Wallpaper update failed: {message}"
        )

    # ---------------------------------------------------------
    # Automatic updater
    # ---------------------------------------------------------

    def on_start_auto(
        self,
        button,
    ):
        if (
            self.auto_process is not None
            and self.auto_process.poll()
            is None
        ):
            self.status_label.set_text(
                "Automatic updates are already running."
            )

            return

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
                    [
                        "cryptopaper"
                    ],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
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

        self.status_label.set_text(
            f"Could not start automatic updates: {message}"
        )

    def stop_auto_process_group(
        self,
        force=False,
    ):
        if self.auto_process is None:
            return

        if self.auto_process.poll() is not None:
            return

        try:
            process_group = os.getpgid(
                self.auto_process.pid
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
                f"Could not stop automatic updates: {error}"
            )

    def on_stop_auto(
        self,
        button,
    ):
        if (
            self.auto_process is None
            or self.auto_process.poll()
            is not None
        ):
            self.status_label.set_text(
                "Automatic updates are not running."
            )

            self.start_button.set_sensitive(
                True
            )

            self.stop_button.set_sensitive(
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
        if (
            self.auto_process is not None
            and self.auto_process.poll()
            is None
        ):
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

        if self.stopping_auto:
            self.status_label.set_text(
                "Automatic updates stopped."
            )

        elif return_code == 0:
            self.status_label.set_text(
                "Automatic updates stopped."
            )

        else:
            self.status_label.set_text(
                "cryptopaper stopped unexpectedly."
            )

        self.auto_process = None
        self.stopping_auto = False

        return False

    # ---------------------------------------------------------
    # Window close
    # ---------------------------------------------------------

    def do_close_request(
        self
    ):
        if (
            self.auto_process is not None
            and self.auto_process.poll()
            is None
        ):
            self.stop_auto_process_group(
                force=True
            )

        return False


class CryptoPaperApplication(
    Gtk.Application
):
    def __init__(self):
        super().__init__(
            application_id="com.cryptopaper.app"
        )

    def do_activate(
        self
    ):
        window = CryptoPaperWindow(
            self
        )

        window.present()


def main():
    app = CryptoPaperApplication()

    app.run(None)


if __name__ == "__main__":
    main()
