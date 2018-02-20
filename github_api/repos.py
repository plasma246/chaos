import arrow
import settings
import logging
from requests import HTTPError

__log = logging.getLogger("github_api.repos")


def get_path(urn):
    """ return the path for the repo """
    return "/repos/{urn}".format(urn=urn)


def get_num_watchers(api, urn):
    """ returns the number of watchers for a repo """
    data = api("get", get_path(urn))
    # this is the field for watchers.  do not be tricked by "watchers_count"
    # which always matches "stargazers_count"
    return data["subscribers_count"]


def set_desc(api, urn, desc):
    """ Set description and homepage of repo """
    path = get_path(urn)
    data = {
        "name": settings.GITHUB_REPO,
        "description": desc,
        "homepage": settings.HOMEPAGE,
    }
    api("patch", path, json=data)


def get_creation_date(api, urn):
    """ returns the creation date of the repo """
    data = api("get", get_path(urn))
    return arrow.get(data["created_at"])


def get_contributors(api, urn):
    """ returns the list of contributors to the repo """
    return api("get", "/repos/{urn}/stats/contributors".format(urn=urn))


def create_label(api, urn, name, color="ededed"):
    """ create an issue label for the repository """
    data = {
        "name": name,
        "color": color
    }
    resp = None
    try:
        resp = api("post", "/repos/{urn}/labels".format(urn=urn), json=data)
    except HTTPError as e:
        if e.response.status_code == 422:
            update_label(api, urn, name, color)
        else:
            __log.exception("couldn't create label")
    return resp


def update_label(api, urn, name, color="ededed"):
    """ update an issue label for the repository """
    data = {
        "name": name,
        "color": color
    }
    resp = None
    try:
        resp = api("patch", "/repos/{urn}/labels/{name}".format(urn=urn, name=name), json=data)
    except HTTPError:
        __log.exception("couldn't update label")
    return resp
