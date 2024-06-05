import os
from time import sleep
from firecrawl import FirecrawlApp



# crawl_data function is used to crawl a website and return the data
def crawl_data(url):

    # Initialize the FirecrawlApp with your API key
    app = FirecrawlApp(api_key=os.getenv('FIRECRAWL_API_KEY'))
    crawl_excludes = os.getenv('CRAWLER_EXCLUDES_LIST') or None
    crawl_includes = os.getenv('CRAWLER_INCLUDES_LIST') or None
    crawl_limit = os.getenv('CRAWLER_LIMIT') or 15
    crawl_depth = os.getenv('CRAWLER_DEPTH') or 3
    crawl_main_content_only = os.getenv('CRAWLER_DEPTH_MAIN_CONTENT_ONLY') or True

    params = {
        'crawlerOptions': {
            'limit': crawl_limit,
            'depth': crawl_depth,
        },
        'pageOptions': {
            'onlyMainContent': os.getenv(crawl_main_content_only)
        }
    }
    if crawl_excludes is not None:
        params['crawlerOptions']['excludes'] = [crawl_excludes]
    if crawl_includes is not None:
        params['crawlerOptions']['includes'] = [crawl_includes]
    print (f"Params: {params}")

    crawl_job_id = app.crawl_url(url, params=params, wait_until_done=False)
    print(f"Crawl job for {url} started: {crawl_job_id}")
    # crawl_job_id = {"jobId": "89243e98-90d5-46b4-a5be-700049447e65"}

    job_active = True
    while job_active:
        job_status = app.check_crawl_status(crawl_job_id["jobId"])
        job_active = job_status['status'] == 'active'
        print(f"Job status: {job_status['status']}, {job_status['current']}/{job_status['total']} pages scraped. Job Active: {job_active}")
        if job_active:
            sleep(10)
    print(f"Crawl job completed: {crawl_job_id}")
    if "data" in job_status and "error" in job_status["data"]:
        print(f"Error Crawling Site: {job_status['data']['error']}")
        raise KeyError("Crawl Failed with message: {job_status['data']['error']}")
    else:
        job_status["job_id"] = crawl_job_id["jobId"]
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