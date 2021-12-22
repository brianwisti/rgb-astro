from rich import print
from rich.panel import Panel
from rich.markdown import Markdown

md = Markdown("**Hello**, *World*.")
print(Panel(md))
