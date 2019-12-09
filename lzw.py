import sys
from struct import *

class LZW:
    def __init__(self, max_table_size,  dict_size = 256):
        self.dict_size = dict_size
        self.max_table_size = pow(2, max_table_size)
        self.dictionary = {chr(i): i for i in range(dict_size)}
        self.compressed_data = []
        self.decompressed_data = []

    def compress(self, filename):
        f = open(filename, "r")
        data = f.read()
        f.close()
        recent_chain = ""
        compressed_data = []
        for symbol in data:
            recent_chain_with_next_symbol = recent_chain + symbol
            if recent_chain_with_next_symbol in self.dictionary:
                recent_chain = recent_chain_with_next_symbol
            else:
                compressed_data.append(self.dictionary[recent_chain])
                if len(self.dictionary) <= self.max_table_size:
                    self.dictionary[recent_chain_with_next_symbol] = self.dict_size
                    self.dict_size += 1
                recent_chain = symbol
        if recent_chain in self.dictionary:
            compressed_data.append(self.dictionary[recent_chain])

        self.compressed_data = compressed_data
        output_file = open(filename.split('.')[0] + '.lzw', "wb")
        for data in self.compressed_data:
            output_file.write(pack('>H', int(data)))
        output_file.close()

    def decompress(self, filename):
        compressed_data = []
        next_code = 256
        decompressed_data = ""
        f = open(filename, 'rb')
        recent_chain = ""

        while True:
            rec = f.read(2)
            if len(rec) != 2:
                break
            (data, ) = unpack('>H', rec)
            compressed_data.append(data)

        dec_dict_size = 256
        dec_dictionary = {i: chr(i) for i in range(dec_dict_size)}

        for code in compressed_data:
            if not (code in dec_dictionary):
                dec_dictionary[code] = recent_chain + recent_chain[0]
            decompressed_data += dec_dictionary[code]
            if not(len(recent_chain)) == 0:
                dec_dictionary[next_code] =recent_chain + (dec_dictionary[code][0])
                next_code += 1
            recent_chain = dec_dictionary[code]

        out = filename.split('.')[0] + "_decompressed.txt"
        output_file = open(out, 'w')
        for data in decompressed_data:
            output_file.write(data)
        output_file.close()

