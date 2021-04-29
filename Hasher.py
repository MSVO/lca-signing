import libnum
import random
import binascii
from PIL import Image
import numpy as np


## Requires iv1, iv2, prime, generated_random_index to compute the hash
class ImageHasher:
    # If only message (as bits) is provided, compute the remaining parameters.
    # These parameters have to be saved by user to recompute the hash later
    def __init__(self, image, iv1 = None, iv2 = None, prime = None, rand_ind = None):
        self.N = 256
        self.PRIME_BITLEN = 13
        self.iv1 = iv1 if iv1 else format(libnum.randint_bits(self.N),'0256b')
        self.iv2 = iv2 if iv2 else format(libnum.randint_bits(self.N),'0256b')
        self.prime = prime if prime else libnum.generate_prime(self.PRIME_BITLEN)
        self.image_as_bits = self.image_to_bits(image)
        self.rand_ind = rand_ind if rand_ind else random.randint(0,len(self.image_as_bits)//self.N)

    # Computes the hash using LCAHASH 1.1 Algorithm and return N bit string 
    def lcahash(self, msg_bits_string, iv1, iv2, prime, rand_ind):
        # Add padding if not multiple of self.N
        padded_msg = msg_bits_string
        if len(msg_bits_string)%self.N != 0:
            padded_msg = self.add_padding(msg_bits_string)

        splitted_msg = [padded_msg[i:i+self.N] for i in range(0,len(padded_msg),self.N)]
        splitted_msg[rand_ind] = self.string_xor(splitted_msg[rand_ind], iv1)
        
        combined_prime_msg = []

        for block in splitted_msg:
            combined_prime_msg.append(format((int(block,2)%prime),'b'))
        
        
        padded_prime_msg = ''.join(combined_prime_msg)
        if len(padded_prime_msg)%self.N != 0:
            padded_prime_msg = self.add_padding(padded_prime_msg)
        
        splitted_prime_msg = [padded_prime_msg[i:i+self.N] for i in range(0,len(padded_prime_msg),self.N)]

        m_evolv = iv2
        for block in splitted_prime_msg:
            m_evolv = self.string_xor(m_evolv, block)

        rule_set = [30,90]*(self.N//2)
        for i in range(self.N):
            m_evolv = self.runCA_periodic(rule_set, m_evolv)
        
        return m_evolv
    
    def digest(self):
        hval = hex(int(self.lcahash(self.image_as_bits, self.iv1, self.iv2, self.prime, self.rand_ind),2))[2:]
        return "0"*((self.N//4)-len(hval)) + hval
    


    #####
    ## Helper functions
    ####


    ## Converts image to bit string
    def image_to_bits(self, image):
        image_bit_string = ''.join([format(i,'08b') for i in (np.asarray(image).reshape((-1,)))])
        return image_bit_string

    # two strings , does xor , returns string
    def string_xor(self,a,b):
        res = []
        for a_i,b_i in zip(a,b):
            res.append('0' if a_i==b_i else '1')
        return ''.join(res)
    # Add padding to bit string
    def add_padding(self, msg_bits_string):
        num_zeroes = (self.N - len(msg_bits_string)%self.N)-1
        return (msg_bits_string + '1' + '0'*num_zeroes)

    # return string of {0,1}. Input (string , int)
    def apply_rule_to_cell(self, neigbourhood_string, rule_no):
        binary_string = '{:08b}'.format(rule_no)
        return binary_string[int(neigbourhood_string,2)]

    # returns new state as string {0,1} given state and list of rules
    def runCA_periodic(self, rules, state):
        new_state = []
        first_cell_state = state[-1] + state[0:2]
        new_state.append(self.apply_rule_to_cell(first_cell_state, rules[0]))

        for i in range(1,len(rules)-1):
            neighbour = state[i-1:i+2]
            new_state.append(self.apply_rule_to_cell(neighbour, rules[i]))
        last_cell_state = state[-2:] + state[0]
        new_state.append(self.apply_rule_to_cell(last_cell_state, rules[-1]))
        return ''.join(new_state)




# Sample
if __name__=="__main__":
    image = Image.open('veggies.jpg').convert('L')
    hasher_ = ImageHasher(image)
    print(hasher_.digest(), hasher_.iv1, hasher_.iv2, hasher_.prime, hasher_.rand_ind)

