def is_valid_bush_name(element):
    if type(element) == dict and 'name' in element:
        name = element['name'].lower()
        if name in ('храст', 'bush', 'shrub'):
            return True
    return False

def filter_kwargs(kwargs):
    res = {}
    for name_of_element, element in kwargs.items():
        if is_valid_bush_name(element):
            res[name_of_element] = element
    return res
        
def ch_count(kwargs):
    res = set()
    for name in kwargs:
        for ch in name:
         res.add(ch)
    return len(res)
    
def find_price(args):
    price = 0
    for element in args:
        price += element.get('cost', 0)
    return price

def is_it_good(price, ch_count):
    if int(price) == 0 or int(price) > 42 or ch_count % int(price) != 0:
        return "Ni!" 
    return f'{price:.2f}лв'

def function_that_says_ni(*args, **kwargs):  
    args_filtered = list(filter(is_valid_bush_name, args))
    kwargs_filtered = filter_kwargs(kwargs)
    
    distinct_ch_count = ch_count(kwargs_filtered)
    
    args_filtered.extend(kwargs_filtered.values())
    
    price = find_price(args_filtered)
    return is_it_good(price, distinct_ch_count)