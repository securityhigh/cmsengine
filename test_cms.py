#!/usr/bin/python

import sys

from os.path import exists

from core.detector import Detect, CMS
from core.message import *


def main(cms):
	if cms in CMS:
		if exists(f"tests/{cms}.txt"):
			with open(f"tests/{cms}.txt") as f:
				items = f.readlines()
				detector = Detect()

				ok(f"Items: {len(items)}")
				for item in items:
					item = item.strip()
					answer = detector.run(item)

					if answer.status_code == 20:
						if answer.name == cms:
							ok(f"{item}")

						else:
							error(f"{item}: {answer.name}, Invalid CMS")

					elif answer.status_code == 44:
						info(f"{item}: {answer.status_code}, {answer.status} ({answer.content})")

					elif answer.status_code == 42:
						error(f"{item}: {answer.status_code}, {answer.status}")

					else:
						info(f"{item}: {answer.status_code}, {answer.status}")

		else:
			die("File not found fot this CMS")

	else:
		die("This CMS is not in the database")


if __name__ == "__main__":
	if len(sys.argv) != 2:
		die("python3 test_cms.py <CMS>")

	try:
		main(sys.argv[1])

	except KeyboardInterrupt:
		...
