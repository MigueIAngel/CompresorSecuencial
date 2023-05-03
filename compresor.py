import heapq
import os
from collections import defaultdict
import sys
import time

class Nodo:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def calcular_frecuencias(file_path):
    with open(file_path, 'rb') as f:
        text = f.read()
    freqs = defaultdict(int)
    for byte in text:
        freqs[byte] += 1
    return freqs

def construir_arbol(freqs):
    heap = [Nodo(byte, freq) for byte, freq in freqs.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        nodo = Nodo(None, left.freq + right.freq)
        nodo.left = left
        nodo.right = right
        heapq.heappush(heap, nodo)

    return heap[0]

def generar_codigos(nodo, codigo='', codigos={}):
    if nodo is None:
        return

    if nodo.char is not None:
        codigos[nodo.char] = codigo
        return codigos

    codigos = generar_codigos(nodo.left, codigo + '0', codigos)
    codigos = generar_codigos(nodo.right, codigo + '1', codigos)

    return codigos

def comprimir(input_path, output_path):
    start_time=time.time()
    freqs = calcular_frecuencias(input_path)
    arbol = construir_arbol(freqs)
    codigos = generar_codigos(arbol)

    with open(input_path, 'rb') as input_file, open(output_path, 'wb') as output_file:
        # Write header
        output_file.write(len(codigos).to_bytes(2, 'big'))
        for byte, freq in freqs.items():
            output_file.write(byte.to_bytes(1, 'big'))
            output_file.write(freq.to_bytes(4, 'big'))

        # Write compressed data
        text = input_file.read()
        compressed_data = ''
        for byte in text:
            compressed_data += codigos[byte]

        padding = 8 - len(compressed_data) % 8
        compressed_data += '0' * padding

        output_file.write(padding.to_bytes(1, 'big'))

        byte_array = bytearray()
        for i in range(0, len(compressed_data), 8):
            byte_array.append(int(compressed_data[i:i + 8], 2))

        output_file.write(bytes(byte_array))
    end_time=time.time()
    print(f'Time compresor: {end_time-start_time}')
if __name__ == '__main__':
    file_path = sys.argv[1]
    
    comprimir(file_path, "comprimido.elmejorprofesor")
    
    
