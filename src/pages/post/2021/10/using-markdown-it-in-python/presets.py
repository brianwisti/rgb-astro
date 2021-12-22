"""Display the default settings for each markdown-it-py preset."""

from markdown_it import presets
from tabulate import tabulate

def for_display(value):
    """Return the value formatted for in-table display"""

    if value is True:
        return "enabled"

    if value:
        return f"`{value}`"

    return "—"


def options_table():
    """Return a markdown table of markdown-it-py preset options."""

    options = {}

    preset_names = [
        attribute for attribute in dir(presets) if not attribute.startswith("__")
    ]

    for preset_name in preset_names:
        preset = getattr(presets, preset_name)
        option_values = preset.make()["options"]

        for option, value in option_values.items():
            value_list = options.get(option, [])
            value_list.append(for_display(value))
            options[option] = value_list

    table_rows = []

    for option, values in options.items():
        table_rows.append([for_display(option), *values])

    header_row = ["Option", *[for_display(preset) for preset in preset_names]]
    table = tabulate(table_rows, header_row, tablefmt="github")
    return table

if __name__ == "__main__":
    print(options_table())
