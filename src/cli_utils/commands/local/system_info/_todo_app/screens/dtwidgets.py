"""
Date and Time Input Widgets for Textual

This module provides three reusable date/time input widgets that integrate with
the 'dialog' command-line utility for interactive calendar and timebox pickers.

Requirements:
    - The 'dialog' utility must be installed on the system
    - Nerd Fonts (optional, for icons)

Widgets:
    DateInput: Date-only input with calendar picker
    TimeInput: Time-only input with clock picker
    DateTimeInput: Combined date and time input with both pickers

Examples:
    Basic usage in a Textual app:

    >>> from textual.app import App, ComposeResult
    >>> from dialog_example import DateInput, TimeInput, DateTimeInput
    >>>
    >>> class MyApp(App):
    ...     def compose(self) -> ComposeResult:
    ...         yield DateInput()
    ...         yield TimeInput()
    ...         yield DateTimeInput()
    >>>
    >>> if __name__ == "__main__":
    ...     MyApp().run()

    Using just the date picker:

    >>> class MyApp(App):
    ...     def compose(self) -> ComposeResult:
    ...         yield DateInput()
    >>>
    >>> MyApp().run()

    Accessing widget values:

    >>> class MyApp(App):
    ...     def compose(self) -> ComposeResult:
    ...         yield DateInput()
    ...
    ...     def on_mount(self):
    ...         date_input = self.query_one(DateInput)
    ...         input_field = date_input.query_one(Input)
    ...         self.log(f"Current date: {input_field.value}")

Validation:
    All widgets include built-in validation:
    - DateInput: Validates YYYY-MM-DD format
    - TimeInput: Validates HH:MM format (00-23:00-59)
    - DateTimeInput: Validates YYYY-MM-DD HH:MM format

    Invalid inputs are highlighted with a red border, valid inputs with green.
"""
import shutil
import subprocess
from datetime import date, datetime, time
from typing import Optional

from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.validation import ValidationResult, Validator
from textual.widgets import Button, Input, Label, Static

# Icon constants (using nerd fonts)
ICON_CALENDAR = "📅"  # nf-md-calendar
ICON_CLOCK = "🕐"  # nf-md-clock_outline


def pick_date_dialog(default: Optional[datetime] = None) -> Optional[date]:
    """
    Pick a date using dialog, return a date or None.

    :param default: Optional[datetime]
        The default date to display in the dialog. If None, the current date will be used.
    :return: Optional[date]
        The selected date or None if the dialog was cancelled or not available.
    """
    if not shutil.which("dialog"):
        return None

    if default is None:
        default = datetime.now()

    date_cmd = [
        "dialog", "--stdout", "--calendar", "Select a date",
        "0", "0",  # height, width (0 = auto-size)
        str(default.day), str(default.month), str(default.year)
    ]
    date_proc = subprocess.run(
        date_cmd,
        text=True,
        stdout=subprocess.PIPE,  # capture result
        stderr=None,             # let dialog draw to terminal
        stdin=None               # use terminal for input
    )
    if date_proc.returncode != 0:
        return None
    return datetime.strptime(date_proc.stdout.strip(), "%d/%m/%Y").date()


def pick_time_dialog(default: Optional[datetime] = None) -> Optional[time]:
    """
    Pick a time using dialog, return a time or None.

    :param default: Optional[datetime]
        The default time to display in the dialog. If None, the current time will be used.
    :return: Optional[time]
        The selected time or None if the dialog was cancelled or not available.
    """
    if not shutil.which("dialog"):
        return None

    if default is None:
        default = datetime.now()

    time_cmd = [
        "dialog", "--stdout", "--timebox", "Select a time",
        "0", "0",  # height, width (0 = auto-size)
        str(default.hour), str(default.minute), "0"  # Set seconds to 0
    ]
    time_proc = subprocess.run(
        time_cmd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=None,
        stdin=None
    )
    if time_proc.returncode != 0:
        return None
    # Parse and return only HH:MM
    return datetime.strptime(time_proc.stdout.strip(), "%H:%M:%S").time()



class DateValidator(Validator):
    """Validates date in YYYY-MM-DD format."""

    def validate(self, value: str) -> ValidationResult:
        """
        Validate a date string in YYYY-MM-DD format.

        :param value: str
            The date string to validate.
        :return: ValidationResult
            A ValidationResult indicating whether the input is valid or not.
        """
        if not value.strip():
            return self.success()

        try:
            datetime.strptime(value.strip(), "%Y-%m-%d")
            return self.success()
        except ValueError:
            return self.failure("Invalid format. Use YYYY-MM-DD")


class TimeValidator(Validator):
    """Validates time in HH:MM format."""

    def validate(self, value: str) -> ValidationResult:
        """
        Validate a time string in HH:MM format.

        :param value: str
            The time string to validate.
        :return: ValidationResult
            A ValidationResult indicating whether the input is valid or not.
        """
        if not value.strip():
            return self.success()

        try:
            dt = datetime.strptime(value.strip(), "%H:%M")

            if not (0 <= dt.hour <= 23):
                return self.failure("Hour must be between 00 and 23")
            if not (0 <= dt.minute <= 59):
                return self.failure("Minutes must be between 00 and 59")

            return self.success()
        except ValueError:
            return self.failure("Invalid format. Use HH:MM")


class DateTimeValidator(Validator):
    """Validates datetime in YYYY-MM-DD HH:MM format."""

    def validate(self, value: str) -> ValidationResult:
        """
        Validate a datetime string in YYYY-MM-DD HH:MM format.

        :param value: str
            The datetime string to validate.
        :return: ValidationResult
            A ValidationResult indicating whether the input is valid or not.
        """
        if not value.strip():
            return self.success()

        try:
            dt = datetime.strptime(value.strip(), "%Y-%m-%d %H:%M")

            if not (0 <= dt.hour <= 23):
                return self.failure("Hour must be between 00 and 23")
            if not (0 <= dt.minute <= 59):
                return self.failure("Minutes must be between 00 and 59")

            return self.success()
        except ValueError:
            return self.failure("Invalid format. Use YYYY-MM-DD HH:MM")


class DateInput(Static):
    """Date input widget with calendar picker button."""

    DEFAULT_CSS = """
    DateInput Horizontal {
        height: auto;
        align: left middle;
    }

    DateInput Input {
        width: 1fr;
    }

    DateInput Input.-invalid {
        border: tall red;
    }

    DateInput Input.-valid {
        border: tall green;
    }

    DateInput Button.icon-btn {
        width: 3;
        min-width: 3;
        padding: 0 0;
    }
    """

    def __init__(
        self,
        label: str = "Date:",
        value: str = "",
        input_id: str = "dateinput",
        input_classes: str = "",
        label_classes: str = "",
        container_id: str = "",
        container_classes: str = "",
        *args,
        **kwargs
    ) -> None:
        """Initialize the DateInput widget.

        Args:
            label: The label text to display before the input field
            value: The initial value for the input field (YYYY-MM-DD format)
            input_id: The ID for the input field
            input_classes: Additional CSS classes for the input field
            label_classes: Additional CSS classes for the label
            container_id: Optional ID for the internal Horizontal container
            container_classes: Additional CSS classes for the internal container
            *args: Additional positional arguments for Static
            **kwargs: Additional keyword arguments for Static
        """
        super().__init__(*args, **kwargs)
        self._label = label
        self._value = value
        self._input_id = input_id
        self._input_classes = f"dateinput {input_classes}".strip()
        self._label_classes = label_classes
        self._container_id = container_id
        self._container_classes = container_classes

    def compose(self) -> ComposeResult:
        """
        Compose the date input widget.

        The compose method is responsible for generating the content of the widget.
        In this case, it generates a horizontal layout with a label, an input field,
        and a button. The input field is used to input a date in YYYY-MM-DD format,
        and the button is used to open a calendar picker dialog.

        :return: ComposeResult
            A ComposeResult containing the composed content of the widget.
        """
        container_kwargs = {}
        if self._container_id:
            container_kwargs["id"] = self._container_id
        if self._container_classes:
            container_kwargs["classes"] = self._container_classes

        with Horizontal(**container_kwargs):
            if self._label:
                label_kwargs = {}
                if self._label_classes:
                    label_kwargs["classes"] = self._label_classes
                yield Label(self._label, **label_kwargs)
            yield Input(
                placeholder="YYYY-MM-DD",
                id=self._input_id,
                classes=self._input_classes,
                value=self._value,
                validators=[DateValidator()]
            )
            yield Button(ICON_CALENDAR, id="pick-date", classes="icon-btn")

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """
        Called when a button is pressed.

        If the button is the calendar picker (id="pick-date"), it will open a
        calendar picker dialog and update the input field with the picked date.

        :param event: Button.Pressed
            The button press event.
        :return: None
        """
        if event.button.id == "pick-date":
            input_widget: Input = self.query_one(f"#{self._input_id}", Input)
            with self.app.suspend():
                picked_date: Optional[date] = pick_date_dialog()
            if picked_date:
                input_widget.value = picked_date.strftime("%Y-%m-%d")


class TimeInput(Static):
    """Time input widget with clock picker button."""

    DEFAULT_CSS = """
    TimeInput Horizontal {
        height: auto;
        align: left middle;
    }

    TimeInput Input {
        width: 1fr;
    }

    TimeInput Input.-invalid {
        border: tall red;
    }

    TimeInput Input.-valid {
        border: tall green;
    }

    TimeInput Button.icon-btn {
        width: 3;
        min-width: 3;
        padding: 0 0;
    }
    """

    def __init__(
        self,
        label: str = "Time:",
        value: str = "",
        input_id: str = "timeinput",
        input_classes: str = "",
        label_classes: str = "",
        container_id: str = "",
        container_classes: str = "",
        *args,
        **kwargs
    ) -> None:
        """Initialize the TimeInput widget.

        Args:
            label: The label text to display before the input field
            value: The initial value for the input field (HH:MM format)
            input_id: The ID for the input field
            input_classes: Additional CSS classes for the input field
            label_classes: Additional CSS classes for the label
            container_id: Optional ID for the internal Horizontal container
            container_classes: Additional CSS classes for the internal container
            *args: Additional positional arguments for Static
            **kwargs: Additional keyword arguments for Static
        """
        super().__init__(*args, **kwargs)
        self._label = label
        self._value = value
        self._input_id = input_id
        self._input_classes = f"timeinput {input_classes}".strip()
        self._label_classes = label_classes
        self._container_id = container_id
        self._container_classes = container_classes

    def compose(self) -> ComposeResult:
        """
        Compose the content of the widget.

        Composes a Horizontal widget containing a label, an input field
        and a button. The input field has a placeholder of "HH:MM" and
        is validated with a TimeValidator. The button has an icon of a clock
        and an id of "pick-time".

        :return: ComposeResult
            A ComposeResult containing the composed content of the widget.
        """
        container_kwargs = {}
        if self._container_id:
            container_kwargs["id"] = self._container_id
        if self._container_classes:
            container_kwargs["classes"] = self._container_classes

        with Horizontal(**container_kwargs):
            if self._label:
                label_kwargs = {}
                if self._label_classes:
                    label_kwargs["classes"] = self._label_classes
                yield Label(self._label, **label_kwargs)
            yield Input(
                placeholder="HH:MM",
                id=self._input_id,
                classes=self._input_classes,
                value=self._value,
                validators=[TimeValidator()]
            )
            yield Button(ICON_CLOCK, id="pick-time", classes="icon-btn")

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """
        Called when a button is pressed.

        If the button is the clock picker (id="pick-time"), it will open a
        clock picker dialog and update the input field with the picked time.

        :param event: Button.Pressed
            The button press event.
        :return: None
        """
        if event.button.id == "pick-time":
            input_widget: Input = self.query_one(f"#{self._input_id}", Input)
            with self.app.suspend():
                picked_time: Optional[time] = pick_time_dialog()
            if picked_time:
                input_widget.value = picked_time.strftime("%H:%M")


class DateTimeInput(Static):
    """Hybrid input that can use dialog for date/time selection."""

    DEFAULT_CSS = """
    DateTimeInput Horizontal {
        height: auto;
        align: left middle;
    }

    DateTimeInput Input {
        width: 1fr;
    }

    DateTimeInput Input.-invalid {
        border: tall red;
    }

    DateTimeInput Input.-valid {
        border: tall green;
    }

    DateTimeInput Button.icon-btn {
        width: 3;
        min-width: 3;
        padding: 0 0;
    }
    """

    def __init__(
        self,
        label: str = "Date/Time:",
        value: str = "",
        input_id: str = "dtinput",
        input_classes: str = "",
        label_classes: str = "",
        container_id: str = "",
        container_classes: str = "",
        *args,
        **kwargs
    ) -> None:
        """Initialize the DateTimeInput widget.

        Args:
            label: The label text to display before the input field
            value: The initial value for the input field (YYYY-MM-DD HH:MM format)
            input_id: The ID for the input field
            input_classes: Additional CSS classes for the input field
            label_classes: Additional CSS classes for the label
            container_id: Optional ID for the internal Horizontal container
            container_classes: Additional CSS classes for the internal container
            *args: Additional positional arguments for Static
            **kwargs: Additional keyword arguments for Static
        """
        super().__init__(*args, **kwargs)
        self._label = label
        self._value = value
        self._input_id = input_id
        self._input_classes = f"dtinput {input_classes}".strip()
        self._label_classes = label_classes
        self._container_id = container_id
        self._container_classes = container_classes

    def compose(self) -> ComposeResult:
        """
        Compose the datetime input widget.

        The compose method is responsible for generating the content of the widget.
        In this case, it generates a horizontal layout with a label, an input field,
        and two buttons. The input field is used to input a date and time in
        YYYY-MM-DD HH:MM format, and the buttons are used to open a calendar
        picker dialog and a clock picker dialog respectively.

        :return: ComposeResult
            A ComposeResult containing the composed content of the widget.
        """
        container_kwargs = {}
        if self._container_id:
            container_kwargs["id"] = self._container_id
        if self._container_classes:
            container_kwargs["classes"] = self._container_classes

        with Horizontal(**container_kwargs):
            if self._label:
                label_kwargs = {}
                if self._label_classes:
                    label_kwargs["classes"] = self._label_classes
                yield Label(self._label, **label_kwargs)
            yield Input(
                placeholder="YYYY-MM-DD HH:MM",
                id=self._input_id,
                classes=self._input_classes,
                value=self._value,
                validators=[DateTimeValidator()]
            )
            yield Button(ICON_CALENDAR, id="pick-date", classes="icon-btn")
            yield Button(ICON_CLOCK, id="pick-time", classes="icon-btn")


    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """
        Called when a button is pressed.

        If the button is the calendar picker (id="pick-date"), it will open a
        calendar picker dialog and update the input field with the picked date and
        existing time if present, otherwise use current time.

        If the button is the clock picker (id="pick-time"), it will open a
        clock picker dialog and update the input field with the picked time and
        existing date if present, otherwise use current date.

        :param event: Button.Pressed
            The button press event.
        :return: None
        """
        input_widget: Input = self.query_one(f"#{self._input_id}", Input)
        current_value: str = input_widget.value.strip()

        if event.button.id == "pick-date":
            # Suspend Textual temporarily
            with self.app.suspend():
                picked_date: Optional[date] = pick_date_dialog()
            if picked_date:
                # Keep existing time if present, otherwise use current time
                if current_value and " " in current_value:
                    time_part: str = current_value.split(" ", 1)[1]
                else:
                    time_part: str = datetime.now().strftime("%H:%M")
                input_widget.value = f"{picked_date.strftime('%Y-%m-%d')} {time_part}"

        elif event.button.id == "pick-time":
            with self.app.suspend():
                picked_time: Optional[time] = pick_time_dialog()
            if picked_time:
                # Keep existing date if present, otherwise use current date
                if current_value and " " in current_value:
                    date_part: str = current_value.split(" ", 1)[0]
                else:
                    date_part: str = datetime.now().strftime("%Y-%m-%d")
                input_widget.value = f"{date_part} {picked_time.strftime('%H:%M')}"