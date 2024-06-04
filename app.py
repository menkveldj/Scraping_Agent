
from save_data import save_raw_data, save_cleaned_data
from clean_data_with_ai import format_data
from scraper_data_with_firecrawl import crawl_data
from dotenv import load_dotenv
from datetime import datetime
import os
import traceback



if __name__ == "__main__":

    try:
        load_dotenv()
        
        url = os.getenv('WEBSITE_URL')

        # Extract sitename from URL
        sitename: str = url.split('/')[2]
        timestamp_start = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Scrape data
        # raw_data = scrape_data(url)
        # save_raw_data(raw_data, sitename, timestamp_start)
        
        # Crawl site for data
        print(f"Starting scraping {url} at {timestamp_start}")
        raw_data = crawl_data(url)

        # Organize & save raw data
        organized_data = {}
        print(f"Organizing raw data for {sitename}...")
        sitemap, url_keys = save_raw_data(raw_data, sitename, timestamp_start, organized_data)

        # # Clean & save data with AI
        clean_data = {}
        print(f"Cleaning organized data for {url}...")
        sitemap = save_cleaned_data(organized_data, url,sitename, sitemap, timestamp_start, clean_data)





        
        # Compile Data Into Final Result
        # compiled_data = {}
        # for url in organized_data:
        #     site_data = {"url": url, "metadata": organized_data[url]['metadata'], "content": formatted_data[url]}
        #     # create compiled_data
        #     keys = url.split("/")
        #     if len(keys) > 1:
        #         if keys[0] in compiled_data:
        #             compiled_data[keys[0]].append(keys[1])
        #         else:
        #             compiled_data[keys[0]] = [keys[1]
        #             ]
        #     else:
        #         compiled_data[keys[0]] = []

        # print(f"Processing organized data for {sitename}...")
        # formatted_data = format_data(organized_data)
        # save_formatted_data(organized_data,sitename,timestamp_start,formatted_data)
        
        # Save formatted data
        # save_formatted_data(formatted_data, timestamp)

        timestamp_end = datetime.now().strftime('%Y%m%d_%H%M%S')
        duration = datetime.strptime(timestamp_end, '%Y%m%d_%H%M%S') - datetime.strptime(timestamp_start, '%Y%m%d_%H%M%S')
        print(f"Finished scraping for {sitename} at {timestamp_end}. Duration: {duration}")
        
    except Exception as e:
        print(traceback.format_exc())
        print(f"An error occurred: {e}")

    



# Split URL into parts
# url_parts = url.split("/")
# Create sitemap
# sitemap = create_sitemap(url_parts, compiled_data)