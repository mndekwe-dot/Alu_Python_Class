move_zeros = [1,0,1,2,0,1,3]

def move_zeros(lst):
    i =0
    for item in lst:
        if item == 0:
            lst[i],lst[i+1] = lst[i+1],lst[i]
            i += 1
        else:
            i += 1
    return lst
print (move_zeros([3,5,0,6,0,7]))