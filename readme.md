# Calder Scaping Agent 1.0

The scraping agent will scrape data from a website, organize it into markdown and then feed it to OpenAI to processes into trainable data. Furthermore it tracks keywords and generates a sitemap for use later.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Installation

- create virtual environment `python -m venv venv`
- get into venv `source .venv/bin/activate`
- add api keys to .env
    ```
        WEBSITE_URL=""

        CRAWLER_EXCLUDES_LIST="" # ex: "services/,industries/"
        CRAWLER_INCLUDES_LIST="" # ex: "services/,industries/"
        CRAWLER_LIMIT=1000 # how many pages to crawl before stopping
        CRAWLER_DEPTH=100 # how deep to crawl
        CRAWLER_DEPTH_MAIN_CONTENT_ONLY="False" # "True" or "False" - pull only main content from site (this can miss content areas)
        CRAWL_ONLY="True" # "True" or "False" - Crawl site but do not processes with AI
        CRAWLER_SITEMAP_ONLY="True" # "True" or "False" - Return only a sitemap
        AI_RECLEAN_CRAWL_JOB="" # add a job_id to reprocesses an existing crawl_job

        FIRECRAWL_API_KEY=
        OPENAI_API_KEY=
        AI_REQUESTS_MAX_CONCURRENCY=3 # how many ai threads run at a time
        AI_SYSTEM_MESSAGE="You are an intelligent website copy writer. You understand the structure of websites and webpages. You understand the difference between types of webpages including: homepages, content pages, case studies, testimonials, portfolios. Your task is review the provided markdown generated during scaping a webpage for content and organize it more clearly based upon the type of page it comes from. You will be reading markdown and returning cleaned and organized markdown. Whenever possible you should utilize the existing content structure including sections, titles, paragraphs and lists. The markdown should contain only the structured data extracted from the provided content, with no additional commentary, explanations, or extraneous information. You should remove any unnecessary content including markdown reguarding the website header,footer, and navigation. You should also remove links to images and files. Your primary goal is to extract the webpages primary content and organize it in a clear and concise manner. Please process the following markdown and provide the output in markdown format with no words before or after the markdown"
        AI_USER_MESSAGE="Extract the webpage content and organize it in a clear and consise manner using markdown. Do not change the content, only the structure."
    ```
- Install the dependencies: `pip install -r requirements.txt`
- Start the application: `python app`
- optional: to fix ssl python error ``

## Usage


## Contributing


## License

