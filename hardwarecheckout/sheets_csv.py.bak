import requests

class SheetsImportError(Exception):
    def __init__(self, msg):
        self.msg = msg 

    def __str__(self):
        return repr(self.msg)

# This function returns a list of dictionaries. The input is a google spreadsheet link (after publishing it to the web)
# and the output is list of a dictionary for each row (excluding the first row). The keys are the first row with the data from every other row.
def get_csv(u):
    tokens = u.split('/')

    for t, i in zip(tokens, range(len(tokens))):
        if t == 'd':
            id = tokens[i+1]
            break

    url = """https://docs.google.com/spreadsheets/d/{id}/export?format=tsv&id={id}&gid=0""".format(id=id)
    r = requests.get(url, allow_redirects=False)
    if r.status_code == 302:
        raise SheetsImportError('Unable to load sheet. Please make sure sharing is on!')

    lines = r.text.split('\n')

    dictionary_list = []

    # the first row will be the keys for each dictionary
    dic_keys = lines[0].replace('\r', '').split('\t')

    # skip the first row when constructing the dictionary list
    for l in range(1, len(lines)):
        temp_dic = {}
        items = lines[l].split('\t')
        for i in range(len(items)):
            temp_dic[dic_keys[i]] = items[i].replace('\r', '') # remove '\r' character from some entries
        dictionary_list.append(temp_dic)

    return dictionary_list
