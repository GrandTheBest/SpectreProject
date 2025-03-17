from telethon.tl.functions.users import GetFullUserRequest
import time

from vendor.misc import *
from vendor.core.validator import Validator

from datetime import datetime

from app import config

async def main():
	while True:
		await client.get_dialogs()
		target = await client.get_entity(config.target)

		full_target = await client(GetFullUserRequest(target.id))

		validator = Validator(filename="BASE_DATA", entity=target, full_entity=full_target,
		                      data_keys=["first_name",
                                           "last_name",
                                           "id", "username",
                                           "premium", "scam",
                                           "verified",
                                           "phone"],
		                      full_data_keys=["blocked",
		                                      "business_location.address",
		                                      "stargifts_count",
		                                      "about"], access_level=3, skip_errors=False)

		base_output = await validator.data_validation()

		date = datetime.now()
		print(f"[{date.strftime('%Y.%m.%d %H:%M:%S')}] Base Output: {str(base_output)}")

		time.sleep(config.delay)

with client:
	client.loop.run_until_complete(main())
