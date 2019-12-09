from  argparse import ArgumentParser
from lzw import LZW


parser = ArgumentParser(description = "Implementacja algorytmu kompresji słownikowej \
        bezstratnej LZW, wykonana w języku Python v3.6, jako projekt na\
        Podstwy Kompresji Danych laboratoria.\nNależy skorzystać tylko i wyłącznie z jednego trybu pracy programu na raz.")
filename = ""
bits = 0
parser.add_argument('filename', metavar="FILE", type=str, help="nazwa pliku, który chcemy skompresować / zdekompresować")
parser.add_argument('bits', metavar="BITS", type=int, help="ilość bitów wykorzystywana do określenia maksymalnej pojemności słownika (nie zaleca się korzystania z liczb poniżej 8)")
parser.add_argument('-c', dest="compress", action="store_true", help="Tryb pracy - kompresja")
parser.add_argument('-d', dest="decompress", action="store_true", help="Tryb pracy - dekompresja")

args = parser.parse_args()
print(args)
if args.decompress and args.compress:
    raise ValueError("Wybrano więcej niż jeden tryb pracy")

algorithm = LZW(max_table_size=args.bits)
if args.compress:
    algorithm.compress(args.filename)
elif args.decompress:
    algorithm.decompress(args.filename)


