""" Represent multiple data utilities used by flask contact blueprint """
import inspect

class AllowedList:
    """ List that represent allowed items

    Use '*' String to allow anything
    Use '' or None to allow nothing
    Use a space separated list or an array to allow only those items
    """

    def __init__(self, allowed_items):
        self.allowed_items = allowed_items or []

    def items(self):
        """ return allowed items as a list """
        if isinstance(self.allowed_items, str):
            return self.allowed_items.split(' ')
        return self.allowed_items

    def __contains__(self, key):
        """ Return wether the specified key is allowed """
        if self.allowed_items == '*':
            return True
        return key in self.items()

    def filter(self, obj):
        """ Filter object keys by wether it is allowed """
        if isinstance(obj, dict):
            for key, item in obj.items():
                if key in self:
                    yield key, item
        else:
            for key in obj:
                if key in self:
                    yield key


def filter_args(dict_to_filter, fn):
    """ Function that filter +dict_to_filter+ to work with fn """
    # Taken from https://stackoverflow.com/questions/26515595/how-does-one-ignore-unexpected-keyword-arguments-passed-to-a-function

    sig = inspect.signature(fn)
    filter_keys = [param.name for param in sig.parameters.values() if param.kind == param.POSITIONAL_OR_KEYWORD]
    filtered_dict = {filter_key:dict_to_filter[filter_key] for filter_key in filter_keys}
    return filtered_dict

def get_domain(url):
    """ Return the domain part of an url """
    # Taken from https://www.quora.com/How-do-I-extract-only-the-domain-name-from-an-URL

    return url.split('//')[-1].split('/')[0]
