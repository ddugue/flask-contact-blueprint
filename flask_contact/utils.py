""" Represent multiple data utilities used by flask contact blueprint """

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
