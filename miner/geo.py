#!/usr/bin/env python
# -*- coding: utf-8 -*-

from geopy.geocoders import GoogleV3

###############
# GEOcode 
###############

def geocode(address):
    geolocator = GoogleV3()
    geocodes = geolocator.geocode(address.encode('utf-8'),exactly_one=False)
    # for g in geocodes:
    #     print g
    return geocodes