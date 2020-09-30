from enum import Enum


class Function(Enum):
    SEARCH = "search"
    REPOS = "repos/"
    ORGS = "orgs/"
    USERS = "users/"
    ZEN = "zen/"
    SELF = "user/"


def build_starting_url(function, root="https://api.github.com/"):
    if root[-1] != "/":
        root += "/"

    return root + function.value


def add_subdirectories(url, values):
    return url + "/".join(values)


def paginate(url, page, per_page):
    return url + f"?page={page}&per_page={per_page}"
