@echo off
echo Running Scrapy spiders...
cd /d "C:\Users\muham\Ecc\Ecc"
start cmd /k scrapy crawl athex_spider & start cmd /k scrapy crawl gpw_spider  & start cmd /k scrapy crawl Ecc_spider 

echo All spiders have been started.
pause