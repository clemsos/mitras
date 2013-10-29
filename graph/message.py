#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bulbs.model import Node, Relationship
from bulbs.property import String, Integer, DateTime, Null
from bulbs.utils import current_datetime

class Message(Node):
       
    element_type = "message"

    mid = Integer() # Unique pseudo message ID
    hasImage = Null() # With image? (1= Yes, 0=No)
    source = String(nullable=False) #The application name of the client program
    text = String(nullable=False) # body of the message
    created_at = DateTime(default=current_datetime, nullable=False) # Original posting time
    deleted_last_seen = DateTime() #The last seen time before this message was missing from the user timeline
    permission_denied = Null() # 'permission denied' status is marked when the message was found missing in the timeline and the API return message was 'permission denied' - See details in (Fu, Chan, Chau 2013)

    # Available Relationships
    # retweeted_status_mid - Pseudo message ID of the original message (Only available if the row of interest is a retweet)
    # uid - Pseudo user ID
    # retweeted_uid - Pseudo user ID of the original poster (Only available if the row of interest is a retweet)
    # geo - GIS information. Please refer to the Sina Weibo API documentation: http://goo.gl/Um8SS

class Coordinate(Node):
    element_type = "coordinate"
    lat=Integer()
    lon=Integer()

class GeoTag(Node):
    element_type = "geotag"
    name = String()

class containsGeoInfo(Relationship):
    label = "containsGeoInfo"
    created = DateTime(default=current_datetime, nullable=False)
    occurence = Integer()

class IsLocated(Relationship):
    label = "isLocated"
    created = DateTime(default=current_datetime, nullable=False)

class Retweets(Relationship):
    label = "retweets"
    created = DateTime(default=current_datetime, nullable=False)