class LockPicker_1MI0600289():
    def __init__(self, lock):
        self.lock = lock  
   
    def unlock(self):
        args = []
        while True:
            try:
                self.lock.pick(*args)
                #no error was raised
                break
            except TypeError as exc:
                if exc.position is None:
                    #needs to expand
                    while len(*args) < exc.expected:
                        args.append(None)
                else:
                    #change type
                    args[exc.position - 1] = exc.expected(args[exc.position - 1])
            except ValueError as exc:
                #change element
                args[exc.position - 1] = exc.expected
        
                