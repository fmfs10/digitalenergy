from LogicDiagram import LogicDiagram, readCircuitJSON
import itertools
import os
import sys

def convertArg(arg):
    binaryInput = 0
    power = 1 << len(arg)-1

    for i in range(0, len(arg)):
        binaryInput += power*int(arg[i])
        power = power >> 1

    return binaryInput

circuit1 = readCircuitJSON(os.path.join(sys.path[0], 'circuit2.json'))
circuit2 = readCircuitJSON(os.path.join(sys.path[0], 'circuit3.json'))

inputs = ["".join(i) for i in list(itertools.product('01', repeat=circuit1.getInputNumber()))]
for i in range(2, len(inputs) + 1):
    combs = itertools.combinations(inputs, i)
    for group in combs:
        outputs = []
        circuit1.resetInputs()
        circuit2.resetInputs()
        for arg in group:
            binaryArg = convertArg(arg)
            circuit1.applyInput(binaryArg)
            circuit2.applyInput(binaryArg)
            a = circuit1.getOutput(binaryArg)
            b = circuit2.getOutput(binaryArg)
            assert a == b, "For same input: {} We got two different results: {} {}".format(binaryArg, a, b)
            outputs.append(circuit1.getOutput(binaryArg))
        if (len(set(outputs)) == 1):
            print("[WARNING] Wire")
        else:
            print(circuit1.calculateEnergy())