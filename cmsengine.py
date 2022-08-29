#!/usr/bin/python

import sys

from core import detector
from core.message import *


def main(domain):
	cms = detector.run(domain)
	
	if cms.status_code == 20:
		ok(cms.name)

	else:
		error(cms.status)


if __name__ == "__main__":
	if len(sys.argv) != 2:
		die("python3 cmsengine.py <DOMAIN>")

	main(sys.argv[1])
