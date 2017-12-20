#! /usr/bin/env python
# -*- coding: utf-8 -*-

import json
from os.path import dirname, abspath, join

import tornado.ioloop
import tornado.web
import tornado.log
import tornado.options
from tornado.options import define, options

from api.email import EmailHandler, handle_notify


define('host', default='0.0.0.0', help='run on the given host', type=str)
define('port', default=8080, help='run on the given port', type=int)


def set_email_conf(conf):
    with open(conf, 'r') as f:
        email_conf = json.load(f, encoding='utf-8')
        return email_conf


def main():
    BASE_DIR = dirname(abspath(__file__))
    email_conf = join(BASE_DIR, 'etc/email.conf')
    settings = dict(
        debug=False,
        email_conf=set_email_conf(email_conf),
        template_path=join(BASE_DIR, 'templates')
    )
    tornado_conf = join(BASE_DIR, 'etc/api.conf')
    tornado.options.parse_config_file(tornado_conf)
    tornado.options.parse_command_line()

    print 'Log Handlers: %s' % tornado.log.logging.getLogger().handlers

    application = tornado.web.Application([
        (r'/xxxxxx/v1/email', EmailHandler),
        (r'/xxxxxx/v1/email/(\w+)', EmailHandler)
    ], **settings)

    application.listen(options.port, options.host)
    print 'server running on %s:%s' % (options.host, options.port)
    tornado.ioloop.IOLoop.instance().spawn_callback(handle_notify)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
