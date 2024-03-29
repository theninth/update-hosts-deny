#!/usr/bin/env python
# -*- coding: utf-8 -*-

#########################
# CONFIGURATION GOES HERE

# In production the filename is /etc/hosts.deny
FILENAME = '/etc/hosts.deny'

# Use this separator in file. Really no use in changing
SEPARATOR = '## AUTOGENERATED LIST'

# URL to blacklist
BLACKLIST_URL = 'http://www.openbl.org/lists/hosts.deny'


#################
# CODE GOES HERE!

import sys
import urllib2


def get_file():
    """
    Read content of hosts.deny file and return code that is generated
    static and dynamic. I.e. What is seperated by the string SEPARATOR.

    Returns a tuple: (static_part, generated_part)
    """

    with open(FILENAME, 'r') as f:
        try:
            content = f.read()
        except Exception, e:
            print str(e)
            sys.exit(1)

        if SEPARATOR in content:
            static, dynamic = content.split(SEPARATOR)
            return static.strip(), dynamic.strip()
        else:
            return content.strip(), ''


def update_file():
    """
    Update hosts.deny-file with dynamic content
    This is the main function to run.
    """

    static, _ = get_file()

    try:
        dynamic = urllib2.urlopen(BLACKLIST_URL).read()
    except Exception, e:
        print str(e)
        print '\nCould not fetch url:', BLACKLIST_URL
        sys.exit(1)

    with open(FILENAME, 'w') as f:
        f.write(static + '\n\n')
        f.write(SEPARATOR + '\n\n')
        f.write(dynamic + '\n')

    added_lines = dynamic.count('\n')
    print 'Number of lines added to %s: %s' % (FILENAME, added_lines)


if __name__ == '__main__':
    update_file()
