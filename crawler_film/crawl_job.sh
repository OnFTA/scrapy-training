#!/bin/bash

spider_name=${1}

opts=${@:2}

scrapy crawl ${spider_name} -s LOG_FILE=logs/${spider_name}_`date +%Y-%m-%d"_"%H-%M-%S`.log \
    -s JOBDIR=jobs/${spider_name} \
    -s HTTPCACHE_ENABLED=1 \
    -s HTTPCACHE_IGNORE_HTTP_CODES=302,401,403,404,500,501,502,503,504,522,524 \
#    -s HTTPCACHE_STORAGE='scrapy.extensions.httpcache.LeveldbCacheStorage' \
    ${opts}
