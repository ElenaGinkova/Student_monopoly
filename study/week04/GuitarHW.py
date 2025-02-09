INTERVALS = ['unison','minor 2nd', 'major 2nd', 'minor 3rd', 'major 3rd', 'perfect 4th', 'diminished 5th', 'perfect 5th', 'minor 6th', 'major 6th', 'minor 7th', 'major 7th']
ORDER = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
MINOR_3RD = 3
MAJOR_3RD = 4


class Tone:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __add__(self, other):
        if type(other) is Tone:
            return Chord(self, other)
        elif type(other) is Interval:
            tone_index = other.number_of_semitones
            tone_index += ORDER.index(self.name)
            tone_index %= 12
            return Tone(ORDER[tone_index]) 

    def __sub__(self, other):
        if type(other) is Interval:
            return Tone(ORDER[(ORDER.index(self.name) - other.number_of_semitones) % 12])
        elif type(other) is Tone:
            return Interval(abs(ORDER.index(self.name) - ORDER.index(other.name)) % 12)

    def __eq__(self, other):
        return self.name == other.name
        

class Interval:
    def __init__(self, number_of_semitones):
        self.number_of_semitones = number_of_semitones 

    def __str__(self):
        interval = self.number_of_semitones % 12
        return INTERVALS[interval]

    def __add__(self, other):
        if type(other) is Tone:
            raise TypeError('Invalid operation')
        elif type(other) is Interval:
            res = (self.number_of_semitones + other.number_of_semitones) % 12
            return Interval(res)

    def __neg__(self):
         return Interval(-self.number_of_semitones)



def sort_tones(root, tones):
    # rotating the ORDER list based on the root index
    root_index = ORDER.index(root)
    rotated_ORDER = ORDER[root_index:] + ORDER[:root_index]
    ORDER_index = {char: idx for idx, char in enumerate(rotated_ORDER)}
    return sorted(tones, key = lambda x: ORDER_index[x]) # custom sorting func


def remove_duplicates(input_list):
    seen = set()
    return [x for x in input_list if not (x in seen or seen.add(x))]


class Chord:
    def __init__(self, main_tone, *args):
        tones_names_list = []
        for el in args:
            tones_names_list.append(el.name)
        if main_tone.name in tones_names_list:
            tones_names_list.remove(main_tone.name)
        tones_names = set(tones_names_list)
        if len(tones_names) == 0:
            raise TypeError('Cannot have a chord made of only 1 unique tone')
        self.root = main_tone
        self.tones = args

    def __str__(self):
        res = self.root.name
        tones = []
        for el in self.tones: tones.append(el.name)
        sorted = remove_duplicates(sort_tones(self.root.name, tones))
        for el in sorted: 
            if el != self.root.name:
               res = f'{res}-{el}'
        return res

    def is_minor(self):
        for el in self.tones:
            if abs(ORDER.index(self.root.name) - ORDER.index(el.name)) == MINOR_3RD:
                return True
        return False

    def is_major(self):
        for el in self.tones:
            if abs(ORDER.index(self.root.name) - ORDER.index(el.name)) == MAJOR_3RD:
                return True
        return False

    def is_power_chord(self):
        return not self.is_major() and not self.is_minor()

    def __add__(self, other):
        if type(other) is Tone:
            return Chord(self.root, *self.tones, other)
        elif type(other) is Chord:
            return Chord(self.root, *self.tones, other.root, *other.tones)

    def __sub__(self, other):
        if type(other) is Tone:
            tones = []
            for el in self.tones: tones.append(el.name)
            sorted = remove_duplicates(sort_tones(self.root.name, tones))
            if other not in self.tones and other != self.root:
                raise TypeError(f'Cannot remove tone {str(other)} from chord {str(self)}')
            if self.root.name in sorted and len(sorted) < 3 or len(sorted) + 1 < 3:
                raise TypeError('Cannot have a chord made of only 1 unique tone')
            if self.root == other:
                if sorted[0] != self.root:
                   self.root = Chord(sorted[0])
                else:
                   self.root = Chord(sorted[1]) 
            res = []
            for el in sorted: 
                if el != other.name:
                   res.append(Tone(el)) 
            return Chord(self.root, *res)

    def transposed(self, interval):
        tones = []
        root = self.root
        for el in self.tones:
            tones.append(Tone(ORDER[(ORDER.index(el.name) + interval.number_of_semitones) % 12]))
        root = Tone(ORDER[(ORDER.index(root.name) + interval.number_of_semitones) % 12])
        return Chord(root, *tones)
    
 