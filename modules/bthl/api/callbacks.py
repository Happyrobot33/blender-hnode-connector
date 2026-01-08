callbacks = []

def add_callback(func):
    #enforce no duplicates
    remove_callback(func)
    callbacks.append(func)

def remove_callback(func):
    #check if callbacks has any entrys
    if not callbacks:
        return
    #check explicetly based on the name
    for existing_func in callbacks:
        if existing_func.__name__ == func.__name__:
            callbacks.remove(existing_func)

def run_callbacks(*args, **kwargs):
    """DONT CALL THIS! its internally used to trigger callbacks"""
    for func in callbacks:
        func(*args, **kwargs)
