import requests
import warnings

from .answers import Status


warnings.filterwarnings("ignore")


CMS = ["OpenCart", "Bitrix", "Simpla", "CS-Cart"]
HEADERS = {
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"
}


class Detect:
	def __init__(self, timeout=10):
		self.timeout = timeout

		self.domain = None
		self.index = None

	def run(self, domain):
		self.domain = domain
		self.index = None

		try:
			status = self.by_index_headers()  # Определение CMS по заголовкам ответа index.php
			if status: return status

			status = self.by_index_page()  # Определение CMS по index.php
			if status: return status

			status = self.by_unique_files()  # Определение CMS по уникальным файлам
			if status: return status

			status = self.by_admin_page()  # Определегние CMS по административным панелям
			if status: return status

			return Status(42)

		except requests.exceptions.Timeout:
			return Status(40)

		except requests.exceptions.ConnectionError:
			return Status(41)

	def by_index_headers(self):
		if self.index is None:
			self.index = self.request()

		headers = self.index.headers
		
		if "Set-Cookie" in headers:
			cookies = headers["Set-Cookie"].lower()

			""" OpenCart (ocStore) """
			if "ocsessid" in cookies:
				return Status(cms="OpenCart", content="cookies")

			""" Bitrix """
			if "bitrix" in cookies:
				return Status(cms="Bitrix", content="cookies")

		""" Bitrix """
		if "X-Bitrix-Composite" in headers:
			return Status(cms="Bitrix", content="headers")

		if "X-Powered-CMS" in headers:
			powered_cms = headers["X-Powered-CMS"]

			""" Bitrix """
			if "Bitrix" in powered_cms:
				return Status(cms="Bitrix", content="headers")

		return None

	def by_index_page(self):
		if self.index is None:
			self.index = self.request()

		""" OpenCart (ocStore) """
		if "catalog/view/theme/default/stylesheet/" in self.index.text:
			return Status(cms="OpenCart", content="by_index_page")

		return None

	def by_admin_page(self):
		admin = self.request("/admin/")

		""" OpenCart (ocStore) """
		if "/admin/index.php?route=common/login" in admin.text:
			return Status(cms="OpenCart", content="by_admin_page")

		return None

	def by_unique_files(self):
		""" OpenCart (ocStore) """
		opencart_ico = self.request("/image/catalog/opencart.ico")
		if opencart_ico.status_code == 200 and "icon" in opencart_ico.headers["Content-Type"]:
			return Status(cms="OpenCart", content="by_unique_files")

		return None

	def request(self, path=''):
		return requests.get(f"https://{self.domain}{path}", allow_redirects=True, verify=False, timeout=self.timeout, headers=HEADERS)
