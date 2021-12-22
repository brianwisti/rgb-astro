"""Tasks for exploring Invoke"""

from invoke import task

DEFAULT_NAME = "world"


@task
def setup(c):
    """Get things ready for hello"""
    print("Creating the world")


@task(
    pre=[setup],
    default=True,
    help={"name": "Who or what it being greeted (default {DEFAULT_NAME})"},
)
def hello(c, name=DEFAULT_NAME):
    """
    Print the standard greeting

    "Hello world" is the classic first program to see what a language looks like.
    So of course I used it to understand Invoke.
    """
    print(f"Hello, {name}!")
