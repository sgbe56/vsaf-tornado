import os
from pathlib import Path

settings = {
    'static_path': os.path.abspath(os.path.dirname(__file__)),
    'cookie_secret': 'd5feffcec36ab8468da4eccf4a8cab75',
    # 'xsrf_cookies': True,
    'db_name': 'simple_pw.db',
    'template_path': str(Path('./app/templates'))
}

