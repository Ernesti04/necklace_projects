import timeit as timer
import math
import necklace_generation_algorithms_from_various_sources as vnga # various necklace gen algorithms

# To use:
# when adding new algorithms: import any new methods or define them below,
# add case into test function that calls the method, add name into types_arr
#
# at the bottom of the program there is a list of variables, they determine
# the parameters of the test including how many times to run in order to gather
# an average. once all parameters look acceptable run the program to get results

def basic_gen_a(n, lim):
    if lim == 0:
        lim = 2**n
    x = 1
    uniques = []
    while (x < 2**(n-1) and len(uniques) < lim):
        s = str(bin(x)[2:].zfill(n))
        cycle = []
        for i in range(1, len(s)+1):
            rot = s[i:] + s[:i]
            cycle.append(rot)
            if rot < s:
                continue
        if min(cycle) == s:
            uniques.append([x, s])
        x += 2
    #print(n, len(uniques))
        
def basic_gen_b(n, lim):
    if lim == 0:
        lim = 2**n
    x = 1
    uniques = []
    while (x < 2**(n-1) and len(uniques) < lim):
        s = str(bin(x)[2:].zfill(n))
        cycle = []
        for i in range(len(s)-1):
            rot = s[(n - i):] + s[:(n - i)]
            cycle.append(rot)
            if rot < s:
                break
        if min(cycle) == s:
            uniques.append([x, s])
        x += 2
    #print(n, len(uniques))

def basic_gen_c(n, lim):
    if lim == 0:
        lim = 2**n
    x = 1
    uniques = []
    while (x < 2**(n-1) and len(uniques) < lim):
        s = str(bin(x)[2:].zfill(n))
        cycle = []
        for i in range(len(s)//2 +1):
            rot = s[i:] + s[:i]
            rotb = s[(n - i):] + s[:(n - i)]
            cycle.append(rot)
            cycle.append(rotb)
            if rot < s or rotb < s:
                break
        if min(cycle) == s:
            uniques.append([x, s])
        x += 2
    #print(n, len(uniques))
        
def test(n, k, lim, t):
    match t:
        case 0:
            basic_gen_a(n, lim)
        case 1:
            basic_gen_b(n, lim)
        case 2:
            basic_gen_c(n, lim)
        case 3:
            vnga.run_CRSMS(n, k)
        case 4:
            vnga.run_combos(n, k)
        case _:
            raise ValueError(f"Requested test ({t}) not found in list of tests under test()")

def _round(number, digits):
    number = round(number, digits)
    return str(number) + (" " * (digits - len( str(number).split(".")[1] ) ) )

def main(a, b, c, d, k):
    testing_start = timer.default_timer()
    types_arr = ["left rotation array", "right rotation array", "mixed rotation array", "CRSMS algorithm ", "Combos method   "]
    phrases_arr = ["of size \t", " took \t", "\tseconds on average"]
    results = [types_arr, [], [0*w for w in range(len(types_arr))], [], 0]
    #print(results)
    print("-" * 100)
    
    for i in range(a, b+1):
        results = [types_arr, [], [0*w for w in range(len(types_arr))], [], 0]
        for j in range(1, c+1):
            for t in range( len( results[0] ) ):
                # rotate left
                time_start = timer.default_timer()
                test(i, k, d, t) # = n(length), k(alphabet size), d(necklace limit), t(test to run)
                time_end = timer.default_timer()
                results[2][t] = (results[2][t] +  (time_end - time_start))
        
        # get average times for current length for each method
        for j in range(len(results[2])):
            results[2][j] = round(  results[2][j]  /c, 4 )
        
        # group times for average and fastest
        for j in results[2]:
            results[3].append(j) # combine values into seperate array for processing
            results[4] += j
        #results.append(t_basic_gen_a[3] + t_basic_gen_b[3] + t_basic_gen_c[3])
        #print(results)
        
        # process times for fastest
        best_type = types_arr[results[3].index(min(results[3]))] # get the fastest type by the name
        best_time = min(results[3]) # get the fastest type by time
        
        # process time differences for two fastest times
        results[3].pop( results[3].index(best_time) ) # get rid of the lowest time
        diff = min(results[3]) - best_time # use the remaining (second) lowest to get difference
        
        # get number of necklaces generated to include in testing results
        if d != 0:
            # calculate max number of necklaces for current length, use instead if smaller than given maximum
            lim = min(d, int(( (1/i) * sum(2**(math.gcd(k, i)) for k in range(1, i+1)) ) - 2))
        else:
            lim = 0
        
        # print out results for the current length tested
        print()
        for j in range(len(results[0])):
            print(results[0][j], phrases_arr[0], i, phrases_arr[1], _round(results[2][j], 4), phrases_arr[2], (f'for {lim} necklaces.' * int( d != 0)))
        print()
        print("Length", i, "average: ", _round(results[4]/len(types_arr), 4)+"s ")
        print("Fastest was", best_type, "by",  _round(diff, 4)+"s" )
        print()
        print("-" * 100)
        
    testing_end = timer.default_timer()
    print("Total testing time: \t", round(testing_end-testing_start, 2), "seconds")

if __name__ == "__main__":
    a = 13 # the binary length to start testing
    b = 13 # the number to stop testing on (inclusive). match with a to only test one length
    k = 2 # alphabet size for other algorithms, leave at 2 to keep all at binary
    c = 3 # the number of times each length is tested to generate an average, more rounds is more accurate but takes longer
    d = 0 # the target number of necklaces to generate before stopping. will generate full list if set to 0 or above max possible for length
    # total time will be influenced by (#of algorithms to test * #of lengths to test * #of rounds)
    # each time is measured from before the function call until it returns to main, printing times should not influence calculations
    # an average time overall is given, along with the fastest method and the difference between the two fastest
    main(a, b, c, d, k)

