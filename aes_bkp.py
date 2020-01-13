import aes2
import os,struct
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto import Random
import random

iv = Random.new().read(AES.block_size)

dir_name = input("Enter the directoy name : ")
list_file = None
choice = None
password = None
sz = 2048


def encrypt_file(key, in_filename, out_filename=None, chunksize=64*1024):
    """ Encrypts a file using AES (CBC mode) with the
        given key.

        key:
            The encryption key - a string that must be
            either 16, 24 or 32 bytes long. Longer keys
            are more secure.

        in_filename:
            Name of the input file

        out_filename:
            If None, '<in_filename>.enc' will be used.

        chunksize:
            Sets the size of the chunk which the function
            uses to read and encrypt the file. Larger chunk
            sizes can be faster for some files and machines.
            chunksize must be divisible by 16.
    """
    if not out_filename:
        out_filename = in_filename + '.enc'

    iv = Random.new().read(AES.block_size)
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    filesize = os.path.getsize(in_filename)

    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            outfile.write(struct.pack('<Q', filesize))
            outfile.write(iv)

            while True:
                chunk = base64.b64encode(infile.read(chunksize))
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += bytearray((16 - len(chunk) % 16) * ' ', 'utf8')

                outfile.write(encryptor.encrypt(chunk))


def decrypt_file(key, in_filename, out_filename=None, chunksize=24*1024):
    """ Decrypts a file using AES (CBC mode) with the
        given key. Parameters are similar to encrypt_file,
        with one difference: out_filename, if not supplied
        will be in_filename without its last extension
        (i.e. if in_filename is 'aaa.zip.enc' then
        out_filename will be 'aaa.zip')
    """
    if not out_filename:
        out_filename = os.path.splitext(in_filename)[0]

    with open(in_filename, 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, iv)

        with open(out_filename, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(base64.b64decode(decryptor.decrypt(chunk)))

            outfile.truncate(origsize)


if(os.path.exists(dir_name)):
	list_file = os.listdir(dir_name)

print("\nThe list of files : ")
for l in list_file:
	#print(os.path.join(dir_name,l))
	print(l)

choice = input("\nDo you want to encrypt all? Y/N\n")

if(choice == 'Y' or choice == 'y'):
	password = input("Enter password : ")
	aes = AES.new(password, AES.MODE_CBC, iv)
	print("Cypher generated...")
	for l in list_file:
		file_path = os.path.join(dir_name,l)
		print("Encrypting .. ",file_path)
		encrypt_file(password, file_path)
		os.system('rm '+file_path)
		print(file_path," encrypted & deleted")


choice = input("\nDo you want to decrypt all? Y/N\n")

if(choice == 'Y' or choice == 'y'):
	password = input("Enter password : ")
	aes = AES.new(password, AES.MODE_CBC, iv)
	print("Cypher generated...")
	for l in list_file:
		file_path = os.path.join(dir_name,l)
		print("Decrypting .. ",file_path,'.enc')
		decrypt_file(password, file_path+'.enc', file_path)
		#os.system('rm '+file_path)
		print(file_path," decrypted")
		

elif(choice == 'N' or choice == 'n'):
	print("You entered ",choice,"Good bye")
