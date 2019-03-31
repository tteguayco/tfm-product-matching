import re


def preprocess(attr_list, with_rows_removal=True):
    # Lowercase words
    attr_list = [x.lower() for x in attr_list]

    # Remove punctuation
    attr_list = [re.sub(r'[^\w\s]', '', x) for x in attr_list]

    # Remove NULL values
    if with_rows_removal:
        attr_list = [x for x in attr_list if str(x) != 'nan']

    # Remove duplicates
    if with_rows_removal:
        attr_list = list(set(attr_list))

    # Trim surrounding spaces
    attr_list = [x.strip() for x in attr_list]

    # Remove sequential spaces
    attr_list = [re.sub(r'\s{2,}', ' ', x) for x in attr_list]

    return attr_list
