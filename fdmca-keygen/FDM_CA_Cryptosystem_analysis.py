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
        for key in message.keys():
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
        for key in message.keys():
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
            print "Writing public key to "+filename+"...",
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

            print "Done."
        elif key_type=="private":
            print "Writing private key to "+filename+"...",
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
            print "Done."
        else:
            print "Invalid key type. Please enter 'public' or 'private'."

    def write_parameters(self,filename):
        print "Writing parameters to "+filename+"...",
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
        print "Done."

    #method to read the algorithm parameters from a file
    def read_parameters(self, filename):
        try:
            print "Reading parameters from "+filename+"... ",
            go=True
            dom = minidom.parse(filename)
        except:
            print "Error: File either cannot be read or is malformed XML."
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
            print "Done."

    #method to read a public or private key from an xml file
    def read_key(self,filename,key_type):
        if key_type=="public":
            print "Reading public key from "+filename+"...",
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
            print "Done. Public key is now in memory."
        elif key_type=="private":
            print "Reading private key from "+filename+"...",
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
            print "Done. Private key is now in memory."
        else:
            print "Invalid key type. Please enter 'public' or 'private'."

    def generate_keys(self,dimension,state_set,neighbourhood,num_CA,p,q):
        self.dimension = dimension
        self.state_set = state_set[:]
        self.neighbourhood = neighbourhood
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

        print "Generating the random FDM CA list...",
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
            positions = self.random_binary(len(self.neighbourhood))
            for nbhd in self.all_possible_neighbourhoods:
                unchanging_neighbourhood = True
                rg = range(len(self.neighbourhood))
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

        print "Composing into one CA...",
        self.compose_CA()
        self.generated = True
        print "Done. The public and private keys are now in memory."

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
        total = len(self.state_set)**len(self.neighbourhood)
        for i in range(0,total):
            temp = []
            num=i
            for j in range(len(self.neighbourhood)):
                temp.append(self.state_set[num/((len(self.state_set))**(len(self.neighbourhood)-j-1))])
                num-=(num/((len(self.state_set))**(len(self.neighbourhood)-j-1)))*((len(self.state_set))**(len(self.neighbourhood)-j-1))
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
        for key in message.keys():
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
        for key in message.keys():
            for i in range(0,self.dimension):
                if key[i]>sizes[i]:
                    sizes[i]=key[i]
        for i in range(num_iterations):
            tmp={}
            for key in message.keys():
                nbhood = []
                for nb in self.neighbourhood:
                    nbhood.append(message[vector_add(key,nb,sizes)])
                tmp[key] = self.composed_CA[tuple(nbhood)][message[key]]
            message = tmp
        return tmp

    #decrypts ciphertext by applying the inverse of each rule in reverse order
    def decrypt(self,message,num_iterations):
        sizes = [0]*self.dimension
        for key in message.keys():
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




if __name__=="__main__":

    sys = FDM_CA_Cryptosystem()

    filename = raw_input("Please enter the filename of the public key you want to analyze.")
    sys.read_key(filename,'public')

    freqArray = {}
    for state in sys.state_set:
        for state2 in sys.state_set:
            freqArray[(state,state2)]=0
    sys.all_possible_neighbourhoods=sys.generate_all_possible_neighbourhoods()
    for nbhd in sys.all_possible_neighbourhoods:
        for state in sys.state_set:
            freqArray[(state,sys.composed_CA[nbhd][state])]+=1

    #for state in sys.state_set:
    #    for state2 in sys.state_set:
    #        print state+","+state2+","+str(freqArray[(state,state2)])
    maxArray = {}
    for state in sys.state_set:
        maxval = 0
        for state2 in sys.state_set:
            if freqArray[(state,state2)]>maxval:
                maxval = freqArray[(state,state2)]
                maxArray[state] = 100.0*maxval/(len(sys.state_set)**len(sys.neighbourhood))

    items = [(v, k) for k, v in maxArray.items()]
    items.sort()
    items.reverse()             # so largest is first
    items = [(k, v) for v, k in items]
    for item in items:
        k,v = item
        print v



