from datetime import datetime
from sfmanager import FileManager, FilesManager

from vendor.misc import FILE_NAMES

access_level = 3

# Generic filemanager
generic_manager = FilesManager(level=2)

# Not universal filemanagers
base_data = FileManager(filename=FILE_NAMES["base-data"], level=access_level) # data/BASE_DATA

# Return current string with date and time
def time_string(_input: str) -> str:
	_date = datetime.now()
	return f"[{_date.strftime('%Y.%m.%d %H:%M:%S')}] {_input}"