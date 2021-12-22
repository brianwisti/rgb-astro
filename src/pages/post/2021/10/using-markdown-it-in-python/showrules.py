import rich
from markdown_it import MarkdownIt

presets = ["zero", "commonmark", "gfm-like", "js-default"]

for preset in presets:
    md = MarkdownIt(preset, {"linkify": True, "html": True, "typographer": False})
    active_rules = md.get_active_rules()
    all_rules = md.get_all_rules()
    difference = {
        category: set(all_rules[category]) - set(active_rules[category])
        for category in all_rules
    }
    rich.print(f"{preset} enabled: {active_rules}")
    rich.print(f"{preset} disabled: {difference}")
