import argparse

parser = argparse.ArgumentParser(description="Yet Another Recursive Descent Parser")
parser.add_argument(
    "-c",
    "--color",
    action=argparse.BooleanOptionalAction,
    help="Whether to enable color. Defaults to False",
)


args = parser.parse_args()


class Config:
    def __init__(self, color: bool) -> None:
        self.colors_enabled = color

    def cprint(self, text: str, *args, **kwargs):
        if self.colors_enabled:
            from termcolor import cprint as ccprint

            ccprint(text, *args, **kwargs)
        else:
            print(text)


config = Config(args.color)
cprint = config.cprint
