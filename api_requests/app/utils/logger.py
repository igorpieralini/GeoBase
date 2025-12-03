import os
import datetime
from app.utils.config import cfg

def log_message(msg, level="INFO"):
	log_cfg = cfg.get('logging', {})
	log_dir = log_cfg.get('path', 'logs/')
	log_file = os.path.join(log_dir, 'app.log')

	if not os.path.exists(log_dir):
		os.makedirs(log_dir)

	timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	log_line = f"[{timestamp}] [{level}] {msg}"

	with open(log_file, 'a', encoding='utf-8') as f:
		f.write(log_line + '\n')

	print(log_line)
