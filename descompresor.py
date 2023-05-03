import heapq
import os
import time

class Nodo:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

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

def descomprimir(input_path, output_path):
    start_time = time.time()
    with open(input_path, 'rb') as input_file:
        # Read header
        num_chars = int.from_bytes(input_file.read(2), 'big')
        freqs = {}
        for _ in range(num_chars):
            byte = int.from_bytes(input_file.read(1), 'big')
            freq = int.from_bytes(input_file.read(4), 'big')
            freqs[byte] = freq

        padding = int.from_bytes(input_file.read(1), 'big')

        # Reconstruct Huffman tree
        arbol = construir_arbol(freqs)

        # Read compressed data
        compressed_data = input_file.read()
        bits = ''.join(bin(byte)[2:].zfill(8) for byte in compressed_data)[:-padding]

        # Decompress data
        descomprimido = bytearray()
        nodo_actual = arbol
        for bit in bits:
            if bit == '0':
                nodo_actual = nodo_actual.left
            else:
                nodo_actual = nodo_actual.right

            if nodo_actual.char is not None:
                descomprimido.append(nodo_actual.char)
                nodo_actual = arbol
        end_time = time.time()
        # Write decompressed data to output file
        with open(output_path, 'wb') as output_file:
            output_file.write(bytes(descomprimido))
        print(f'Time descompresor: {end_time - start_time}')

if __name__ == '__main__':
    input_path = "comprimido.elmejorprofesor"
    output_path = "descomprimido-elmejorprofesor.txt"
    descomprimir(input_path, output_path)
