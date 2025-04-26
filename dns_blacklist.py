#!/usr/bin/env python
from __future__ import print_function, with_statement
import sys
import socket
import re
import codecs
import os

__author__ = 'Ethan Robish'

# TODO:
# add command line argument to resolve hostnames to IP addresses (slow)
# add command line argument to resolve IP addresses to hostnames (slow)
# add ability to specify DNS server
# tell which blacklist the item was found in
# tell which input file the item was in
# for now can do: grep -n IP_or_domain bad_lists/* && grep -n IP_or_domain check/*
# document the source of each included blacklist
# allow updating of blacklists
# add ability to query online blacklists (slow)
# add ability to specify CIDR notation in the blacklists and match a single IP from within the IP block
# create a readme

USAGE = """\
Usage: %s blacklist_directory check_directory

blacklist_directory - directory containing the blacklist files
check_directory     - directory containing the files to check against the blacklists
""" % (sys.argv[0])

# source: StackOverflow
ipv4_cidr_regex = re.compile(r"""(
    (
        (
            [0-9]
            |[1-9][0-9]
            |1[0-9]{2}
            |2[0-4][0-9]
            |25[0-5]
        )
        \.
    ){3}
    (
        25[0-5]
        |2[0-4][0-9]
        |1[0-9]{2}
        |[1-9][0-9]
        |[0-9]
    )
    (/(3[012]|[12]\d|\d))?
)
\D                              # end with a non-digit character
""", re.VERBOSE)

# source: http://stackoverflow.com/a/17871737
# with modifications (moved last line in regex)
ipv6_regex = re.compile(r"""(
    (
        ([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|          # 1:2:3:4:5:6:7:8
        ([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|         # 1::8             1:2:3:4:5:6::8  1:2:3:4:5:6::8
        ([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|  # 1::7:8           1:2:3:4:5::7:8  1:2:3:4:5::8
        ([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|  # 1::6:7:8         1:2:3:4::6:7:8  1:2:3:4::8
        ([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|  # 1::5:6:7:8       1:2:3::5:6:7:8  1:2:3::8
        ([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|  # 1::4:5:6:7:8     1:2::4:5:6:7:8  1:2::8
        [0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|       # 1::3:4:5:6:7:8   1::3:4:5:6:7:8  1::8  
        :((:[0-9a-fA-F]{1,4}){1,7}|:)|                     # ::2:3:4:5:6:7:8  ::2:3:4:5:6:7:8 ::8       ::     
        fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|     # fe80::7:8%eth0   fe80::7:8%1     (link-local IPv6 addresses with zone index)
        ::(ffff(:0{1,4}){0,1}:){0,1}
        ((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]).){3,3}
        (25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|          # ::255.255.255.255   ::ffff:255.255.255.255  ::ffff:0:255.255.255.255  (IPv4-mapped IPv6 addresses and IPv4-translated addresses)
        ([0-9a-fA-F]{1,4}:){1,4}:
        ((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]).){3,3}
        (25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|          # 2001:db8:3:4::192.0.2.33  64:ff9b::192.0.2.33 (IPv4-Embedded IPv6 Address)
        ([0-9a-fA-F]{1,4}:){1,7}:                          # 1::                              1:2:3:4:5:6:7::
    )
    (/(12[0-8]|1[0-1][0-9]|\d\d|\d))?
)""", re.VERBOSE)

hostname_regex = re.compile("""(
    (
        (
            [a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9]|
            [a-zA-Z0-9]
        )
        \.
    )+
    (
        [A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9]|
        [A-Za-z0-9]
    )
)""", re.VERBOSE)

def resolve_hostname(d):
    """
    This method returns an array containing
    one or more IP address strings that respond
    as the given domain name

    source: http://stackoverflow.com/questions/3837744/how-to-resolve-dns-in-python
    """
    try:
        data = socket.gethostbyname_ex(d)
        return data[2]
    except Exception:
        # fail gracefully!
        return []

def parse_file(filename):
    
    # handle files with UTF encodings
    # source: http://stackoverflow.com/a/13591421
    bytes = min(32, os.path.getsize(filename))
    raw = open(filename, 'rb').read(bytes)

    if raw.startswith(codecs.BOM_UTF8):
        encoding = 'utf-8-sig'
    elif raw.startswith(codecs.BOM_UTF16):
        encoding = 'utf-16'
    elif raw.startswith(codecs.BOM_UTF32):
        encoding = 'utf-32'
    else:
        encoding = 'utf-8'

    ip_set = set()
    hostname_set = set()
    with codecs.open(filename, encoding=encoding) as inf:
        for line in inf:
            for ip in ipv6_regex.finditer(line):
                #print('IPv6:', ip.group(1))
                ip_set.add(ip.group(1))
                # remove the IP so it doesn't trigger a hostname or IPv4 match
                line = line.replace(ip.group(1), '', 1)
        
            for ip in ipv4_cidr_regex.finditer(line):
                #print('IPv4', ip.group(1))
                ip_set.add(ip.group(1))
                # remove the IP so it doesn't trigger a hostname match
                line = line.replace(ip.group(1), '', 1)

            for hostname in hostname_regex.finditer(line):
                #print('Hostname:', hostname.group(1))
                hostname_set.add(hostname.group(1))

    return (hostname_set, ip_set)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(USAGE)
        sys.exit(1)
    
    blacklist_dir = sys.argv[1]
    check_dir = sys.argv[2]
    check_sets = (set(), set())
    blacklist_sets = (set(), set())

    print('Note: DNS resolution and reverse resolution is currently not supported.')
    
    print('Parsing blacklist files...')
    print('-'*80)
    for filename in os.listdir(blacklist_dir):
        filepath = os.path.join(blacklist_dir, filename)
        if not os.path.isfile(filepath):
            continue
        print(filename)
        blacklist = parse_file(filepath)
        blacklist_sets[0].update(blacklist[0])
        blacklist_sets[1].update(blacklist[1])
            
    print()
    print('Parsing check files...')
    print('-'*80)
    for filename in os.listdir(check_dir):
        filepath = os.path.join(check_dir, filename)
        if not os.path.isfile(filepath):
            continue
        print(filename)
        check = parse_file(filepath)
        check_sets[0].update(check[0])
        check_sets[1].update(check[1])

    print()
    print('='*80)
    print('The following hostnames were found in the blacklists:')
    print('='*80)
    
    result = blacklist_sets[0] & check_sets[0]
    print('\n'.join(map(str, result)))
    
    print('='*80)
    print('The following IPs were found in the blacklists:')
    print('='*80)
    
    result = blacklist_sets[1] & check_sets[1]
    print('\n'.join(map(str, result)))
