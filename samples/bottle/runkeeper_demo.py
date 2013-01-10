#!/usr/bin/env python
"""Demo Application for HealthGraph-API Python Library developed using Bottle 
fast, simple and lightweight WSGI micro web-framework for Python.

"""

import sys
import os
import optparse
import ConfigParser
import bottle
from healthgraph import RunKeeperAuthMgr, RunKeeperClient
from beaker.middleware import SessionMiddleware


__author__ = "Ali Onur Uyar"
__copyright__ = "Copyright 2012, Ali Onur Uyar"
__credits__ = []
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Ali Onur Uyar"
__email__ = "aouyar at gmail.com"
__status__ = "Development"


# Defaults
conf = {'baseurl': '127.0.0.1:8000',
        'bindaddr': '127.0.0.1',
        'bindport': 8000,
        }
defaultConfFilename = 'runkeeper_demo.conf'


# Globals



@bottle.route('/')
def index():
    rk_auth_mgr = RunKeeperAuthMgr(conf['client_id'], conf['client_secret'], 
                                   '/'.join((conf['baseurl'], 'login',)))
    rk_auth_uri = rk_auth_mgr.getLoginURL()
    rk_button_img = rk_auth_mgr.getLoginButtonURL('blue', 'black', 300)
    return bottle.template('index.html', {'rk_button_img': rk_button_img,
                                          'rk_auth_uri': rk_auth_uri,})



def parse_cmdline(argv):
    """Parse command line options."""
    parser = optparse.OptionParser()
    parser.add_option('-c', '--conf', help='Configuration file path.',
                      dest='confpath',default=None)
    parser.add_option('-p', '--bindport',
                      help='Bind to TCP Port. (Default: %d)' % conf['bindport'],
                      dest='bindport', type='int', default=None, action='store')
    parser.add_option('-b', '--bindaddr',
                      help='Bind to IP Address. (Default: %s)' % conf['bindaddr'],
                      dest='bindaddr', default=None, action='store')
    parser.add_option('-u', '--baseurl', 
                      help='Base URL. (Default: %s)' % conf['baseurl'],
                      dest='baseurl', default=None, action='store')
    parser.add_option('-D', '--devel', help='Enable development mode.',
                      dest='devel', default=False, action='store_true')
    if argv is None:
        return parser.parse_args()
    else:
        return parser.parse_args(argv[1:])
   
    
def parse_conf_files(conf_paths):
    conf_file = ConfigParser.RawConfigParser()
    conf_read = conf_file.read(conf_paths)
    if conf_read:
        try:
            conf['client_id'] = conf_file.get('runkeeper', 'client_id')
            conf['client_secret'] = conf_file.get('runkeeper', 'client_secret')
            if conf_file.has_option('runkeeper', 'bindport'):
                conf['bindport'] = conf_file.getint('runkeeper', 'bindport')
            if conf_file.has_option('runkeeper', 'bindaddr'):
                conf['bindaddr'] = conf_file.get('runkeeper', 'bindaddr')
            if conf_file.has_option('runkeeper', 'baseurl'):
                conf['baseurl'] = conf_file.get('runkeeper', 'baseurl')
        except ConfigParser.Error:
            return "Error parsing configuration file(s): %s\n%s" % (
                ', '.join(conf_read), sys.exc_info()[1])
    else:
        return "No valid configuration file (%s) found." % defaultConfFilename


def main(argv=None):
    cmdOpts = parse_cmdline(argv)[0]
    if cmdOpts.confpath is not None:
        if os.path.exists(cmdOpts.confpath):
            conf_paths = [cmdOpts.confpath,]
        else:
            return "Configuration file not found: %s" % cmdOpts.confpath
    else:
        conf_paths = [os.path.join(path, defaultConfFilename) for path in ('/etc', '.',)]
    parse_conf_files(conf_paths)
    if cmdOpts.bindport is not None:
        conf['bindport'] = cmdOpts.bindport
    if cmdOpts.bindaddr is not None:
        conf['bindaddr'] = cmdOpts.bindaddr
    if cmdOpts.baseurl is not None:
        conf['baseurl'] = cmdOpts.baseurl
    if cmdOpts.devel:
        from bottle import debug
        debug(True)
    bottle.run(server=bottle.WSGIRefServer, 
               host=conf['bindaddr'], port=conf['bindport'], 
               reloader=cmdOpts.devel)
    


if __name__ == "__main__":
    sys.exit(main())