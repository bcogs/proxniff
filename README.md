# proxniff

A man in the middle http(s) proxy that logs all the traffic to a file.

It requires the `mitmproxy` utility (on mac: `brew install mitmproxy`).

Run it with `./run.sh`

Then configure your browser to trust `~/.mitmproxy/mitmproxy-ca-cert.pem` and to use `localhost:8080` as proxy.

It will proxy on port 8080 and log all the traffic to `proxniff.txt`

The filter-out.py companion script allows to filter out some of the crap requests from the log file by url: `./filter-out.py 'http://googlead.*' 'blahblah.*' <proxniff.txt | less `
