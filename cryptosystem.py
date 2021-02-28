# FDM CA Cryptosystem Simulator. Written by Adam Clarridge (3agc AT queensu D0T ca), 2008
# Usage: Simply run this script and use the on-screen menu.
# For more information, see the README.txt file.

import math,random,copy
from xml.dom import minidom

#The Fixed-Domain Marker Cellular Automaton class.
class FDM_CA:

    #constructor
    def __init__(self, dimension, state_set, neighbourhood):
        self.dimension = dimension
        self.state_set=state_set[:]

        #the neighbourhood is a tuple of tuples representing the set of dimension-
        #sized vectors corresponding to the CA"s neighbourhood.
        #Example: neighbourhood = ((1,0),(0,1),(-1,0),(0,-1)) is the 2-dimensional
        #von Neumann neighbourhood without the cell itself
        self.neighbourhood = neighbourhood

        #the transition_rules dictionary works as follows: if the neighbourhood
        #of a cell c is part of this CA"s acting_set, then if the state of c
        #is s, c will change to transition_rules[s] on the next generation.
        self.transition_rules={}
        #initialize transition_rules to the identity map.
        for s in state_set:
            self.transition_rules[s] = s

        #the acting set is a list of tuples corresponding to the neighbourhood
        #positions in the order of the self.neighbourhood tuple.
        #Example: acting_set = [(s1,s2,s3,s4),(s1,s1,s1,s2),(s3,s1,s1,s2)]
        # (here (s1,s2,s3,s4) corresponds to
        #               s2
        #            s3 c  s1
        #               s4
        #with the neighbourhood as in the example above.)
        self.acting_set = []

        #stores the inverse transition function
        self.inverse_transition_rules = {}

    #apply this CA to a given message for one generation.
    #the "message" input is a dictionary keyed by cell location.
    #So a message encoded into a 2x2 array may have the following entries:
    # message[(0,0)] = s1
    # message[(1,0)] = s2
    # message[(0,1)] = s3
    # message[(1,1)] = s4
    #messages in any rectangular shape are acceptable (higher dimensions than 2
    #are OK as well)
    def apply(self, message, sizes):
        tmp={}
        for key in list(message.keys()):
            nbhood = []
            for nb in self.neighbourhood:
                nbhood.append(message[vector_add(key,nb,sizes)])
            if tuple(nbhood) in self.acting_set:
                tmp[key] = self.transition_rules[message[key]]
            else:
                tmp[key] = message[key]
        return tmp

    #calculate the inverse transition function
    def calculate_inverse(self):
        for state in self.state_set:
            self.inverse_transition_rules[self.transition_rules[state]]=state

    #apply the inverse of this CA for one generation
    def apply_inverse(self, message, sizes):
        tmp={}
        for key in list(message.keys()):
            nbhood = []
            for nb in self.neighbourhood:
                nbhood.append(message[vector_add(key,nb,sizes)])
            if tuple(nbhood) in self.acting_set:
                tmp[key] = self.inverse_transition_rules[message[key]]
            else:
                tmp[key] = message[key]
        return tmp

#Creates a sequence of FDM RCA at initialization and composes them together to
#form one CA. Also provides encryption/decryption functions.
class FDM_CA_Cryptosystem():

    def __init__(self):
        self.generated = False
        self.read_private = False
        self.read_public = False
        self.have_parameters = False
        self.rows=0
        self.cols=0
        self.num_generations=0

    #method to write a public or private key to an xml file
    def write_key(self, filename, key_type):
        if key_type=="public":
            print("Writing public key to "+filename+"...", end=' ')
            #write a public key
            xml = minidom.Document()
            pubkey = xml.createElement("public_key")
            state_set_str = ""
            for state in self.state_set:
                state_set_str=state_set_str + state
            nbhd_str = ""
            for nb in range(0,len(self.neighbourhood)):
                for num in range(len(self.neighbourhood[nb])):
                    nbhd_str=nbhd_str + str(self.neighbourhood[nb][num])
                    if num<len(self.neighbourhood[nb])-1:
                        nbhd_str=nbhd_str + ","
                if nb<len(self.neighbourhood)-1:
                    nbhd_str = nbhd_str + ";"
            pubkey.setAttribute("state_set", state_set_str)
            pubkey.setAttribute("neighbourhood", nbhd_str)
            pubkey.setAttribute("dimension", str(self.dimension))

            for nbhd in self.composed_CA:
                nbhd_str = ""
                for state in nbhd:
                    nbhd_str = nbhd_str + state
                rule = xml.createElement("neighbourhood")
                rule.setAttribute("configuration",nbhd_str)
                for state in self.composed_CA[nbhd]:
                    rule2 = xml.createElement("map")
                    rule2.setAttribute("state",str(state))
                    rule2.setAttribute("next_state",str(self.composed_CA[nbhd][state]))
                    rule.appendChild(rule2)
                pubkey.appendChild(rule)

            xml.appendChild(pubkey)
            f = open(filename,"w")
            f.write(xml.toprettyxml())
            f.close()

            print("Done.")
        elif key_type=="private":
            print("Writing private key to "+filename+"...", end=' ')
            #write a private key
            xml = minidom.Document()
            privkey = xml.createElement("private_key")
            state_set_str = ""
            for state in self.state_set:
                state_set_str=state_set_str + state
            nbhd_str = ""
            for nb in range(0,len(self.neighbourhood)):
                for num in range(len(self.neighbourhood[nb])):
                    nbhd_str=nbhd_str + str(self.neighbourhood[nb][num])
                    if num<len(self.neighbourhood[nb])-1:
                        nbhd_str=nbhd_str + ","
                if nb<len(self.neighbourhood)-1:
                    nbhd_str = nbhd_str + ";"
            privkey.setAttribute("state_set", state_set_str)
            privkey.setAttribute("neighbourhood", nbhd_str)
            privkey.setAttribute("num_FDM_CA", str(len(self.FDM_CA_list)))
            privkey.setAttribute("dimension", str(self.FDM_CA_list[0].dimension))

            for i in range(0,len(self.FDM_CA_list)):
                fdmca = xml.createElement("FDM_CA")
                fdmca.setAttribute("number",str(i))
                ca = self.FDM_CA_list[i]
                actingset = xml.createElement("acting_set")
                for nbhd in ca.acting_set:
                    nbhd_elem = xml.createElement("nbhd")
                    nbhd_str = ""
                    for state in nbhd:
                        nbhd_str = nbhd_str+state
                    nbhd_elem.setAttribute("conf",nbhd_str)
                    actingset.appendChild(nbhd_elem)

                function = xml.createElement("function")
                for state in ca.transition_rules:
                    map_elem = xml.createElement("map")
                    map_elem.setAttribute("state",str(state))
                    map_elem.setAttribute("next_state",str(ca.transition_rules[state]))
                    function.appendChild(map_elem)

                fdmca.appendChild(actingset)
                fdmca.appendChild(function)
                privkey.appendChild(fdmca)

            xml.appendChild(privkey)
            f = open(filename,"w")
            f.write(xml.toprettyxml())
            f.close()
            print("Done.")
        else:
            print("Invalid key type. Please enter 'public' or 'private'.")

    def write_parameters(self,filename):
        print("Writing parameters to "+filename+"...", end=' ')
        xml = minidom.Document()
        params = xml.createElement("parameters")
        state_set_str = ""
        for state in self.state_set:
            state_set_str=state_set_str + state
        nbhd_str = ""
        for nb in range(0,len(self.neighbourhood)):
            for num in range(len(self.neighbourhood[nb])):
                nbhd_str=nbhd_str + str(self.neighbourhood[nb][num])
                if num<len(self.neighbourhood[nb])-1:
                    nbhd_str=nbhd_str + ","
            if nb<len(self.neighbourhood)-1:
                nbhd_str = nbhd_str + ";"
        CA_params = xml.createElement("CA_parameters")
        CA_params.setAttribute("dimension", str(self.dimension))
        CA_params.setAttribute("neighbourhood", nbhd_str)
        CA_params.setAttribute("state_set", state_set_str)
        alg_params = xml.createElement("algorithm_parameters")
        alg_params.setAttribute("numCA",str(self.num_CA))
        alg_params.setAttribute("p",str(self.p))
        alg_params.setAttribute("q",str(self.q))
        params.appendChild(CA_params)
        params.appendChild(alg_params)
        xml.appendChild(params)
        f = open(filename,"w")
        f.write(xml.toprettyxml())
        f.close()
        print("Done.")

    #method to read the algorithm parameters from a file
    def read_parameters(self, filename):
        try:
            print("Reading parameters from "+filename+"... ", end=' ')
            go=True
            dom = minidom.parse(filename)
        except:
            print("Error: File either cannot be read or is malformed XML.")
            go = False
        if go:
            params = dom.firstChild
            CA_params = params.getElementsByTagName("CA_parameters").item(0)
            alg_params = params.getElementsByTagName("algorithm_parameters").item(0)
            self.state_set = list(str(CA_params.getAttribute("state_set")))
            self.dimension = int(str(CA_params.getAttribute("dimension")))
            tmp_nbhd = str(CA_params.getAttribute("neighbourhood")).split(";")
            self.neighbourhood = []
            for nb in tmp_nbhd:
                n = []
                for num in nb.split(","):
                    n.append(int(num))
                self.neighbourhood.append(tuple(n))
            self.num_CA = int(str(alg_params.getAttribute("numCA")))
            self.p = float(str(alg_params.getAttribute("p")))
            self.q = float(str(alg_params.getAttribute("q")))
            self.have_parameters = True
            print("Done.")

    #method to read a public or private key from an xml file
    def read_key(self,filename,key_type):
        if key_type=="public":
            print("Reading public key from "+filename+"...", end=' ')
            #read a public key
            dom = minidom.parse(filename)
            pubkey = dom.firstChild
            self.state_set = list(str(pubkey.getAttribute("state_set")))
            self.dimension = int(str(pubkey.getAttribute("dimension")))
            tmp_nbhd = str(pubkey.getAttribute("neighbourhood")).split(";")
            self.neighbourhood = []
            for nb in tmp_nbhd:
                n = []
                for num in nb.split(","):
                    n.append(int(num))
                self.neighbourhood.append(tuple(n))
            self.composed_CA={}
            for nbhd_node in pubkey.getElementsByTagName("neighbourhood"):
                nbhd = tuple(list(str(nbhd_node.getAttribute("configuration"))))
                self.composed_CA[nbhd]={}
                for mapping_node in nbhd_node.getElementsByTagName("map"):
                    self.composed_CA[nbhd][mapping_node.getAttribute("state")]=mapping_node.getAttribute("next_state")

            self.read_public=True
            print("Done. Public key is now in memory.")
        elif key_type=="private":
            print("Reading private key from "+filename+"...", end=' ')
            #read a private key

            dom = minidom.parse(filename)
            privkey = dom.firstChild
            state_set = list(str(privkey.getAttribute("state_set")))
            tmp_nbhd = str(privkey.getAttribute("neighbourhood")).split(";")
            neighbourhood = []
            for nb in tmp_nbhd:
                n = []
                for num in nb.split(","):
                    n.append(int(num))
                neighbourhood.append(tuple(n))
            num_FDM_CA = int(str(privkey.getAttribute("num_FDM_CA")))
            self.dimension = int(str(privkey.getAttribute("dimension")))
            self.FDM_CA_list = []
            for i in range(num_FDM_CA):
                self.FDM_CA_list.append(FDM_CA(self.dimension,state_set,neighbourhood))

            for ca_node in privkey.getElementsByTagName("FDM_CA"):
                num = int(str(ca_node.getAttribute("number")))
                for acting_set_node in ca_node.getElementsByTagName("acting_set"):
                    for nbhd_node in acting_set_node.getElementsByTagName("nbhd"):
                        nbhd_tup = tuple(list(str(nbhd_node.getAttribute("conf"))))
                        self.FDM_CA_list[num].acting_set.append(nbhd_tup)
                for function_node in ca_node.getElementsByTagName("function"):
                    for map_node in function_node.getElementsByTagName("map"):
                        self.FDM_CA_list[num].transition_rules[str(map_node.getAttribute("state"))]=str(map_node.getAttribute("next_state"))
                self.FDM_CA_list[num].calculate_inverse()

            self.read_private = True
            print("Done. Private key is now in memory.")
        else:
            print("Invalid key type. Please enter 'public' or 'private'.")

    def generate_keys(self,dimension,state_set,neighbourhood,num_CA,p,q):
        self.dimension = dimension
        self.state_set = state_set[:]
        self.neighbourhood = neighbourhood
        self.neighbourhood_size = len(neighbourhood)
        self.num_states = len(state_set)
        self.num_CA = num_CA
        self.p=p
        self.q=q
        #the list of FDM CA objects to be composed together
        self.FDM_CA_list = []
        self.all_possible_neighbourhoods = self.generate_all_possible_neighbourhoods()
        #initialize the composed rule
        self.composed_CA = {}
        for nbhd in self.all_possible_neighbourhoods:
            tnbhd = tuple(nbhd)
            self.composed_CA[tnbhd] = {}
            for s in state_set:
                self.composed_CA[tnbhd][s]=s

        print("Generating the random FDM CA list...", end=' ')
        #Begin the algorithm to generate a random FDM CA list
        change_set = []
        the_rest = self.state_set[:]
        state = random.choice(the_rest)
        the_rest.remove(state)
        change_set.append(state)
        state = random.choice(the_rest)
        the_rest.remove(state)
        change_set.append(state)
        for i in range(0,self.num_CA):
            ca = FDM_CA(self.dimension,self.state_set,self.neighbourhood)

            if random.uniform(0.0,1.0)<p and the_rest!=[]:
                state = random.choice(the_rest)
                the_rest.remove(state)
                change_set.append(state)

            #choose the acting set for this FDM CA
            positions = self.random_binary(self.neighbourhood_size)
            for nbhd in self.all_possible_neighbourhoods:
                unchanging_neighbourhood = True
                rg = list(range(self.neighbourhood_size))
                for n in rg:
                    if nbhd[n] in change_set:
                        unchanging_neighbourhood = False
                        if positions[n]==True:
                            #accept the neighbourhood for sure in this case
                            ca.acting_set.append(nbhd)
                            break
                #if none of the neighbourhood states are part of the change set,
                # then accept the neighbourhood with probability q
                if unchanging_neighbourhood == True and random.uniform(0.0,1.0)<q:
                    ca.acting_set.append(nbhd)

            ca.transition_rules = self.random_transition_rules(change_set)
            ca.calculate_inverse()
            self.FDM_CA_list.append(ca)

        print("Composing into one CA...", end=' ')
        self.compose_CA()
        self.generated = True
        print("Done. The public and private keys are now in memory.")

    #generates a random binary string of a specified length
    #the binary string is useful in randomly choosing the acting_set
    #of an FDM_CA.
    def random_binary(self,length):
        num = int(random.uniform(0.0,1.0)*(2**length))
        list = []
        for i in range(length):
            if num/(2**(length-i-1))!=0:
                num-=2**(length-1-i)
                list.append(True)
            else:
                list.append(False)
        return list

    #Generates a list of all possible neighbourhoods. This is useful to
    #iterate through when finding the composed_CA.
    def generate_all_possible_neighbourhoods(self):
        nbhds = []
        total = self.num_states**self.neighbourhood_size
        for i in range(0,total):
            temp = []
            num=i
            for j in range(self.neighbourhood_size):
                temp.append(self.state_set[num/(self.num_states**(self.neighbourhood_size-j-1))])
                num-=(num/(self.num_states**(self.neighbourhood_size-j-1)))*(self.num_states**(self.neighbourhood_size-j-1))
            nbhds.append(tuple(temp))
        return nbhds

    #this function generates a random permutation of the given change_set,
    #and returns the result as a dictionary of outputs keyed by inputs.
    def random_transition_rules(self,change_set):
        cs = change_set[:]
        left = change_set[:]
        tr = {}
        for state in self.state_set:
            if state in cs:
                rand = random.choice(left)
                tr[state] = rand
                left.remove(rand)
            else:
                tr[state]=state
        return tr

    #encrypt a message using each of the CA in succession. This has the
    #same result as encrypting with the composed CA and was only used for
    #debugging and proof-of-concept purposes.
    def encrypt(self,message,num_iterations):
        sizes = [0]*self.dimension
        for key in list(message.keys()):
            for i in range(0,self.dimension):
                if key[i]>sizes[i]:
                    sizes[i]=key[i]
        for i in range(num_iterations):
            for ca in self.FDM_CA_list:
                message = ca.apply(message,sizes)
        return message

    #encrypt a message using the public key, the composed CA.
    def encrypt_with_composed_CA(self,message,num_iterations):
        sizes = [0]*self.dimension
        for key in list(message.keys()):
            for i in range(0,self.dimension):
                if key[i]>sizes[i]:
                    sizes[i]=key[i]
        for i in range(num_iterations):
            tmp={}
            for key in list(message.keys()):
                nbhood = []
                for nb in self.neighbourhood:
                    nbhood.append(message[vector_add(key,nb,sizes)])
                tmp[key] = self.composed_CA[tuple(nbhood)][message[key]]
            message = tmp
        return tmp

    #decrypts ciphertext by applying the inverse of each rule in reverse order
    def decrypt(self,message,num_iterations):
        sizes = [0]*self.dimension
        for key in list(message.keys()):
            for i in range(0,self.dimension):
                if key[i]>sizes[i]:
                    sizes[i]=key[i]
        for i in range(num_iterations):
            for ca in reversed(self.FDM_CA_list):
                message = ca.apply_inverse(message,sizes)
        return message

    def compose_CA(self):
        for neighbourhood in self.all_possible_neighbourhoods:
            actors=[]
            #find out which rules will act on this neighbourhood
            for c in range(0,len(self.FDM_CA_list)):
                if neighbourhood in self.FDM_CA_list[c].acting_set:
                    actors.append(True)
                else:
                    actors.append(False)

            #simulate each rule acting on the neighbourhood in succession,
            #and record the result in the composed rule.
            for s in self.state_set:
                state = s
                for ca in range(0,len(self.FDM_CA_list)):
                    if actors[ca]:
                        state = self.FDM_CA_list[ca].transition_rules[state]
                self.composed_CA[neighbourhood][s] = state


#helps the user to create a 2D message with a specified number of rows and
#columns and the desired text, with random states filling up the rest
#of the message
def create_2D_message(text,state_set,rowsize,colsize):
    msg = {}
    for i in range(0,rowsize):
        for j in range(0,colsize):
            if len(text)==0:
                msg[(i,j)] = random.choice(state_set)
            else:
                state = text[0]
                text.remove(state)
                msg[(i,j)] = state
    return msg

def create_string_message(msg, rowsize, colsize):
    message = []
    for i in range(0,rowsize):
        for j in range(0,colsize):
            message.append(msg[(i,j)])
    return ''.join(message)
    
#prints a 2D message to the screen
def print_2D_message(message):
    rowsize,colsize=0,0
    for key in list(message.keys()):
        i=key[0]
        j=key[1]
        if i>rowsize:
            rowsize=i
        if j>colsize:
            colsize=j
    for i in range(0,rowsize+1):
        for j in range(0,colsize+1):
            print(message[(i,j)], end=' ')
        print("\n")

def write_2D_message(message,filename):
    print("Writing message to "+filename+"... ", end=' ')
    rowsize,colsize=0,0
    for key in list(message.keys()):
        i=key[0]
        j=key[1]
        if i>rowsize:
            rowsize=i
        if j>colsize:
            colsize=j
    colsize+=1
    rowsize+=1
    xml = minidom.Document()
    msg = xml.createElement("message")
    msg.setAttribute("rows", str(rowsize))
    msg.setAttribute("cols", str(colsize))

    for i in range(rowsize):
        tmp=""
        for j in range(colsize):
            tmp = tmp + message[(i,j)]
        row = xml.createElement("row")
        row.setAttribute("number",str(i))
        row.setAttribute("value",tmp)
        msg.appendChild(row)

    xml.appendChild(msg)
    f = open(filename,"w")
    f.write(xml.toprettyxml())
    f.close()
    print("Done.")

def write_2D_ciphertext(ciphertext,filename,num_generations):
    print("Writing ciphertext to "+filename+"... ", end=' ')
    rowsize,colsize=0,0
    for key in list(ciphertext.keys()):
        i=key[0]
        j=key[1]
        if i>rowsize:
            rowsize=i
        if j>colsize:
            colsize=j
    colsize+=1
    rowsize+=1
    xml = minidom.Document()
    ctext = xml.createElement("ciphertext")
    ctext.setAttribute("rows", str(rowsize))
    ctext.setAttribute("cols", str(colsize))
    ctext.setAttribute("num_generations",str(num_generations))

    for i in range(rowsize):
        tmp=""
        for j in range(colsize):
            tmp = tmp + ciphertext[(i,j)]
        row = xml.createElement("row")
        row.setAttribute("number",str(i))
        row.setAttribute("value",tmp)
        ctext.appendChild(row)

    xml.appendChild(ctext)
    f = open(filename,"w")
    f.write(xml.toprettyxml())
    f.close()
    print("Done.")

def read_2D_message(filename):
    try:
        print("Reading message from "+filename+"... ", end=' ')
        go=True
        dom = minidom.parse(filename)
    except:
        print("Error: File either cannot be read or is malformed XML.")
        go = False
    if go:
        message = dom.firstChild
        numrows = int(message.getAttribute("rows"))
        numcols = int(message.getAttribute("cols"))
        rows = message.getElementsByTagName("row")
        msg={}
        for i in range(0,numrows):
            r = int(rows.item(i).getAttribute("number"))
            val = rows.item(i).getAttribute("value")
            for j in range(0,numcols):
                msg[(r,j)]=val[j]
        print("Done.")
        return msg,numrows,numcols

def read_2D_ciphertext(filename):
    try:
        print("Reading ciphertext from "+filename+"... ", end=' ')
        go=True
        dom = minidom.parse(filename)
    except:
        print("Error: File either cannot be read or is malformed XML.")
        go = False
    if go:
        ctext = dom.firstChild
        numrows = int(ctext.getAttribute("rows"))
        numcols = int(ctext.getAttribute("cols"))
        num_generations = int(ctext.getAttribute("num_generations"))
        rows = ctext.getElementsByTagName("row")
        ct={}
        for i in range(0,numrows):
            r = int(rows.item(i).getAttribute("number"))
            val = rows.item(i).getAttribute("value")
            for j in range(0,numcols):
                ct[(r,j)]=val[j]
        print("Done.")
        return ct,num_generations

#adds two vectors (tuples) componentwise.
def vector_add(vec1, vec2, sizes):
    sum = []
    for i in range(0,len(vec1)):
        sum.append((vec1[i]+vec2[i])%(sizes[i]+1))
    return tuple(sum)


if __name__=="__main__":

    sys = FDM_CA_Cryptosystem()

    try:
        while True:
            print("Please make a selection:")
            print("    1. Generate a random key pair")
            print("    2. Read the algorithm parameters from a file")
            print("    3. Read a public key from a file")
            print("    4. Read a private key from a file")
            print("    5. Write the algorithm parameters to a file")
            print("    6. Write a public key to a file")
            print("    7. Write a private key to a file")
            print("    8. Encrypt a 2D message")
            print("    9. Decrypt a 2D message's ciphertext")
            print("    0. Quit")
            choice = input("Please make a selection.")
            if choice=='1':
                if sys.have_parameters == False:
                    print("You do not have the algorithm parameters in memory. Please make a selection:")
                    print("    1. Input parameters manually")
                    print("    2. Input parameters from a file")

                    choice = input("Please make a selection.")
                    if choice == "1":
                        dim = int(str(input("Please enter the dimension size. Currently the visual display of non-2D messages is not supported.")))
                        ss = list(str(input("Please enter the state set in a single string, one state per character. Ex. 'abcd'.")))
                        nh = input("Please enter the neighbourhood of each cell separated by semicolons, and do not include spaces. Ex. '0,0;1,0;-1,1' refers to the cell itself, the right neighbour and the top-left neighbour.")
                        tmp_nh = str(nh).split(";")
                        nh = []
                        for nb in tmp_nh:
                            n = []
                            for num in nb.split(","):
                                n.append(int(num))
                            nh.append(tuple(n))
                        nCA = int(str(input("Please enter the number of FDM CA you would like in the composition.")))
                        prob1 = float(str(input("Please enter the probability p (chance to add an element to the 'change set'). Ex. '0.5'.")))
                        prob2 = float(str(input("Please enter the probability q (chance to add a neighbourhood containing no elements of the change set to the acting set). Ex. '0.5'.")))
                        sys.generate_keys(dim,ss,nh,nCA,prob1,prob2)
                        sys.have_parameters = True
                    elif choice=="2":
                        fn = str(input("Please enter the name of the file."))
                        #read parameters from a file
                        sys.read_parameters(fn)
                        sys.generate_keys(sys.dimension,sys.state_set,sys.neighbourhood,sys.num_CA,sys.p,sys.q)
                else:
                    sys.generate_keys(sys.dimension,sys.state_set,sys.neighbourhood,sys.num_CA,sys.p,sys.q)
            elif choice == '2':
                filename = input("Please enter the filename.")
                sys.read_parameters(filename)
            elif choice=='3':
                filename = input("Please enter the filename.")
                sys.read_key(filename,"public")
            elif choice=='4':
                filename = input("Please enter the filename.")
                sys.read_key(filename,"private")
            elif choice=='5':
                if sys.have_parameters:
                    filename = input("Please enter the filename.")
                    sys.write_parameters(filename)
                else:
                    print("Error: No parameters are loaded into memory.")
            elif choice=='6':
                if sys.read_public==False and sys.generated==False:
                    print("Generate or read a public key before trying to write.")
                else:
                    filename = input("Please enter the filename.")
                    sys.write_key(filename,"public")
            elif choice=='7':
                if sys.read_private==False and sys.generated==False:
                    print("Generate or read a private key before trying to write.")
                else:
                    filename = input("Please enter the filename.")
                    sys.write_key(filename,"private")
            elif choice=='8':
                if sys.generated or sys.read_public:
                    while True:
                        print("Please make a selection:")
                        print("    1. Manually input a message")
                        print("    2. Read a message from a file")
                        choice = input("Please make a selection.")
                        if choice == '1':
                            sys.rows = int(str(input("Please enter the number of rows in your message.")))
                            sys.cols = int(str(input("Please enter the number of columns in your message.")))
                            message = str(input("Please enter the message you want to encrypt. Remember to only use members of the state set in your message. If your message is smaller than the specified size, the rest of the configuration will be set randomly."))
                            msg = create_2D_message(list(message),sys.state_set,sys.rows,sys.cols)
                        elif choice == '2':
                            fn = input("Please enter the name of the file containing the message.")
                            msg,rows,cols = read_2D_message(fn)
                        if choice =='1' or choice=='2':
                            sys.num_generations = int(str(input("Please enter the number of generations to evolve the CA.")))
                            print("Original Message:")
                            print_2D_message(msg)
                            print("Encrypted with Composed CA:")
                            encrypted_with_composed_CA = sys.encrypt_with_composed_CA(msg,sys.num_generations)
                            print_2D_message(encrypted_with_composed_CA)
                            choice = input("Would you like to write the ciphertext to a file? (y/n)")
                            if choice=='y' or choice=='Y':
                                fn = input("Please enter the name of the file.")
                                write_2D_ciphertext(encrypted_with_composed_CA,fn,sys.num_generations)
                            choice = input("Would you like to write the original message to a file? (y/n)")
                            if choice=='y' or choice=='Y':
                                fn = input("Please enter the name of the file.")
                                write_2D_message(msg,fn)
                            break
                        else:
                                print("Invalid selection. Please try again.")
                    else:
                        print("Error: Can't encrypt, no public key in memory.")
            elif choice=='9':
                if sys.generated or sys.read_private:
                    fn = input("Please enter the name of the file containing the ciphertext.")
                    ctext,gens = read_2D_ciphertext(fn)
                    print("Decrypted Message:")
                    decrypted = sys.decrypt(ctext,gens)
                    print_2D_message(decrypted)
                    choice = input("Would you like to write the decrypted message to a file? (y/n)")
                    if choice=='y' or choice=='Y':
                        fn = input("Please enter the name of the file.")
                        write_2D_message(decrypted,fn)
                else:
                    print("Error: Can't decrypt, no private key in memory.")
            elif choice=='0':
                break
            else:
                print("Invalid input. Please try again.")
    except:
        print('Error: Invalid input.')


