def add_page_and_meta_to_sitemap(sitemap, url_keys, metadata):
    if url_keys[0] not in sitemap:
        sitemap[url_keys[0]] = {}
        sitemap[url_keys[0]] = {"meta_data": metadata, "sub_pages": {}}
    if len(url_keys) > 1:
        sitemap[url_keys[0]]["sub_pages"] = add_page_and_meta_to_sitemap(sitemap[url_keys[0]]["sub_pages"], url_keys[1:], metadata)
    return sitemap

def add_page_sitemap_basic(sitemap, url_keys):
    
    # print(f"Sitemap: {sitemap}, URL Keys: {url_keys}")
    if url_keys[0] not in sitemap:
        # print(f"Adding new page: {url_keys[0]}")
        sitemap[url_keys[0]] = {}
    if len(url_keys) > 1:
        # print(f"Adding child pages of {url_keys[0]}, children {url_keys[1:]}")
        sitemap[url_keys[0]] = add_page_sitemap_basic(sitemap[url_keys[0]], url_keys[1:])
    # print(f"Returning sitemap: {sitemap}")
    return sitemap


def add_page_content_to_sitemap(sitemap, url_keys, page_content):
        if url_keys[0] not in sitemap:
            print(f"Could not find page in sitemap: {url_keys[0]}")
            raise KeyError(f"Could not find page in sitemap: {url_keys[0]}")
        elif len(url_keys) <= 1: 
            sitemap[url_keys[0]]["page_content"] = page_content
        else:
            sitemap[url_keys[0]]["sub_pages"] = add_page_content_to_sitemap(sitemap[url_keys[0]]["sub_pages"], url_keys[1:], page_content)
        return sitemap


def get_url_keys(url):
    url = url.replace("https://","")
    url = url.replace("http://","")
    url = url.rstrip("/")
    url = url.replace("\r","")
    url = url.replace("\n","")
    url = url.replace(" ","")
    url_keys = url.split("/")
    return url_keys



def split_list_into_params(list):
    list = list.replace("'","")
    list = list.replace("\"","")
    list = list.replace(" ","")
    params = list.split(",")
    return params