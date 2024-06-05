import json
import os
from helpers import add_page_and_meta_to_sitemap, add_page_sitemap_basic, get_url_keys, add_page_content_to_sitemap
from clean_data_with_ai import clean_data_with_ai, clean_data_test
import concurrent.futures

def save_raw_data(raw_data, sitename, timestamp, organized_data, output_folder='output'):
   
    # Ensure the output folder exists
    root_output_folder = os.path.join(output_folder, sitename, timestamp)
    os.makedirs(output_folder, exist_ok=True)
    output_folder = os.path.join(root_output_folder,'raw_data')
    os.makedirs(output_folder, exist_ok=True)

    full_sitemap = {}
    basic_sitemap = {}

    for raw_page_data in raw_data['data']:
        
        # Extract the URL from the raw data
        url = raw_page_data['metadata']['sourceURL']
        url_keys = get_url_keys(url)
        full_sitemap = add_page_and_meta_to_sitemap(full_sitemap, url_keys, raw_page_data['metadata'])
        basic_sitemap = add_page_sitemap_basic(basic_sitemap, url_keys)

        # organize data
        organized_data[url] = {}
        organized_data[url]['markdown'] = raw_page_data['markdown']
        organized_data[url]['metadata'] = raw_page_data['metadata']

        fileNameFriendlyUrl = url.replace("/","|")
        # Save the raw meta data with url in filename
        raw_output_path = os.path.join(output_folder, f'rawData{fileNameFriendlyUrl}.content.md')
        with open(raw_output_path, 'w', encoding='utf-8') as f:
            f.write(raw_page_data['markdown'])

        # Save the raw markdown data with url in filename
        raw_output_path = os.path.join(output_folder, f'rawData_{fileNameFriendlyUrl}.meta.json')
        with open(raw_output_path, 'w', encoding='utf-8') as fp:
            json.dump(raw_page_data['metadata'], fp, indent=4)

    # write out scraper job id
    if "job_id" in raw_data:
        raw_output_path = os.path.join(output_folder, f'job_id.txt')
        with open(raw_output_path, 'w', encoding='utf-8') as f:
            f.write(raw_data['job_id'])

    # Save the sitemap
    raw_output_path = os.path.join(root_output_folder, f'sitemap_meta_{sitename}.json')
    with open(raw_output_path, 'w', encoding='utf-8') as fp:
        json.dump(full_sitemap, fp, indent=4)
    # Save the basic sitemap
    raw_output_path = os.path.join(root_output_folder, f'sitemap_simple_{sitename}.json')
    with open(raw_output_path, 'w', encoding='utf-8') as fp:
        json.dump(basic_sitemap, fp, indent=4)
    return full_sitemap, url_keys



def save_cleaned_data(organized_data, url, sitename, sitemap, timestamp, clean_data, output_folder='output'):

    # Ensure the output folder exists
    root_output_folder = os.path.join(output_folder, sitename, timestamp)
    os.makedirs(output_folder, exist_ok=True)
    output_folder = os.path.join(root_output_folder,'clean_data')
    os.makedirs(output_folder, exist_ok=True)

    full_sitemap = {}

    pageCount = 1
    total_pages = len(organized_data)

    max_concurrency = int(os.getenv('AI_REQUESTS_MAX_CONCURRENCY', 1))
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_concurrency) as executor:
        futures = []
        for u in organized_data:
            # futures.append(executor.submit(clean_data_test, u,organized_data[u]['markdown']))
            futures.append(executor.submit(clean_data_with_ai, u,organized_data[u]['markdown']))
        for future in concurrent.futures.as_completed(futures): 
            try:
                uc, clean_page_data = future.result()
            except Exception as exc:
                print(f'{uc} generated an exception: {exc}')
            else:
                print(f"page {pageCount} of {total_pages} cleaned: {uc}")
                clean_data[uc] = clean_page_data
    
                # update sitemap with clean data
                url_keys = get_url_keys(uc)
                full_sitemap = add_page_content_to_sitemap(sitemap, url_keys, clean_data[uc])

                fileNameFriendlyUrl = uc.replace("/","|")
                # Save the raw meta data with url in filename
                raw_output_path = os.path.join(output_folder, f'{fileNameFriendlyUrl}.md')
                with open(raw_output_path, 'w', encoding='utf-8') as f:
                    f.write(clean_data[uc])
                pageCount += 1

    print("Concurent data cleaning finished...")
    
    # Save the full sitemap
    raw_output_path = os.path.join(root_output_folder, f'sitemap_full_{sitename}.json')
    with open(raw_output_path, 'w', encoding='utf-8') as fp:
        json.dump(full_sitemap, fp, indent=4)

     # Save clean data into a single file
    raw_output_path = os.path.join(root_output_folder, f'website_content_{sitename}.md')
    with open(raw_output_path, 'w', encoding='utf-8') as fp:
        for url in clean_data:
            fp.write(clean_data[url])
            fp.write("\n\n\n\n----------------------------------------------------\n\n\n\n")  

    return full_sitemap

        