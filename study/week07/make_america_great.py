class Material:
    DENSITY = 0

    def __init__(self, mass):
        self.mass = mass
        self.valid = True

    @property
    def volume(self):
        return self.mass / self.DENCITY

    def invalidate(self):
        if self.valid:
            self.valid = False
            return True
        return False


class Concrete(Material):
    DENCITY = 2500


class Brick(Material):
    DENCITY = 2000


class Stone(Material):
    DENCITY = 1600


class Wood(Material):
    DENCITY = 600


class Steel(Material):
    DENCITY = 7700


CLASS_REGISTER = {'Concrete' : Concrete, 'Brick' : Brick, 'Stone' : Stone, 'Wood' : Wood, 'Steel' : Steel}


class Factory:
    all_materials = []

    def __init__(self):
        self.materials = []

    def help_generate_class(self, *args): 
        new_args = []
        dencity = 0
        count = 0
        mass = 0
        for item in list(*args):
            if not item.invalidate():
                raise AssertionError
            self.remove_material(item)
            args_name = item.__class__.__name__.split('_')
            for element in args_name:
                dencity += CLASS_REGISTER[element].DENCITY
                count += 1
            new_args.extend(args_name)
            mass +=  item.mass
        return '_'.join(str(item).capitalize() for item in sorted(new_args)), dencity // count, mass

    def add_instance(self, material, value):
        material_instance = CLASS_REGISTER[material](value)
        self.materials.append(material_instance)
        return material_instance

    def call_with_kwargs(self, **kwargs):
        res = []
        for material, value in kwargs.items():
            if material not in CLASS_REGISTER:
                raise ValueError
            res.append(self.add_instance(material, value))
        self.all_materials.extend(self.materials)
        return tuple(res)

    def call_with_args(self, *args):
        name, dencity, mass = self.help_generate_class(args)
        if name in CLASS_REGISTER:
            material_instance = self.add_instance(name, mass)
            self.all_materials.extend(self.materials)
            return material_instance
        else:
            DynamicClass = type(name, (Material,), {'DENCITY' : dencity})
            CLASS_REGISTER[name] = DynamicClass
            material_instance = self.add_instance(name, mass)
            self.all_materials.extend(self.materials)
            return material_instance

    def __call__(self, *args, **kwargs):
        if args and kwargs or not args and not kwargs:
            raise ValueError
        if kwargs:
            return self.call_with_kwargs(**kwargs)
        return self.call_with_args(*args)
    
    def remove_material(self, material):
        if material in self.materials:
            self.materials.remove(material)
            self.all_materials.remove(material)

    @property
    def volume(self):
        volume_sum = sum(item.volume for item in self.materials)
        return volume_sum

    def can_build(self, desired_volume):
        return desired_volume <= self.volume

    @classmethod
    def can_build_together(cls, desired_volume):
        volume = 0
        for item in cls.all_materials:
            volume += item.volume
        return desired_volume <= volume