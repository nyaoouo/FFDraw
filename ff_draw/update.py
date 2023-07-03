import logging
import os
import pathlib
import re

import requests

update_host = {
    'github': 'https://raw.githubusercontent.com/',
    'fastgit': 'https://raw.fastgit.org/',
}
update_uri = 'nyaoouo/FFDraw/master/version.txt'

logger = logging.getLogger('UpdateChecker')

update_desc = [
    'major',
    'feature',
    'bugfix'
]


def check(session: requests.Session, select_host='github'):
    try:
        is_latest = _check(session, select_host)
    except Exception as e:
        logger.warning('check update fail, please check network connection or change update source', exc_info=e)


def _check(session: requests.Session, select_host='github'):
    remote_version = local_version = 0, 0, 0
    if (local_version_path := pathlib.Path(os.environ['ExcPath']) / 'version.txt').exists():
        if _match := re.match(r'^(\d+)\.(\d+)\.(\d+)$', local_version_path.read_text()):
            local_version = int(_match.group(1)), int(_match.group(2)), int(_match.group(3)),
    (res := session.get(update_host[select_host] + update_uri)).raise_for_status()
    if _match := re.match(r'^(\d+)\.(\d+)\.(\d+)$', res.text):
        remote_version = int(_match.group(1)), int(_match.group(2)), int(_match.group(3)),
    logger.info(f'local version: {local_version}    remote version: {remote_version}')
    for l, r, d in zip(local_version, remote_version, update_desc):
        if r > l:
            logger.warning(f'there is a {d} update from {local_version} => {remote_version}')
            return False
        elif r < l:  # custom source?
            return True
    return True
