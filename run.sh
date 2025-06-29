#! /bin/sh

exec mitmproxy --listen-host localhost -p 8080 -s logger.py -v
