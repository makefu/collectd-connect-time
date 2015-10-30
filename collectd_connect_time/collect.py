#!/usr/bin/env python

import logging
from socket import socket,getaddrinfo,AF_UNSPEC,SOCK_STREAM,gaierror, \
        error as socket_error,timeout as timeout_error
from time import time

class ConnectTimePlugin(object):
    name = "connect-time"
    collectd_name = "collectd_connect_time"

    def __init__(self,collectd=None):
        self.target = []
        self.collectd = collectd
        self.interval = 10

    def collectd_configure(self,config):
        self.info("configuring")
        for node in config.children:
            k = node.key.lower()
            if  k == "target":
                self.target = node.values
            elif k == "interval":
                self.interval = int(node.values[0])
            else:
                collectd.warn("Unknown config option: {}".format(key))

        self.info("Configured with {}".format(self.target))
        self.collectd.register_read(self.collectd_read,self.interval,name=self.collectd_name)
        if not self.target:
            self.error("no target set, bailing out")
            self.collectd.unregister_read(self.read)

    def collectd_read(self):
        if not self.target:
            self.error("read: no target set")
        for t in self.target:
            target_val = self.get_target_val(t)
            val = self.collectd.Values(plugin=self.name)
            val.type = 'response_time'
            val.type_instance = "max"
            val.plugin_instance = t
            # TODO: split into keys and values
            try:
                val.values = [int(max(target_val.values()))]
                val.dispatch()
            except ValueError as e:
                log.error("cannot dispatch value for target {} -> {}".format(t,e))

    def get_target_val(self,t):
        try:
            host,port = t.split(":")
            port = int(port)
        except ValueError:
            self.debug("defaulting for {} to port 80".format(t))
            host = t
            port = 80
        ret = {}
        try:
            ai = getaddrinfo(host,port,AF_UNSPEC,SOCK_STREAM)
        except gaierror as e:
            self.error("Cannot resolve {}".format(e))
        else:
            for fam,typ,proto,canon,addr in ai:
                try:
                    begin = time()
                    s = socket(fam,typ)
                    s.settimeout(5)
                    s.connect(addr)
                    duration = time() - begin
                except socket_error as e:
                    self.debug("{} -> {}".format(addr[0],e))
                except timeout_error as e:
                    self.error("{} - Timeout error!".format(addr[0],e))
                    duration = 5
                else:
                    k = "{}:{}".format(*addr)
                    ret[k] = duration * 1000 # in ms
        return ret

    def debug(self,msg):
        if self.collectd: self.collectd.debug(msg)
        else: logging.debug(msg)

    def error(self,msg):
        if self.collectd: self.collectd.error(msg)
        else: logging.error(msg)

    def info(self,msg):
        if self.collectd: self.collectd.info(msg)
        else: logging.info(msg)

def cli():
    import sys,json
    c = ConnectTimePlugin()
    print(json.dumps(c.get_target_val(sys.argv[1]),indent=4))

def run_collectd(collectd):
    c = ConnectTimePlugin(collectd)
    collectd.register_config(c.collectd_configure,name="collectd_connect_time")

if __name__ == "__main__":
    cli()

