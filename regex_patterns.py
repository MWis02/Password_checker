import re

MENU_MAIN_RE = re.compile(r'^[123]$')
MENU_YES_NO_RE = re.compile(r'^[12]$')
PASSWORD_RE = re.compile(r'^.+$')
EMAIL_RE = re.compile(r'^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$')
PATH_RE = re.compile(r'^[^\x00-\x1f<>|?*]+$')
BATCH_WITH_EMAIL_RE = re.compile(
    r'^(?P<password>[^,\s].*?),(?P<email>[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,})$'
)

