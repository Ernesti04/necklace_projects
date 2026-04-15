# ----------------------------------------------------------------------------------------------------
#  CRSMS algorithm from https://www.allisons.org/ll/AlgDS/Recn/Necklaces/
#  Converted to python 
# ----------------------------------------------------------------------------------------------------
crsms_necklaces = []
def run_CRSMS(n, k):
    s = []
    for i in range(n+2):
        s.append(0)
    crsms(n, k, s, 1, 1)

# length, alphabet size, current string, position, p (periodic)
def crsms(n, k, s, pos, p):
    # if length of string doesn't match n yet
    if pos <= n: # if not all bits gone through on current path
        s[pos] = s[pos - p] # copy bit at current position left
        crsms(n, k, s, pos+1, p) # continue current branch at next position
        for tmp_bit in range(s[pos] + 1, k): # for remaining options (out of k) on current bit 
            s[pos] += 1 # shift current bit to next option
            crsms(n, k, s, pos+1, pos) # start new branch based on that
    else: # length of string matches desired length, this branch is done
        if n % p == 0: # if p is a multiple of  or equal to n
            ln = [] # create array to store necklace
            for j in range(1, pos): # loop through s from 1 to n+1
                ln.append(str(s[j])) # group together portion of s that has necklace, make string to store easier
            global crsms_necklaces
            crsms_necklaces.append(''.join(ln))
            #print(''.join(ln)) # display the necklace, can store it instead
        #else:
            #print(".") # dead end

# ----------------------------------------------------------------------------------------------------
#  Unrestricted Necklaces gen algorithm from https://combos.org/necklace
#  Stripped down from source code
# ----------------------------------------------------------------------------------------------------

combos_current_sequence = []
combos_necklaces = []
combos_count = 1

def run_combos(n, k):
    for i in range(n+2):
        combos_current_sequence.append("0")
    combos_necklace(1, 1, n, k)

def combos_print(n):
    global combos_current_sequence
    global combos_count
    global combos_necklaces
    #print( f'{combos_count}: ', ''.join( combos_current_sequence[1:n+1] ) )
    combos_necklaces.append(''.join( combos_current_sequence[1:n+1] ))
    combos_count += 1

def combos_necklace(t, p, n, k):
    global combos_current_sequence
    j = 0
    
    if (t > n):
        if n%p == 0:
            combos_print(n)
    else:
        combos_current_sequence[t] = str( combos_current_sequence[t-p] )
        combos_necklace( t+1, p, n, k )
        j = int( combos_current_sequence[t-p] ) + 1
        while j <= k-1:
            combos_current_sequence[t] = str(j)
            combos_necklace( t+1, t, n, k )
            j += 1


# ----------------------------------------------------------------------------------------------------
#  KFM algorithm as detailed in https://sci-hub.st/10.1016/0196-6774(92)90047-G
#  Generates an incomplete list of necklaces at a fairly quick speed
# ----------------------------------------------------------------------------------------------------
kfm_necklaces = []
def kfm(n, k):
    #n = 6 # length
    #k = 2 # alphabet size, 2 = binary
    a = []

    for i in range(n):
        a += "0"
    #print("0"*n)

    i = n-1#str(bin(x)[2:].zfill(n))

    while i != 0:
        a[i] = str(int(a[i])+1)
        
        for j in range(1, n-i):
            a[j+i] = a[j]
            
        if n%i == 0:
            #print(a)
            global kfm_necklaces
            kfm_necklaaces.append(''.join(a))
            #print(''.join(a))
        i = n-1
        
        while int(a[i]) == k-1:
            i = i-1
    #print("1"*n)

# ----------------------------------------------------------------------------------------------------
#  GNNA algorithm as detailed in https://sci-hub.st/10.1016/0196-6774(92)90047-G
#  Generating Necklaces New Algorithm page 16 (429) fig. 5
# ----------------------------------------------------------------------------------------------------

gnna_necklaces = [] # use this for the check step, if string in min rotation (to reduce checks) not in list then it's a necklace
def run_gnna(n): # compatability function to convert n length into bit string of n 0s    y = [1]
    global gnna_necklaces
    y = []
    print("0" * n)
    for i in range(n-1):
        y.append(0)
    y.append(1)
    
    gnna_necklaces.append("0"*(n-1) + "1")
    gnna(y, 1) # run algorithm
    gnna_necklaces.sort()
    #gnna_necklaces_sorted = gnna_necklaces.sort()
    print(gnna_necklaces)

def gnna(y, j):
    s = []
    for bit in y:
        s.append( str(bit) )
    s =''.join( s )
    #print("\t"*(2*(j-1)), s)
    
    done = False
    
    j = 1
    while not done:
        # sigma function (rotate bits left by j)
        print(j, y, y[j:], y[:j], y[j:] + y[:j], "\n")
        y = y[j:] + y[:j] #y = sigma(y, j)
        # tau function (get compliment (0->1, 1->0) of last bit)
        z = y
        z[-1] = int( not ( z[-1] ) )# tau(y)
        
        if gnna_check(z) == True:
#             while True:
#                 gnna(z, j)
#                 j+= 1
#                 if j >= len(y):
#                     break
            gnna(z, j)
            j += 1
        else:
            s2 = []
            for bit in z:
                s2.append( str(bit) )
            s2 =''.join( s2 )
            
            #print("\t"*(2*(j-1)), s, s2, "fail")
            done = True

# if z is necklace
def gnna_check(z):
    global gnna_necklaces
    
    s = []
    for x in z:
        s.append( str(x) )
    s =''.join( s )
    
    cycle = []
    for i in range(1, len(s)+1):
        rot = s[i:] + s[:i]
        cycle.append(rot)
        #print("\t", rot)
        
    if min(cycle) not in gnna_necklaces:
        gnna_necklaces.append( min(cycle) )
        #print(gnna_necklaces)
        return True
    #print("False", s)
    return False

# ----------------------------------------------------------------------------------------------------
#  ---------------------------------------------- Main ----------------------------------------------
# ----------------------------------------------------------------------------------------------------

def main(n, k):
    run_CRSMS(n, k)
    run_combos(n, k)
    kfm(n, k)
    run_gnna(n)


if __name__ == "__main__":
    n = 5
    k = 2
    #main(n, k)
