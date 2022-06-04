# WordPress Content Scraper

Collects posts/pages from a CSV list of Wordpress URLs, spin's them, then prepares them in a JSON file. 

### Requirements

This set of scripts is specifically designed to run on:
 
* [Python 3](https://www.python.org/downloads/windows/)
* [Windows 10](https://www.microsoft.com/en-us/windows/get-windows-10) (although it *should* work on Vista, 7 and 8)
* [MacOS Monterey](https://www.apple.com/macos/monterey/)

 
### Setup

1. Install [Python for Windows](https://www.python.org/downloads/windows/)
2. From the project root, run `python setup.py`
3. Add appropriate values to the `.env` file

### Running the "application"

This is done in 3 parts...

##### 1. Download the articles

1. Compile a list of all URL articles or pages you want to pull content from
2. Add CSV file with list of all URLs to the `./sources` folder

##### 2. Spin and compile the articles

1. Using `terminal`, `bash`, `PowerShell` or similar, navigate to `./scrapers`
2. Run `python scrape-press.py`
3. Wait for the script to finish compiling the JSON file to the `./data` folder

##### 2. Import to your blog

1. Install a processor / importer on your blogging platform (if you're using WordPress, [WP All Import](https://www.wpallimport.com/) is brilliant)
2. Upload the `./data/____.json` file to the importer
3. Map the appropriate fields
4. Run your importer