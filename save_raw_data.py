import json
import os



def save_raw_data(raw_data, sitename, timestamp, organized_data, sitemap, raw_output_folder='output'):
   
    # Ensure the output folder exists
    root_output_folder = os.path.join(raw_output_folder, sitename, timestamp)
    os.makedirs(raw_output_folder, exist_ok=True)
    raw_output_folder = os.path.join(root_output_folder,'raw_data')
    os.makedirs(raw_output_folder, exist_ok=True)

    for raw_page_data in raw_data['data']:

        # Extract the URL from the raw data
        url = raw_page_data['metadata']['sourceURL']
        url = url.replace("https://","")
        url = url.replace("http://","")
        url = url.rstrip("/")
        print("adding page: ", url)

        # create sitemap
        keys = url.split("/")
        if len(keys) > 1:
            if keys[0] in sitemap:
                sitemap[keys[0]].append(keys[1])
            else:
                sitemap[keys[0]] = [keys[1]
                ]
        else:
            sitemap[keys[0]] = []


        # organize data
        organized_data[url] = {}
        organized_data[url]['markdown'] = raw_page_data['markdown']
        organized_data[url]['metadata'] = raw_page_data['metadata']


        fileNameFriendlyUrl = url.replace("/","|")
        # Save the raw meta data with url in filename
        raw_output_path = os.path.join(raw_output_folder, f'rawData{fileNameFriendlyUrl}.content.md')
        with open(raw_output_path, 'w', encoding='utf-8') as f:
            f.write(raw_page_data['markdown'])

        # Save the raw markdown data with url in filename
        raw_output_path = os.path.join(raw_output_folder, f'rawData_{fileNameFriendlyUrl}.meta.json')
        with open(raw_output_path, 'w', encoding='utf-8') as fp:
            json.dump(raw_page_data['metadata'], fp)

    # Save the sitemap
    raw_output_path = os.path.join(root_output_folder, f'sitemap_{fileNameFriendlyUrl}.json')
    with open(raw_output_path, 'w', encoding='utf-8') as fp:
        json.dump(sitemap, fp)

