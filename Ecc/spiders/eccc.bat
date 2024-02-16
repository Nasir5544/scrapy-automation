@echo off
echo Running Scrapy spider...
REM Change the working directory to where your Scrapy project is located
cd /d "C:\Users\muham\Ecc\Ecc"
scrapy crawl ecc -o output.json 
scrapy crawl gpw_spider -o output.json 

echo Spider run completed.
pause
