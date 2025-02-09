def print_types(*allowed_types):
    str_of_types = ', '.join(str(el) for el in allowed_types)
    print(f'Invalid input arguments, expected {str_of_types}!')

def validate_in(args, allowed_types):
    return all(type(arg) in allowed_types for arg in args)

def validate_out(args, allowed_types):
    return type(args) in allowed_types

def type_check(direction):
    def decorator(*allowed_types):
        def check(func):
            def excecute_func(*args, **kwargs):
                if direction == 'in':
                    if not validate_in(args, allowed_types) or not validate_in(kwargs.items(), allowed_types):
                        print_types(*allowed_types)
                returned_values = func(*args, **kwargs)
                if direction == 'out' and not validate_out(returned_values, allowed_types):
                    print_types(*allowed_types)
                return returned_values
            return excecute_func
        return check
    return decorator