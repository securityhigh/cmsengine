STATUS = {
	20: "Successfully CMS detected",
	
	30: "Redirected to other URL",

	40: "Connection timeout error",
	41: "Connection error",
	42: "CMS not found",
	43: "Too many redirects",
}


class Status:
	def __init__(self, status_code=20, content=None, cms=None):
		self.status_code = status_code
		self.status = STATUS[self.status_code]
		
		self.name = cms
		self.content = content
