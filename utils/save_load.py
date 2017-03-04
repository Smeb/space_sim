def save(params, obj):
    """Saves an object with a filename based on a list of parameters given
    Input:
        params - a list of items with the string method implemented (used as the name)
        obj - the item to save
    Output:
        - Side effect: an item will be saved at pickle_path with a hash based on the params
    """
    import pickle
    from config import pickle_path
    hsh = sanitise("_".join([str(param) for param in params]))
    fname = "{}/{}.dat".format(pickle_path, hsh)
    pickle.dump(obj, open(fname, 'wb'))

def load(params):
    """Loads an object using a filename based on a list of parameters given
        Input:
            params - a list of items with the string method implemented (used as the name)
        Output:
            The loaded data, or None if it fails
    """
    import os
    import pickle
    from config import pickle_path
    hsh = sanitise("_".join([str(param) for param in params]))
    fname = "{}/{}.dat".format(pickle_path, hsh)
    print(fname)
    if os.path.isfile(fname):
        print('loaded {}'.format(fname))
        return pickle.load(open(fname, 'rb'))
    return None

def sanitise(string):
    """Removes characters from a string which would interfere with unix compliant path specifications"""
    return "".join(c for c in string if c.isalpha() or c.isdigit() or c=='_').rstrip()
