import os

# Base for uncompress and plugins.
base_path = os.path.dirname(os.path.abspath(__file__))

# Uncompresser.
uncompress_path = f"{base_path}/uncompresser/amxx_uncompress.exe"

# Path to .amxx files directory.
plugins_path = f"{base_path}/plugins"

# Custom output path.
output_path = f"{base_path}/output.txt"

# Removes memory address and some unnecesary stuff outputed.
truncate = 17

# Interval of checking for the .memory files when uncompressing.
uncompress_delay = 0.1

# Timeout of 'uncompress' function.
# Used when file does not open or it fails to uncompress.
uncompress_timeout = 20.0

# Determines how long it will take the program to
# retry deleting .raw/.memory files.
# Applies only when PermissionError exception is raised.
file_remove_delay = 1.0
