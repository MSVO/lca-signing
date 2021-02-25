*************************Readme File for the FDM CA Cryptosystem Simulator*************************

Changelog:
- Created 2008-12-05 by Adam Clarridge (adam AT cs d0t queensu d0t ca).
- NOTE: 2010-02-28 by Adam Clarridge - My permanent email is now adam d0t clarridge AT gmail D0T com

Contents:
	1. What is it?
	2. Basic Usage
		i.   Running the Python script
		ii.  Generating public and private keys and encrypting/decrypting messages
		iii. Reading/Writing keys, algorithm parameters, messages, and ciphertexts from/to files
		iv.  Detailed example
		v.   Less detailed example
	3. Troubleshooting
	4. References
	
	
1. What is it?

	This simulator is meant to be a proof-of-concept of the encryption algorithm presented in the 
	paper by Adam Clarridge and Kai Salomaa entitled 'A Cryptosystem based on the Composition of 
	Reversible Cellular Automata', submitted to LATA 2009.
	'Proof-of-concept' is important here: the simulator should function as advertised, but this tool
	is not meant to be used as a practical means of encryption. The simulator is somewhat slow and 
	has a fairly simple, naive implementation - an optimized parallel implementation would certainly
	be desireable and would increase the speed of encryption and decryption by a large amount.
	It is important to note that the security of the algorithm implemented here is currently unknown.

2. Basic Usage

	i.   Running the Python script
		One can find all the resources necessary for downloading the Python interpreter at
		www.python.org. Once Python is set up, in most operating systems the command 
		'python myProgram.py' would run myProgram.py. The FDM CA Cryptosystem simulator only
		uses standard Python libraries, and should work fine with Python 2.5 or later.
		
	ii.  Generating public and private keys and encrypting/decrypting messages
		To generate keys, select the first menu option (press 1, then Enter), followed by the
		first menu option again to input the parameters manually. The key generation algorithm
		requires several parameters in order to generate the public and private key; simply
		follow the prompts and be sure to provide valid input. Afterwards, the simulator
		will store the public and private keys in memory - you are now free to store these
		keys in files, or use them to encrypt/decrypt.
		You may also save algorithm parameters in a file.
		
	iii. Reading/Writing keys, algorithm parameters, messages, and ciphertexts from/to files
		One may read or write public or private keys, algorithm parameters, messages and
		ciphertexts using the menu commands. The storage format is XML and each of the
		aforementioned objects has its own XML structure (when reading a private key, do not
		point the simulator to a file containing a public key). The format of each XML file
		is not memory efficient; instead it is meant to be understandable to somebody who
		wishes to look at the XML code.
		When referencing files, simply type 'myFile.xml' - this will work as long as the
		simulator is run from the same directory as myFile.xml.
		
	iv.  Detailed example
		Here is an example of the user input required to generate keys, then encrypt,
		save, and decrypt a message. Menu related output is omitted.
		
		INPUT: '1' <ENTER>							 (generate a public and private key)
		INPUT: '1' <ENTER>                           (manual parameter input)
		INPUT: '2' <ENTER>                           (dimension size)
		INPUT: 'abcdefghijklmnopqrstuvwxyz ' <ENTER> (the state set, one state per char)
		INPUT: '1,0;0,1' <ENTER>                     (top & right neighbours (2 dimensional))
		INPUT: '200' <ENTER>                         (number of FDM CA in the composition)
		INPUT: '0.2' <ENTER>                         (p=0.2 since (1/0.2)*27 < 200 (see paper))
		INPUT: '0.5' <ENTER>                         (q=0.5, see paper)
		
		OUTPUT: Generating the FDM CA list... Composing into one CA... Done. The public and
				private keys are now in memory.
				
				(At this point we can now use the public and private keys to encrypt/decrypt)
		
		INPUT: '8' <ENTER>                           (Encrypt a 2D message)
		INPUT: '1' <ENTER>                           (Manually input a message)
		INPUT: '3' <ENTER>                           (the number of rows in the message)
		INPUT: '20' <ENTER>                          (the number of columns in the message)
		INPUT: 'the quick brown fox jumps
				over the lazy dog' <ENTER>           (the message)
		INPUT: '200' <ENTER>                         (number of generations to evolve the CA)
		
		OUTPUT: Original Message:
				t h e   q u i c k   b r o w n   f o x   

				j u m p s   o v e r   t h e   l a z y   

				d o g s r o h n l q c m q x s u w t n z 

				Encrypted with Composed CA:
				o q z z v y g u y d m g x l d e a t c l 

				  c n r d m u n w v m g n w g b z j h t 

				a r i t p o d c q u c q i o   r u l z j 
				
				(note that the message input wasn't long enough to fill the entire message
				area, so the simulator fills the extra space with random states)
						
		INPUT: 'y'                                   (save the ciphertext so we can decrypt)
		INPUT: 'n'                                   (we do not need to save the message)
		INPUT: 'ciphertext.xml'                      (the name of the file to save it as)
		
		OUTPUT: Writing ciphertext to ciphertext.xml...  Done.
		
		INPUT: '9'                                   (decrypt a 2D message's ciphertext)
		INPUT: 'ciphertext.xml'                      (the name of the file)
		
		OUTPUT: Reading ciphertext from ciphertext.xml...  Done.
				Decrypted Message:
				t h e   q u i c k   b r o w n   f o x   

				j u m p s   o v e r   t h e   l a z y   

				d o g s r o h n l q c m q x s u w t n z 
		
		INPUT: 'y'                                   (save the decrypted message)
		INPUT: 'decrypted.xml'                       (save to decrypted.xml)
		
		OUTPUT: Writing message to decrypted.xml...  Done.
		
		INPUT: '0'                                   (Quit the simulator)
		
	v.   Less detailed example
		
		Here is an example of how to use this simulator as a real public key encryption system
		(note that this is not recommended for sensitive data because the security of the
		algorithm is still unknown).
		
		- Generate a public and private key.
		- Save them as public.xml and private.xml, respectively.
		- Close the simulator, and send public.xml to your friends.
		- Your friends can open the simulator, Read the public key, then manually input a
			message, encrypt it, and save the ciphertext to a file.
			Then they can send the ciphertext to you.
		- Run the simulator and read your private key (private.xml). Decrypt your friends'
			messages one at a time.

3. Troubleshooting

	Unfortunately not many of the error messages are very descriptive in this simulator, since
	once again, it is only meant to be a proof of concept. Most problems that occur are due to
	incorrect input/typos. If an error occurs, retry the operation again, making sure that all
	your input is valid, the simulator is being run from the same directory as the files you
	are reading/writing, and that you are reading/writing the right file format.

	As soon as the program quits or ends because of an error, all information (keys or
	algorithm parameters) that were	stored in memory are lost. Therefore, it is good practice
	to store keys and parameters to files after they are generated/inputted, so that if
	something goes wrong you have a backup.

	Any bugs/suggestions/comments can be reported to:
	adam AT cs d0t queensu d0t ca
	
4. References

	Python: www.python.org
	Public key encryption: http://en.wikipedia.org/wiki/Public-key_cryptography