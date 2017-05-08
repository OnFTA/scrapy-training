#!/usr/bin/env bash

cd /crawler_film/

slist=$(scrapy list)

while :
do
    for element in ${slist##* }
    do
       scrapy crawl "$element" -s LOG_FILE=logs/"$element".log

    done
done

