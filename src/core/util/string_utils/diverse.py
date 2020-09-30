import re
from urllib import parse

from uritemplate import URITemplate


def is_r_file(filename):
    matcher = re.compile(r'.+\.[rR]')
    return matcher.fullmatch(filename) is not None


def get_rel_entries(entry_list):
    return re.sub(r' rel="', '', entry_list[1]).strip('"'), \
           URITemplate(re.sub(r'[<>]', '', entry_list[0]))


def get_page_number(url_string):
    parsed_url = parse.urlparse(url_string)
    query_variables = parse.parse_qs(parsed_url.query)
    return int(query_variables["page"][0])
