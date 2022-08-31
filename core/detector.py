import requests
import warnings

from .answers import Status


warnings.filterwarnings("ignore")


CMS = ["OpenCart", "Bitrix", "Simpla", "CS-Cart", "PrestaShop", "Webasyst"]
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

			status = self.by_admin_page()  # Определение CMS по админ-панелям
			if status: return status

			return Status(42)

		except requests.exceptions.Timeout:
			return Status(40)

		except requests.exceptions.ConnectionError:
			return Status(41)

		except requests.exceptions.TooManyRedirects:
			return Status(43)

	def by_index_headers(self):
		if self.index is None:
			self.index = self.request()

		headers = self.index.headers

		""" Bitrix """
		if "X-Bitrix-Composite" in headers:
			return Status(cms="Bitrix", content="headers")
		
		if "Set-Cookie" in headers:
			cookies = headers["Set-Cookie"].lower()

			""" OpenCart (ocStore) """
			if "ocsessid" in cookies:
				return Status(cms="OpenCart", content="cookies")

			""" Bitrix """
			if "bitrix" in cookies:
				return Status(cms="Bitrix", content="cookies")

			""" PrestaShop """
			if "prestashop" in cookies:
				return Status(cms="PrestaShop", content="cookies")

		if "X-Powered-CMS" in headers:
			powered_cms = headers["X-Powered-CMS"]

			""" Bitrix """
			if "Bitrix" in powered_cms:
				return Status(cms="Bitrix", content="headers")

		if "Powered-By" in headers:
			powered_cms = headers["Powered-By"]

			""" PrestaShop """
			if "PrestaShop" in powered_cms:
				return Status(cms="PrestaShop", content="headers")

		return None

	def by_index_page(self):
		if self.index is None:
			self.index = self.request()

		""" OpenCart (ocStore) """
		if "catalog/view/theme/default/stylesheet/" in self.index.text:
			return Status(cms="OpenCart", content="index_page")

		""" Webasyst """
		#if "/wa-data/public/site/themes/" in self.index.text:
		#	return Status(cms="Webasyst", content="index_page")

		return None

	def by_admin_page(self):
		admin = self.request("/admin/")

		""" OpenCart (ocStore) """
		if "/admin/index.php?route=common/login" in admin.text:
			return Status(cms="OpenCart", content="admin_page")

		""" Simpla """
		simpla = self.request("/simpla/")
		if "WWW-Authenticate" in simpla.headers and "Simpla" in simpla.headers["WWW-Authenticate"] \
				or "/password.php" in simpla.url or "module=LoginAdmin" in simpla.url or simpla.status_code == 401:
			return Status(cms="Simpla", content="admin_headers")

		return None

	def by_unique_files(self):
		""" CS-Cart """
		store_closed = self.request("/store_closed.html")
		if store_closed.status_code == 200 and "bigEntrance" in store_closed.text:
			return Status(cms="CS-Cart", content="unique_files")

		""" PrestaShop """
		tools_js = self.request("/js/tools.js")
		if tools_js.status_code == 200:
			if "PrestaShop" in tools_js.text or "((!obj.value || obj.value == text2) ? text1 : text2);" in tools_js.text:
				return Status(cms="PrestaShop", content="unique_files") 

		""" OpenCart (ocStore) """
		opencart_ico = self.request("/image/catalog/opencart.ico")
		if opencart_ico.status_code == 200 and "icon" in opencart_ico.headers["Content-Type"] and "imunify360" not in opencart_ico.headers["Server"]:
			return Status(cms="OpenCart", content="unique_files")

		""" Webasyst """
		wa_php = self.request("/wa.php")
		if wa_php.status_code == 200 and "cli only" in wa_php.text.lower():
			return Status(cms="Webasyst", content="unique_files")

		return None

	def request(self, path='', redirects=True):
		r = requests.get(f"http://{self.domain}{path}", allow_redirects=redirects, verify=False, timeout=self.timeout, headers=HEADERS)
		return r
