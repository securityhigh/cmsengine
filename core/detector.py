import requests
import warnings

from .answers import Status


warnings.filterwarnings("ignore")


def run(domain, timeout=10):
	try:
		index = requests.get(f"https://{domain}", allow_redirects=True, verify=False, timeout=timeout)
		headers = index.headers

		return Status(cms="none")

	except requests.exceptions.Timeout:
		return Status(40)

	except requests.exceptions.ConnectionError:
		return Status(41)
