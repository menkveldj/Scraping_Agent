import json
import os
from helpers import add_page_and_meta_to_sitemap, add_page_sitemap_basic



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
        url = url.replace("https://","")
        url = url.replace("http://","")
        url = url.rstrip("/")
        print("adding page: ", url)

        # create sitemap
       
        print("Starting Sitemap")
        url_keys = url.split("/")
        full_sitemap = add_page_and_meta_to_sitemap(full_sitemap, url_keys, raw_page_data['metadata'])
        basic_sitemap = add_page_sitemap_basic(basic_sitemap, url_keys)
        print("Ending Sitemap")


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

    # Save the sitemap
    raw_output_path = os.path.join(root_output_folder, f'sitemap_full_{fileNameFriendlyUrl}.json')
    with open(raw_output_path, 'w', encoding='utf-8') as fp:
        json.dump(full_sitemap, fp, indent=4)
    # Save the basic sitemap
    raw_output_path = os.path.join(root_output_folder, f'sitemap_simple_{fileNameFriendlyUrl}.json')
    with open(raw_output_path, 'w', encoding='utf-8') as fp:
        json.dump(basic_sitemap, fp, indent=4)



def save_cleaned_data(clean_data, url, sitename, timestamp, output_folder='output'):

    # Ensure the output folder exists
    root_output_folder = os.path.join(output_folder, sitename, timestamp)
    os.makedirs(output_folder, exist_ok=True)
    output_folder = os.path.join(root_output_folder,'processed_data')
    os.makedirs(output_folder, exist_ok=True)

    fileNameFriendlyUrl = url.replace("/","|")
    # Save the raw meta data with url in filename
    raw_output_path = os.path.join(output_folder, f'{fileNameFriendlyUrl}.md')
    with open(raw_output_path, 'w', encoding='utf-8') as f:
        f.write(clean_data)

    # # Check if data is a dictionary and contains exactly one key
    # if isinstance(organized_data, dict) and len(organized_data) == 1:
    #     key = next(iter(organized_data))  # Get the single key
    #     organized_data = organized_data[key]


    # # Convert the formatted data to a pandas DataFrame
    # df = pd.DataFrame(organized_data)

    # # Convert the formatted data to a pandas DataFrame
    # if isinstance(organized_data, dict):
    #     organized_data = [organized_data]

    # df = pd.DataFrame(organized_data)

    # # Save the DataFrame to an Excel file
    # excel_output_path = os.path.join(output_folder, f'sorted_data_{timestamp}.xlsx')
    # df.to_excel(excel_output_path, index=False)
    # print(f"Formatted data saved to Excel at {excel_output_path}")


