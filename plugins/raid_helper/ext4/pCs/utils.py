import logging
import math

import glm

from raid_helper import utils as raid_utils
from raid_helper.utils.typing import *
from raid_helper.data import special_actions

pCs = raid_utils.MapTrigger(1154)

center = glm.vec3(100, 0, 100)

logger = logging.getLogger('raid_helper/pCs')
