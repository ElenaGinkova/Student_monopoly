import re


MAX_AGE = 5


class Santa:
    """"Singleton class. Contains all kids and their wishes"""
    _instance = None

    #kid => present
    _kids_presents = {}

    def __find_signiture(self, letter):
        return re.search(r'^\s*(\d+)\s*$', letter, flags=re.MULTILINE).group(1)

    def __find_present(self, letter):
        return re.search(r'(["\'])([A-Za-z0-9\s]*)\1', letter).group(2)

    def __new__(cls):
        if not cls._instance:
            cls._instance = object.__new__(cls)
        return cls._instance

    def new_kid(self, kid):
        self._kids_presents[kid] = None

    def __matmul__(self, letter):
        """Letter to Santa"""
        signature = self.__find_signiture(letter)
        present = self.__find_present(letter)
        for kid in self._kids_presents.keys():
            if str(id(kid)) == signature:
                self._kids_presents[kid] = present
                break
    
    def __call__(self, kid, wish):
        """Phone Santa"""
        present = self.__find_present(wish)
        self._kids_presents[kid] = present

    def __iter__(self):
        return self._generator()

    def _generator(self):
        for kid, present in self._kids_presents.items():
            if present is not None:
                yield present

    def __most_wanted(self):
        presents_counter = {}
        curr_present = None
        curr_max_count = 0
        for kid, present in self._kids_presents.items():
            if present:
                presents_counter[present] = presents_counter.get(present, 0) + 1
                if presents_counter[present] > curr_max_count:
                    curr_present = present
                    curr_max_count = presents_counter[present]
        return curr_present

    def xmas(self):
        def_present = self.__most_wanted()

        for kid, present in self._kids_presents.items():
            if kid.age <= MAX_AGE and def_present:
                if kid.naughty:
                    present = 'coal'
                if not present:
                    present = def_present
                kid(present)
                self._kids_presents[kid] = None
            kid.age += 1
            kid.naughty = False


class Kid(type):
    """"Meta class. Ensures there is a call method in the class that will inherit the metacls. Has logic if a kid has thrown an exception to mark him as naughty"""
    def __call__(cls, *args, **kwargs):
            instance = super().__call__(*args, **kwargs)
            Santa().new_kid(instance)
            instance.age = 0
            instance.naughty = False
            return instance

    def __new__(cls, name, bases, attr_dict):
        if '__call__' not in attr_dict:
            raise NotImplementedError('Оправи си детето?! Не чува, като го викаш!')
        for key, value in attr_dict.items():
            #                           because otherwise it wrappes all my dunders :((
            if callable(value) and not str(key).startswith('_'):
                func = value
                def wrapped(self, *args, **kwargs):
                    try:
                        func(self, *args, **kwargs)
                        self.naughty = False
                    except Exception as e:
                        self.naughty = True
                        raise e
                attr_dict[key] = wrapped
        return super().__new__(cls, name, bases, attr_dict)


class Bulgarian_kid(metaclass = Kid):
    def __call__(self, present):
        print(f"i got {present}")

    def be_naughty(self):
        raise TypeError('eho')

s = Santa()
gosho = Bulgarian_kid()
raqa = Bulgarian_kid()
wish = f"lalalllalalla\n {id(gosho)} \n iskam 'Nintendo'"
s @ wish
s(raqa, f"'buhalka'")
s.xmas()
print("new year")
s(gosho, "sadsad 'topka'")
try:
    raqa.be_naughty()
except TypeError as a:
    print("naughty")
s.xmas()
