# coding=utf-8
import pandas as pd
import unicodedata
from sklearn.cluster import KMeans

PERSON_001_PATH = r"C:\Users\Emanuel\Desktop\DataHack16\PERSON - 001.csv"
FEATURES_TABLE_PATH = r"C:\Users\Emanuel\Desktop\DataHack16\features_678.csv"


# We find all keys with an empty value:
def return_keys_without_value(dic):
    keys = []
    for key, value in dic.items():
        if value == "":  # todo: take care of keys without value that do contain : somewhere
            keys.append(key)
    if len(keys) > 0:
        return keys
    else:
        return None


data = pd.read_csv(PERSON_001_PATH, names=["string", "id"])
data = data.dropna()
data = data[data["string"] != "{}"]
data["string"] = [eval(k) for k in data["string"]]
data["string"] = [return_keys_without_value(dic) for dic in data["string"]]
data = data.dropna()

string_list = []
id_list = []
for _, row in data.iterrows():
    for elem in row["string"]:
        string_list.append(elem)
        id_list.append(row["id"])
new_data = pd.DataFrame({"string": string_list, "id": id_list})
new_data.to_csv(r"C:\Users\Emanuel\Desktop\DataHack16\data_separated.csv", encoding="utf-8")


def is_all_hebrew(s):
    try:
        s = s.decode("utf-8")
    except AttributeError:
        pass

    # remove all non-characters:
    q = ""
    for i in s:
        if i.isalpha():
            q = "".join([q, i])

    return all('HEBREW' in unicodedata.name(c) for c in q)


def is_all_english(s):
    try:
        s = s.decode("utf-8")
    except AttributeError:
        pass

    # remove all non-characters:
    chars_only = ""
    for i in s:
        if i.isalpha():
            chars_only = "".join([chars_only, i])
    return all('LATIN' in unicodedata.name(c) for c in chars_only)


def count_words(s):
    return len(s.split())


# todo: add a feature "contains_predefined_year_prefixes", like b. or d.
# todo: add a feature that checks whether the string contains a number that is not a year (i.e not in the range ...)
# todo: detect hebrew years using quotes
new_data["is_all_hebrew"] = new_data["string"].apply(is_all_hebrew)
new_data["is_all_english"] = new_data["string"].apply(is_all_english)
new_data["number_of_words"] = new_data["string"].apply(count_words)
new_data["contains_quote"] = new_data["string"].apply(lambda s: '"' in s)
new_data["contains_colon"] = new_data["string"].apply(lambda s: ':' in s)
new_data.to_csv(FEATURES_TABLE_PATH)

X = new_data.copy()
assert isinstance(X, pd.DataFrame)
del X["id"]
del X["string"]
print(X.columns)
X = (X - X.mean()) / (X.max() - X.min())  # normalizing the features

range_n_clusters = [4, 6]
for n_clusters in range_n_clusters:
    clusterer = KMeans(n_clusters=n_clusters, random_state=10)
    cluster_labels = clusterer.fit_predict(X)
    centers = clusterer.cluster_centers_
    print("\n %s clusters:" % n_clusters)
    print("cluster labels: %s" % cluster_labels)
    print("cluster centers: %s " % centers)

    for k in range(n_clusters):
        print("\ncluster %d consists of the following strings:" % k)
        print(new_data["string"][cluster_labels == k])
