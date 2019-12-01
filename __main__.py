from LogicDiagram import LogicDiagram, readCircuitJSON
import os
import sys

'''assert len(sys.argv) > 1, "[ERROR] NO ARGUMENTS"
assert len(sys.argv) > 2, "[ERROR] NO BINARY INPUTS"

# Reads JSON
circuit = readCircuitJSON(os.path.join(sys.path[0], sys.argv[1]))

for arg in sys.argv[2:]:

	binaryInput = 0
	power = 1 << len(arg)-1
	
	for i in range(0, len(arg)):
		binaryInput += power*int(arg[i])
		power = power >> 1
		
	circuit.applyInput(binaryInput)
	
print(circuit.calculateEnergy())'''

# TESTES SEM ARGUMENTOS!
circuit = readCircuitJSON(os.path.join(sys.path[0], 'circuit2.json'))

a = ['0000', '0001', '0010', '0011', '0100', '0101', '0110', '0111', '1000', '1001', '1010', '1011', '1100', '1101', '1110', '1111']

for arg in a:

	binaryInput = 0
	power = 1 << len(arg)-1
	
	for i in range(0, len(arg)):
		binaryInput += power*int(arg[i])
		power = power >> 1
		
	circuit.applyInput(binaryInput)
	
print(circuit.calculateEnergy())

circuit2 = readCircuitJSON(os.path.join(sys.path[0], 'circuit3.json'))

a = ['0000', '0001', '0010', '0011', '0100', '0101', '0110', '0111', '1000', '1001', '1010', '1011', '1100', '1101', '1110', '1111']

for arg in a:

	binaryInput = 0
	power = 1 << len(arg)-1
	
	for i in range(0, len(arg)):
		binaryInput += power*int(arg[i])
		power = power >> 1
		
	circuit2.applyInput(binaryInput)
	
print(circuit2.calculateEnergy())