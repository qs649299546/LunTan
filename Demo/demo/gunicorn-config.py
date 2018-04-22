# -*- coding: utf-8 -*-

from multiprocessing import cpu_count

bind = ["127.0.0.1:9000"]
daemon = True

workers = cpu_count() * 2
worker_class = "gevent"
forwarded_allow_ips = '*'

keepalive = 6
timeout = 65
graceful_timeout = 10
worker_connections = 65535
