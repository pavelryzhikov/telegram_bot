#!/usr/bin/env python
# -*- coding: utf-8 -*
from speed_dating.views import ping,next_round_auto, create_group_auto 
import datetime
now = datetime.datetime.now()

create_group_auto()
next_round_auto()
if now.hour%5==0 and now.minute<5:
    ping()

#next_round_auto
