#!/usr/bin/env python
# -*- coding: utf-8 -*-

from geopy.geocoders import GoogleV3

###############
# GEOcode 
###############

def geocode(_address):
    geolocator = GoogleV3()
    print _address
    geocodes = geolocator.geocode(_address,exactly_one=True)
    # for g in geocodes:
    #     print g
    return geocodes