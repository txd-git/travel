import random
def random_word(n,list01):
    count1=0
    for i in range(n):
        ch=chr(random.randrange(ord('A'),ord('Z')))
        list01.append(ch)
        count1 += 1
        if count1 == n:
            return