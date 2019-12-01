from abc import ABC, abstractmethod
from math import log2

class LogicGate(ABC):
	''' Abstract class of a generic gate '''

	# Posteriormente quero adicionar isso para performance...
	__slots__ = ('name', 'nbitsInput', 'nbitsOutput',\
	'inputsOcurrNum', 'updatedBits', 'inputSignal', 'outputSignal'\
	'input', 'outputOccurr', 'outputBits')

	# Stores existing gates on circuits
	gateList = {}
	
	# Class constructor
	def __init__(self, circuitid, name, nbitsInput, nbitsOutput = 1):
	
		# Abstract Class Constructor
		super().__init__()
		
		# If circuitid is not in our dict, adds it
		if circuitid not in LogicGate.gateList:
			LogicGate.gateList[circuitid] = {}
	
		# New gate
		self.name = name
		LogicGate.gateList[circuitid][name] = self
		
		# Number of bits in gate input and output
		self.nbitsInput = nbitsInput
		self.nbitsOutput = nbitsOutput
		
		# Total of ocurrences of inputs and outputs
		self.inputsOcurrNum = 0
		
		# None updated bits
		self.updatedBits = 0
		
		# Current signal at input and output
		self.inputSignal = 0
		self.outputSignal = 0
		
		# Creates a list with information of all possible gate entries.
		self.input = [self.Input() for _ in range(self.getInputNum())]
		
		# Creates a list with information of all output occurrences
		self.outputOccurr = [0]*(1<<self.nbitsOutput)
		
		# Creates a list of lists with information of all output signals
		self.outputBits = [[] for _ in range(self.nbitsOutput)]
		
	class Input:
		''' Structure that defines information for each input combination
		For example, entry 000 has output 1 and this input has occurred 1 time.
		Input 001 has output 0 and this input has occurred 2 times and etc... '''
	
		# The number of occurrences of the entry is initially equal to 0
		def __init__(self):
			self.ocurrences = 0
		
		# Defines the output of the given input
		def setOutput(self, output):
			self.output = output
			
		# Get output
		def getOutput(self):
			return self.output
		
		# Defines the number of occurrences
		def setOcurrence(self, ocurrences):
			self.ocurrences = ocurrences
		
		# Increase number of occurrences
		def incrementOcurrence(self):
			self.ocurrences += 1
		
		# Reset the number of occurrences
		def resetOcurrence(self):
			self.ocurrences = 0
		
		# Regates the number of occurrences
		def getOcurrence(self):
			return self.ocurrences
	
	class OutputBit:
		''' Class indicating information of each gate output bit '''
		
		# Indicates which gate the output bit is connected and which input bit
		def __init__(self, gatename, inputbit):
			self.gatename = gatename
			self.inputbit = inputbit
		
		def getInputBit(self):
			return self.inputbit
		
		def getGateName(self):
			return self.gatename
    
	def addInputOcurrence(self):
	
		# Get data from input
		inaux = self.input[self.inputSignal]
			
		# Increments ocurrence of input 
		inaux.incrementOcurrence()
		
		# Increments total ocurrence of inputs
		self.inputsOcurrNum += 1
		
		self.outputOccurr[inaux.getOutput()] += 1
			
	def showTruthTable(self):
		''' Checks all possible input elements and prints outputs as a Truth Table '''
	
		for i in range(0, len(input)):
			print('%d | %d\n' % (i, input[len].output))
			
	def calculateEnergy(self):
		''' Calculates energy of our system '''
	
		inputEntropy = 0
		outputEntropy = 0
		
		if self.inputsOcurrNum != 0:
			for i in self.input:
				if i.getOcurrence() != 0:
					inputEntropy -= log2(i.getOcurrence())*i.getOcurrence()/self.inputsOcurrNum
		
			for i in self.outputOccurr:
				if i != 0:
					outputEntropy -= log2(i)*i/self.inputsOcurrNum
			
			# As this factor is equal on both, we don't really need to add it
			# inputEntropy += log2(self.inputsOcurrNum)
			# outputEntropy += log2(self.inputsOcurrNum)
			
		return (inputEntropy-outputEntropy)
		
	def _addOutputValue(self, input, output):
		''' Adds an output value to given input '''
		self.input[input].setOutput(output)
		
	def __applyInputBit(self, circuitid, input, bit):
		''' Applies a input to a given input bit '''
		
		# Apply bit to input signal
		self.inputSignal += input << bit;
		
		# Bit is updated
		self.updatedBits += 1 << bit;
		
		# All bits were updated, so updates connected gates
		if self.updatedBits == (1 << self.nbitsInput)-1:
			
			# Sets current output signal to output of current input
			self.outputSignal = self.input[self.inputSignal].getOutput()
			
			# Updates all outputs
			self.__updateOutputs(circuitid)
			
			# New input occurence
			self.addInputOcurrence()
		
	def applyInput(self, circuitid, input):
		''' Applies a input to all input bits '''
		
		assert input >= 0 and input < self.getInputNum(), "[ERROR] INVALID INPUT (" + input + ")"
		
		# All bits are updated
		self.updatedBits = ~0

		# Sets current input signal
		self.inputSignal = input
		
		# Sets current output signal to output of current input
		self.outputSignal = self.input[input].getOutput()
		
		# Updates all outputs
		self.__updateOutputs(circuitid)
		
		# New input occurence
		self.addInputOcurrence()
	
	def __updateOutputs(self, circuitid):
		''' Updates outputs '''
		# Applies the signal to all gates connected to the output
		for i in range(0, len(self.outputBits)):
			for j in self.outputBits[i]:
				# Creates a mask to apply the correct signal
				mask = (self.outputSignal & (1 << i)) >> i
				LogicGate.gateList[circuitid][j.getGateName()].__applyInputBit(circuitid, mask, j.getInputBit())
	
	def update(self):
		''' Gate needs new update '''
	
		# All bits needs update
		self.updatedBits = 0
		
		# Resets input signal
		self.inputSignal = 0;
		
	def connectOutput(self, circuitid, gateOutputBit, gateInputBit, gateName):
		''' Connects an output to an input '''
	
		op = self.OutputBit(gateName, gateInputBit)
		self.outputBits[gateOutputBit].append(op)
		
	def resetInputs(self):
	
		# Total of ocurrences of inputs and outputs is 0
		self.inputsOcurrNum = 0
		
		# All bits needs update
		self.updatedBits = 0
		
		# All input ocurrences are 0
		for i in self.input:
			i.resetOcurrence()
		
		# All output ocurrences are 0
		self.outputOccurr = [0]*(1<<self.nbitsOutput)
			
	def getInputNum(self):
		''' Get number of possible inputs '''
		return 1 << self.nbitsInput
		
	def getOutputNum(self):
		''' Get number of possible inputs '''
		return 1 << self.nbitsOutput
			
			
	@abstractmethod
	def _createOutputs(self):
		''' Creates subclass outputs '''
		
		pass
		
if __name__ == "__main__":
    pass