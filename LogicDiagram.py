import json

from enum import Enum
from BasicGates import NOTGate, ANDGate, ORGate, NANDGate, NORGate, MAJGate, BUFFERGate
    
def readCircuitJSON(filename):

    class WireInfo:
        ''' Contains informations for each wire
            var origin expects a tuple containing gatename and output bit 
            var destiny expects a tuple containing gatename and input bit ''' 
        
        def __init__(self):
        
            # From gate
            self._origin = None
            # To gates
            self._destiny = []
        
        # Wire has origin
        def hasOrigin(self):
            return True if (self.origin != None) else False
            
        # Wire has destiny
        def hasDestiny(self):
            return True if (self.destiny) else False
        
        # Wire has origin and destiny
        def fullyConnected(self):
            return True if (self.origin != None and self.destiny) else False
            
        @property
        def origin(self):
            return self._origin
        
        @origin.setter
        def origin(self, gateinfo):
            self._origin = gateinfo
            
        @property
        def destiny(self):
            return self._destiny
        
        @destiny.setter
        def destiny(self, gateinfo):
            self._destiny.append(gateinfo)

    file = None
    with open(filename, 'r') as f:
        file = json.load(f)
    
    # File exist
    assert file != None, "[ERROR] FILE DOES NOT EXIST"
    
    # Check keys
    assert 'inputs' in file, "[ERROR] NO INPUTS"
    assert 'outputs' in file, "[ERROR] NO OUTPUTS"
    assert 'gates' in file, "[ERROR] NO GATES"

    circuitid = filename.split('.json')[0]
    
    # Load circuit object
    circuit = LogicDiagram(circuitid, len(file['inputs']), len(file['outputs']))
    
    # Configure input/output names
    inputnames = file['inputs']
    outputnames = file['outputs']
    circuit.createInputs(inputnames)
    circuit.createOutputs(outputnames)
    
    # Inputs/Outputs connections
    inputcon = {inputname:WireInfo() for inputname in inputnames}
    outputcon = {outputname:WireInfo() for outputname in outputnames}

    # Loads gates information
    wires = {}
    gatenames = []
    for gatename, gateinfo in file['gates'].items():
    
        # Check gate name
        assert gatename not in gatenames, "[ERROR] TWO OR MORE INSTANCES OF " + gatename
        gatenames.append(gatename)
        
        # Check keys
        assert 'inputs' in gateinfo, "[ERROR] NO INPUTS FOR " + gatename
        assert 'outputs' in gateinfo, "[ERROR] NO OUTPUTS FOR " + gatename
        assert 'type' in gateinfo, "[ERROR] NO TYPE FOR " + gatename
        
        # Check inputs
        inputsinfo = gateinfo['inputs']
        for i in range(0, len(inputsinfo)):
        
            input = inputsinfo[i]
        
            # A output can not be a input
            assert input not in outputnames, "[ERROR] OUTPUT CAN NOT BE A INPUT (" + gatename + ")"
            
            # Checks if it's a circuit input
            if input in inputnames:
                # Appends information of wich gate and wich input bit it's connected
                inputcon[input].destiny = (gatename, i)
            
            # Checks if this wire was already added to wires dict
            elif input in wires:
                # Adds destiny
                wires[input].destiny = (gatename, i)
            
            # New wire
            else:
                # Adds to dict a new wire structure
                wires[input] = WireInfo()
                # Adds destiny
                wires[input].destiny = (gatename, i)
                
        # Check outputs
        outputsinfo = gateinfo['outputs']
        for i in range(0, len(outputsinfo)):
        
            output = outputsinfo[i]
        
            # A output can not be a input
            assert output not in inputnames, "[ERROR] INPUT CAN NOT BE A OUTPUT (" + gatename + ")"
            
            # Checks if it's a circuit output
            if output in outputnames:
                outputcon[output].origin = (gatename, i)
            
            # Checks if this wire was already added to wires dict
            elif output in wires:
            
                # Checks if there is no conflict of multiple origins
                assert not wires[output].hasOrigin(), "[ERROR] MULTIPLE ORIGINS (" + output + ")"
            
                # Adds output
                wires[output].origin = (gatename, i)
            
            # New wire
            else:
            
                # Adds to dict a new wire structure
                wires[output] = WireInfo()
                # Adds origin
                wires[output].origin = (gatename, i)
                
        # After everythin is loaded, we create our gate
        circuit.addGate(gatename, gateinfo['type'], len(gateinfo['inputs']), len(gateinfo['outputs']))
    
    # Connect inputs
    for inputname, inputc in inputcon.items():
        for destiny in inputc.destiny:
            circuit.connectInput(inputname, destiny[0], destiny[1])
    
    # Connect outputs
    for outputname, outputc in outputcon.items():
        circuit.connectOutput(outputname, outputc.origin[0], outputc.origin[1])
    
    # Connect wires
    for wirename, wireinfo in wires.items():
    
        assert wireinfo.fullyConnected(), "[ERROR] WIRE NOT FULLY CONNECTED (" + wirename + ")"
        
        # Info from origin
        originname = wireinfo.origin[0]
        originbit = wireinfo.origin[1]
        
        for destiny in wireinfo.destiny:
            circuit.connectGates(originname, originbit, destiny[0], destiny[1])
    
    return circuit
        
    
class LogicDiagram:

    # Exposes number of class instantiations
    diagramids = 0

    # Class constructor
    def __init__(self, circuitname, nbitsInput, nbitsOutput):
    
        # Number of bits in input and output
        self.nbitsInput = nbitsInput
        self.nbitsOutput = nbitsOutput
        
        # Get circuit name
        self.circuitid = LogicDiagram.diagramids
        LogicDiagram.diagramids += 1
        self.circuitname = circuitname
        
        # Creates inputs and outputs
        self.ports = [BUFFERGate(self.circuitid, '___@*&Inputs@@@@', nbitsInput)]
        self.ports.append(BUFFERGate(self.circuitid, '___@*&Outputs@@@@', nbitsOutput))
        
        # Reserves space for input/output names
        self.inputNames = ['' for _ in range(nbitsInput)]
        self.outputNames = ['' for _ in range(nbitsOutput)]
        
    def createInputs(self, inputNames):
        ''' Gives a name for each input '''
        
        assert len(inputNames) == self.nbitsInput, "[ERROR] INVALID SIZE FOR INPUT NAMES"
        
        for i in range(0, self.nbitsInput):
            assert inputNames[i] not in self.outputNames, "[ERROR] CAN NOT HAVE INPUTS WITH SAME NAME AS OUTPUTS"
    
        for i in range(0, self.nbitsInput):
            self.inputNames[i] = inputNames[i]
        
    def createOutputs(self, outputNames):
        ''' Gives a name for each output '''
        
        assert len(outputNames) == self.nbitsOutput, "[ERROR] INVALID SIZE FOR OUTPUT NAMES"
        
        for i in range(0, self.nbitsOutput):
            assert outputNames[i] not in self.inputNames, "[ERROR] CAN NOT HAVE INPUTS WITH SAME NAME AS OUTPUTS"
            
        for i in range(0, self.nbitsOutput):
            self.outputNames[i] = outputNames[i]
        
    def addGate(self, gateName, gate, nbitsInput, nbitsOutput, **kwargs):
        ''' Adds a gate to diagram '''
        
        # Checks gate type and add it
        if gate == 'buffer':
            self.ports.append(BUFFERGate(self.circuitid, gateName, nbitsInput))
        elif gate == 'not':
            self.ports.append(NOTGate(self.circuitid, gateName, nbitsInput))
        elif gate == 'and':
            self.ports.append(ANDGate(self.circuitid, gateName, nbitsInput))
        elif gate == 'or':
            self.ports.append(ORGate(self.circuitid, gateName, nbitsInput))
        elif gate == 'nand':
            self.ports.append(NANDGate(self.circuitid, gateName, nbitsInput))
        elif gate == 'nor':
            self.ports.append(NORGate(self.circuitid, gateName, nbitsInput))
        elif gate == 'majority':
            self.ports.append(MAJGate(self.circuitid, gateName, nbitsInput))
        elif gate == 'generic':
            inputs = kwargs.get('inputs')
            outputs = kwargs.get('outputs')
            
            assert inputs != None, "[ERROR] NO GIVEN INPUTS TO GENERIC (" + gatename + ")"
            assert outputs != None, "[ERROR] NO GIVEN OUTPUTS TO GENERIC (" + gatename + ")"
            
            self.ports.append(GENERICGate(self.circuitid, gateName, nbitsInput, nbitsOutput, logic_inputs, logic_outputs))
            
        else:
            assert False, "[ERROR] INVALID GATE TYPE"
        
    def connectInput(self, inputName, gateName, gateInputBit):
        ''' Connect an input to a gate '''
        
        found = False
    
        # Searchs inputName
        for i in range(0, self.nbitsInput):
            if inputName == self.inputNames[i]:
                found = True
                break
        # Input not found
        assert found, "[ERROR] INPUT NAME NOT FOUND"
        
        found = False
    
        for p in self.ports:
            if p.name == gateName:
                found = True
                break
        
        # Gate not found
        assert found, "[ERROR] GATE NAME " + gateName + " NOT FOUND"
        # Invalid gateInputBit
        assert gateInputBit >= 0 and gateInputBit < p.getInputNum(),\
        "[ERROR] BIT " + str(gateInputBit) + " ON " + gatename + " WAS NOTE FOUND"
        
        self.ports[0].connectOutput(self.circuitid, i, gateInputBit, gateName)
        
    def connectOutput(self, outputName, gateName, gateOutputBit):
        ''' Connect a gate to output '''
        
        found = False
    
        # Searchs OutputName
        for i in range(0, self.nbitsOutput):
            if outputName == self.outputNames[i]:
                found = True
                break
                
        # Input not found
        assert found, "[ERROR] OUTPUT NAME " + outputName + " NOT FOUND"
    
        found = False
    
        for p in self.ports:
            if p.name == gateName:
                found = True
                break
        
        # Gate not found
        assert found, "[ERROR] GATE NAME " + gateName + " NOT FOUND"
        # Invalid gateInputBit
        assert not (gateOutputBit < 0 or gateOutputBit >= p.getOutputNum()), \
        "[ERROR] OUTPUT BIT " + str(gateOutputBit) +  " ON " + gateName + " WAS NOT FOUND" 
        
        p.connectOutput(self.circuitid, i, gateOutputBit, '___@*&Outputs@@@@')
        
    def connectGates(self, gate1_Name, gate1_Output, gate2_Name, gate2_Input):
        ''' Connects a gate to another '''
        
        found = False
    
        # Searchs gate 1
        for i in range(0, len(self.ports)):
            if gate1_Name == self.ports[i].name:
                found = True
                break
                
        # Gate 1 not found
        assert found, "[ERROR] GATE NAME " + gate1_Name + " NOT FOUND"
        
        found = False

        # Searchs gate 2
        for j in range(0, len(self.ports)):
            if gate2_Name == self.ports[j].name:
                found = True
                break
                
        # Gate 2 not found
        assert found, "[ERROR] GATE NAME " + gate2_Name + " NOT FOUND"
        
        # Invalid gateOutputBit
        assert not (gate1_Output < 0 or gate1_Output >= self.ports[j].getOutputNum()), \
        "[ERROR] OUTPUT BIT " + str(gate1_Output) +  " ON " + gate1_Name + " WAS NOT FOUND" 
        assert not (gate2_Input < 0 or gate2_Input >= self.ports[j].getInputNum()), \
        "[ERROR] INPUT BIT " + str(gate2_Output) +  " ON " + gate2_Name + " WAS NOT FOUND" 
        
        self.ports[i].connectOutput(self.circuitid, gate1_Output, gate2_Input, gate2_Name)
    
    def showDiagram(self):
        pass
        
    def showOutput(self, input):
        print('%0*d | %0*d' % (self.nbitsInput, int(bin(input)[2:]), self.nbitsOutput, int(bin(self.ports[1].outputSignal)[2:])))

    def getInputNumber(self):
        return self.nbitsInput

    def getOutput(self, input):
        return '%0*d' % (self.nbitsOutput, int(bin(self.ports[1].outputSignal)[2:]))
        
    def applyInputVec(self, input):
        ''' Applies an input given by a vector containing value from each bit '''
    
        inp = 0
        
        for i in range(0, self.nbitsInput):
            inp += input[i] >> i

        # Apply input
        self.ports[0].applyInput(self.circuitid, inp)

        # Updates everything
        for i in range(0, len(self.ports)):
            self.ports[i].update(self.circuitid)
        
    def applyInput(self, input):
        ''' Applies an input '''
        
        # Apply input
        self.ports[0].applyInput(self.circuitid, input)
        
        # Updates everything
        for i in range(0, len(self.ports)):
            self.ports[i].update()
        
    def resetInputs(self):
        ''' Resets all inputs information '''
    
        for p in self.ports:
            p.resetInputs()
        
    def calculateEnergy(self):
        ''' Calculates total energy on circuit '''
    
        energy = 0.0
        
        for p in self.ports:
            energy += p.calculateEnergy()
        
        return energy
        
if __name__ == "__main__":
    pass