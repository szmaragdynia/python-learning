'''
A Pythagorean triplet is a set of three natural numbers, a < b < c, for which,

a^2 + b^2 = c^2
For example, 3^2 + 4^2 = 9 + 16 = 25 = 5^2.

There exists exactly one Pythagorean triplet for which a + b + c = 1000.
Find the eproduct abc.
'''
#todo: recursive? not sure.
#todo: more elegant approach, maybe task-specific?

#unbelievably ugly code below, beware. Old, rude, bruteforce approach.
#chociaz czy to serio takie brzydkie? moze po prostu staram sie bardziej general approach miec.

import math

a = 0
b = 0
c = 0

#for sake not making things way more calculation heavy than they has to be, this func is deprecated
#(Id have to parse through list of triplets and check each if is a+b+c = 1000. This is too pointless even for such simple task)
def find_triplets(amount): 
    triplet = []
    triplets = []
    arbitrary_range_end = 100
    enough = False
    while enough == False:
        for a in range(1, arbitrary_range_end):
            if enough:
                break
            for b in range(1, arbitrary_range_end):
                if enough:
                    break
                if (math.sqrt(a**2 + b**2)).is_integer():
                    triplet = [a,b, int(math.sqrt(a**2 + b**2))]
                    triplets.append(triplet)
                    if len(triplets) == amount:
                        enough = True
        #if program is here, then it did not find enough triplets or it leaves due to break. Wider range then.
        #this is done in a bad manner. Do not do this like that. (pointless re-doing the calculations)
        #but the task is so simple I do not care
        if not enough:
            triplet = []
            triplets = []
            arbitrary_range_end = arbitrary_range_end+100                        
    return triplets


def find_special_triplet(): 
    triplet = []
    triplets = []
    arbitrary_range_end = 100
    special_found = False
    while special_found == False:
        for i in range(1, arbitrary_range_end):
            if special_found:
                break
            for j in range(1, arbitrary_range_end):
                if special_found:
                    break
                if (math.sqrt(i**2 + j**2)).is_integer():
                    triplet = [i,j, int(math.sqrt(i**2 + j**2))]
                    triplets.append(triplet)
                    if triplet[0] + triplet[1] + triplet[2] == 1000:
                        special_found = True
        #if program is here, then it did not find enough triplets or leaves due to break. Wider range then
        #this is done in a bad manner. Do not do this like that. (pointless re-doing the calculations)
        #but the task is so simple I do not care
        if not special_found:
            triplet = []
            triplets = []
            arbitrary_range_end = arbitrary_range_end+100                        
    return triplet

print (find_special_triplet())
print (find_special_triplet()[0]*find_special_triplet()[1]*find_special_triplet()[2])

