
def get_if_exists(data, key, default=None):
    return data[key] if key in data else default
