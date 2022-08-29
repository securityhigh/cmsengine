import sys

from colorama import Style, Fore


def error(text):
	print(f"{Style.BRIGHT}{Fore.RED}[error]{Style.RESET_ALL}{Style.BRIGHT} {text}")


def ok(text):
	print(f"{Style.BRIGHT}{Fore.MAGENTA}[ok]{Style.RESET_ALL}{Style.BRIGHT} {text}")


def info(text):
	print(f"{Style.BRIGHT}{Fore.YELLOW}[info]{Style.RESET_ALL}{Style.BRIGHT} {text}")


def die(text, ok=False):
	if ok: ok(text)
	else: error(text)

	sys.exit(0)
