@echo off
echo Running Scrapy spider...
REM Change the working directory to where your Scrapy project is located
cd /d "C:\Users\muham\Ecc\Ecc"
scrapy crawl athex_spider

echo Spider run completed.
pause
