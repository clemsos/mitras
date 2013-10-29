#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bulbs.model import Node, Relationship
from bulbs.property import String, Integer, DateTime, Null
from bulbs.utils import current_datetime

class User(Node):
    element_type = "user"
    uid = Integer(nullable=False)
    name = String()
    gender = String() # Self-reported gender
    verified = Null() # verified - VIP status ("V")

class isFromProvince(Relationship):
    #Self-reported province of origin
    label="isFromProvince"

class Province(Node):
    element_type="province"
    name=String()
    code_weibo=String()
    
class Publishs(Relationship):
    label = "posts"
    created = DateTime(default=current_datetime, nullable=False)