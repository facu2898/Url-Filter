from pandas import *



def is_nan_string(value):
    return value != value

def urls_to_dict(urls): ##returns a list of dict such as {level1/url, level2/url......}
    list_of_urls = urls.values.tolist()
    level = 0
    dict = {}
    list_of_url_dicts = []
    for row in list_of_urls:
        for i in range(0, len(row), 2):
            if i % 2 == 0:
                level += 1
            if not (is_nan_string((row[i]))):
                dict[f"level_{level}"] = row[i]
                dict[f"url_{level}"] = row[i+1]
        list_of_url_dicts.append(dict.copy())
        dict.clear()
        level = 0

    return list_of_url_dicts

def items_and_urls_to_dict(items_urls):##returns a dict where the key is the url and the value a list of ids wich come from that url
    urls_list = items_urls["Start URL"].values.tolist()
    ids_list = items_urls["_ID"].values.tolist()
    dict_of_urls_items = {}

    for i in range(0,len(urls_list)):
        if urls_list[i] in dict_of_urls_items:
            dict_of_urls_items[urls_list[i]].append(ids_list[i])
        else:
            dict_of_urls_items[urls_list[i]] = [ids_list[i]]

    return dict_of_urls_items


def create_ids_indexes(items_urls):##returns a dict which has the id as key and the amount of times it appears as the value
    ids = items_urls["_ID"].values.tolist()
    ids_indexes_dic = {}

    for id in ids:
        if id in ids_indexes_dic:
            ids_indexes_dic[id] += 1
        else:
            ids_indexes_dic[id] = 1

    return ids_indexes_dic

def keep_url(url,id_indexes, urls_and_ids, tolerance):##returns true if we should keep the url or false if we shouldnt, tolerance is how many unique ids we should tolerate and still discard the url
    if url not in urls_and_ids:
        return True
    ids_from_url = urls_and_ids[url]
    amount_of_unique_ids = len(ids_from_url)
    real_tolerance = 0
    if tolerance != 0:
        real_tolerance = (len(ids_from_url)/100)*tolerance
    for id in ids_from_url:
        if id_indexes[id] > 1:
            amount_of_unique_ids -= 1

    if amount_of_unique_ids <= int(real_tolerance):
        return False
    else:
        return True


def decrease_indexes(id_indexes, url, urls_and_ids):
    ids = []
    new_id_indexes = id_indexes
    ids_list = urls_and_ids[url]

    for id in ids_list:
        new_id_indexes[id] -= 1

    return new_id_indexes


def process_urls(urls_name, prods_name, input_tolerance):
    try:
        name_of_urls = urls_name
        name_of_prods = prods_name
        noTolerance = True
        while noTolerance:
            try:
                tolerance = input_tolerance
                if tolerance >= 0:
                    noTolerance = False
                else:
                    print("Please insert a positive integer")
            except:
                print("Please insert a positive integer")
        urls_df = read_excel(f"resources/{name_of_urls}")
        dict_of_urls = urls_to_dict(urls_df)
        urls_items_df = read_excel(f"resources/{name_of_prods}")
        id_indexes = create_ids_indexes(urls_items_df)
        urls_and_ids = items_and_urls_to_dict(urls_items_df)
    except:
        print("There was an error converting the .xlsx files, please restart and check the names and paths")
        exit()

    urls_keeped = []
    urls_removed = []

    for current_level_checking in range(1, int(len(urls_df.columns) / 2) + 1):
        for urls in dict_of_urls:
            if len(urls) == current_level_checking * 2:
                url = urls[f"url_{current_level_checking}"]
                if keep_url(url, id_indexes, urls_and_ids, tolerance):
                    urls_keeped.append(urls.copy())
                else:
                    urls_removed.append(urls.copy())

    urls_keeped_df = DataFrame(urls_keeped)
    urls_removed_df = DataFrame(urls_removed)

    urls_keeped_df.to_excel(f"resources/{name_of_urls}", index=False)


