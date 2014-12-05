# -*- coding: utf-8 -*-	

import sys, json
from functions import *

reload(sys)
sys.setdefaultencoding("utf-8")

songlist = refreshSongList()

print songlist
