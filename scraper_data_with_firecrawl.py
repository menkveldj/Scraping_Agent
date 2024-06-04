import os
from time import sleep
from firecrawl import FirecrawlApp




def crawl_data(url):

    # Initialize the FirecrawlApp with your API key
    app = FirecrawlApp(api_key=os.getenv('FIRECRAWL_API_KEY'))

    # params = {
    #     'crawlerOptions': {
    #         'excludes': [],
    #         'includes': [], # leave empty for all pages
    #         'limit': 2,
    #     },
    #     'pageOptions': {
    #         'onlyMainContent': True
    #     }
    # }
    # crawl_job_id = app.crawl_url(url, params=params, wait_until_done=False)
    # print("Crawl job: ", crawl_job_id)

    job_active = True
    while job_active:
        # job_status = app.check_crawl_status(crawl_job_id)
        job_status = app.check_crawl_status("cedf28a8-9667-474e-8e01-360d3fc57687")
        job_active = job_status['status'] == 'active'
        print(f"Job status: {job_status['status']}, {job_status['current']}/{job_status['total']} pages scraped")
        if job_active:
            sleep(5)
    # print(f"{job_status['data'][0]['markdown']}")
    return job_status


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