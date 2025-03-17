from telethon import TelegramClient

from vendor.init import api_id, api_hash, app_version

client = TelegramClient('cache-v1', api_id=api_id, api_hash=api_hash, app_version=app_version)

BASE_OPTIONS = [
	"First name",
	"Last name",
	"ID",
	"Username",
	"Premium",
	"Scam",
	"Verified",
	"Phone",
	"Blocked",
	"Address",
	"Stargifts count",
	"Bio",
	"Birthday"
]

DATA_DIR = "data"

FILE_NAMES = {
	"base-data": f"{DATA_DIR}/BASE_DATA",
}