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


    






    