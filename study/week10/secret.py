num = 42
def clue(**kwargs):
        operation, value = next(iter(kwargs.items()))

        if operation == 'left_shift':
            return (num << value) & 0xFF

        elif operation == 'right_shift':
             return num >> value

        elif operation == 'bw_and':
            return num & value

        elif operation == 'bw_or':
             return num | value