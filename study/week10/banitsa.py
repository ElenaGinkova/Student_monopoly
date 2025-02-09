from secret import clue
def lucky():
    #[00000{111}]
    first_res = clue(left_shift = 5) >> 5
    #[{111}00(000)]
    second_res = clue(right_shift = 5) << 5
    #[(000){1}0(000)]
    third_res = clue(bw_and = 16)
    #[(111)(1){0}(111)]            [0000{1}000]
    fourth_res = clue(bw_or = 247) & 8
    number = first_res | second_res | third_res | fourth_res
    return number