import json
import configurer as config

SFILE = config.get("status")


def write(status):
    with open(SFILE, 'w') as f:
        json.dump(status, f, indent=4)


def clear():
    write({})
    return {}


def read():
    try:
        with open(SFILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}
    except FileNotFoundError:
        return clear()


def add(path, pid, stdout):
    status = read()

    status.update({path: {"pid": pid, "stdout": stdout}})

    write(status)


def exists(path):
    status = read()

    return path in status


def remove(path):
    '''
    returns success of removing of the item, True if remove successful else False
    '''
    path = str(path)
    if exists(path):
        status = read()
        try:
            status.pop(path)
        except:
            pass
        write(status)
        return True
    else:
        return False


def valid_key(key):
    if key in ["path", "paths", "PATH", "Paths", "pa"]:
        return "paths"
    elif key in ["pid", "PID", "Pid", "p", "pi"]:
        return "pid"
    elif key in ["stdout", "STDOUT", "Stdout", "output"]:
        return "stdout"
    else:
        return None


def get(path, key):
    '''
    returns value of key for a path. returns None if invalid key or path
    '''

    path = str(path)
    #key = valid_key(key)

    if exists(path):
        status = read()
        status_path = status.get(path)
        if status_path:
            return status_path.get(key)
        else:
            return None
    else:
        return None


def get_from_key(item, key, value):
    '''
    >>> get_from_key("path", "pid", 3225)
    '''

    all_values = get_all(key)
    if all_values and value in all_values:
        index = all_values.index(value)
        #item_key = valid_key(item)

        paths = get_all("paths")
        path = None

        if bool(paths):
            try:
                path = paths[index]
            except:
                open('errors.txt', 'a').write("ERROR (from line 107 in status.py) PATHS: =>"+str(paths)+"\n")
                return None
        else:
            return None

        if item == "paths":
            return path
        else:
            return get(path, item)


def get_all(key):
    status = read()
    if status:
        paths = list(status.keys())
        #key = valid_key(key)
    else:
        return []

    if key == "paths":
        return paths
    else:
        values = []
        for path in paths:
            value = get(path, key)
            if value is not None:
                values.append(value)
        return values


def is_empty():
    return not bool(read())


def read_list():
    status = read()

    status_list = []
    for k, v in status.items():
        v_items = list(v.values())
        status_list.append([k]+v_items)

    return status_list
