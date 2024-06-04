
from save_data import save_raw_data, save_cleaned_data
from clean_data_with_ai import format_data
from scraper_data_with_firecrawl import crawl_data
from dotenv import load_dotenv
import pprint
from datetime import datetime


if __name__ == "__main__":
    # Scrape a single URL
    # url = 'https://michiganlabs.com'
    url = 'https://caldersolutions.com'
    # url = 'https://www.trulia.com/CA/San_Francisco/'
    # url = 'https://atomicobject.com/platforms/web-app-development'
    

    try:
        load_dotenv()
        
        # Extract sitename from URL
        sitename: str = url.split('/')[2]
        timestamp_start = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Scrape data
        # raw_data = scrape_data(url)
        # save_raw_data(raw_data, sitename, timestamp_start)
        
        # Crawl site for data
        print(f"Starting scraping {sitename} at {timestamp_start}")
        raw_data = crawl_data(url)

        # Organize & save raw data
        organized_data = {}
        sitemap = {}
        print(f"Organizing raw data for {sitename}...")
        save_raw_data(raw_data, sitename, timestamp_start, organized_data, sitemap)

        # Clean & save data with AI
        formatted_data = {}
        for url in organized_data:
            print(f"Cleaning organized data for {url}...")
            clean_data = format_data(organized_data[url]['markdown'])
            formatted_data[url] = clean_data
            save_cleaned_data(clean_data, url,sitename,timestamp_start)
        
        # Compile Data Into Final Result
        

        # print(f"Processing organized data for {sitename}...")
        # formatted_data = format_data(organized_data)
        # save_formatted_data(organized_data,sitename,timestamp_start,formatted_data)
        
        # Save formatted data
        # save_formatted_data(formatted_data, timestamp)

        timestamp_end = datetime.now().strftime('%Y%m%d_%H%M%S')
        duration = datetime.strptime(timestamp_end, '%Y%m%d_%H%M%S') - datetime.strptime(timestamp_start, '%Y%m%d_%H%M%S')
        print(f"Finished scraping for {sitename} at {timestamp_end}. Duration: {duration}")
        
    except Exception as e:
        print(f"An error occurred: {e.with_traceback}")
        print(f"An error occurred: {e}")