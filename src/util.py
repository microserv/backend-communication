#!/usr/bin/env python
# -*- coding: utf-8 -*-

IP_DELIM = ":"

def ips_to_string(ip_list):
    return IP_DELIM.join(ip_list)

def split_ips(ip_as_string):
    return ip_as_string.split(IP_DELIM)
