# pastebin-scraper2
usage: pastebin2.py [-h] [-s SLEEP] [--gzip]

optional arguments:
  -h, --help                  show this help message and exit

  -s SLEEP, --sleep SLEEP     Seconds to sleep between scraping

  --gzip, --gz                Saves compressed files

-----------------------------------------------------------------------------
The inital source was written by someone else and unfortunately I cant remember who it was
or from where I got it. There isn't much left from the original anyway.

The scraper supports proxies and predefined user agents.

If you run out of proxies you can get new ones with the following:
```bash
wget -q -O- http://www.us-proxy.org |awk -F '<tr><td>' {'print $2'} |awk -F '</td><td>' '{print $1":"$2}'|grep -P '^(\d{1,3}.){3}' >> Data/Proxies.txt
```

* Compatible only with python2.
