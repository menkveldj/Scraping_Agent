import os
from time import sleep
from firecrawl import FirecrawlApp



# crawl_data function is used to crawl a website and return the data
def crawl_data(url):

    # Initialize the FirecrawlApp with your API key
    app = FirecrawlApp(api_key=os.getenv('FIRECRAWL_API_KEY'))

    params = {
        'crawlerOptions': {
            'excludes': [os.getenv('CRAWLER_EXCLUDES_LIST')],
            'includes': [os.getenv('CRAWLER_INCLUDES_LIST')], # leave empty for all pages
            'limit': os.getenv('CRAWLER_DEPTH'),
        },
        'pageOptions': {
            'onlyMainContent': os.getenv('CRAWLER_DEPTH_MAIN_CONTENT_ONLY')
        }
    }
    # crawl_job_id = app.crawl_url(url, params=params, wait_until_done=False)
    # print("Crawl job: ", crawl_job_id)

    print("starting wait loop")
    job_active = True
    while job_active:
        print("starting wait loop 2")
        sleep(10)
        # job_status = app.check_crawl_status(crawl_job_id)
        job_status = app.check_crawl_status("d36ce23b-e036-4aa7-8418-c0c7ae7a341b")
        # job_status = app.check_crawl_status("87280c99-e409-4356-a8ce-282bd2bc40a1")
        print("starting wait loop 3")
        job_active = job_status['status'] == 'active'
        print(f"Job status: {job_status['status']}, {job_status['current']}/{job_status['total']} pages scraped. Job Active: {job_active}")
    # print(f"{job_status['data'][0]['markdown']}")
    return job_status


# used for a single page and is not built out correctly yet
def scrape_data(url):

    # Initialize the FirecrawlApp with your API key
    app = FirecrawlApp(api_key=os.getenv('FIRECRAWL_API_KEY'))
    
    # Scrape a single URL
    scraped_data = app.scrape_url(url,{'pageOptions':{
        'onlyMainContent': True,
        'waitFor': 5000}
        })

    # Check if 'markdown' key exists in the scraped data
    if 'markdown' in scraped_data:
        return scraped_data
    else:
        raise KeyError("The key 'markdown' does not exist in the scraped data.")