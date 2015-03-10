import sh
from path import Path
import os

d = Path('zukan_workspace/web/images/ichiran')

dest = Path('zukan_workspace/web/images')

for f in d.files('*.jpg'):
	name = str(f.name)
	fish_name = name.replace('.jpg', '')
	destination = os.path.join(dest, fish_name)
	try:
		os.mkdir(destination)
	except Exception:
		pass
	new_file = fish_name + "-ichiran.jpg"
	f.copy(os.path.join(destination, new_file))


