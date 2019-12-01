from LogicGate import LogicGate

class NOTGate(LogicGate):

	def __init__(self, circuitid, name, nbitsInput):
	
		# Base class constructor with nbitsInput and 1 output
		super().__init__(circuitid, name, nbitsInput)
		
		# Creates all outputs from inputs
		self._createOutputs()
		
	def _createOutputs(self):
		''' Applies NOT logic  '''
		
		# (0=>1 and 1=>0) '''
		for i in range(0, self.getInputNum()):
			self._addOutputValue(i, i^1)
			
class ANDGate(LogicGate):

	def __init__(self, circuitid, name, nbitsInput):
	
		# Base class constructor with nbitsInput and 1 output
		super().__init__(circuitid, name, nbitsInput)
		
		# Creates all outputs from inputs
		self._createOutputs()
		
	def _createOutputs(self):
		''' Applies AND logic  '''
		
		# (1 only if all inputs are 1) '''
		for i in range(0, self.getInputNum()-1):
			self._addOutputValue(i, 0)

		self._addOutputValue(self.nbitsInput-1, 1);
		
class ORGate(LogicGate):

	def __init__(self, circuitid, name, nbitsInput):
	
		# Base class constructor with nbitsInput and 1 output
		super().__init__(circuitid, name, nbitsInput)
		
		# Creates all outputs from inputs
		self._createOutputs()
		
	def _createOutputs(self):
		''' Applies OR logic  '''
		
		# (0 only if all inputs are 0) '''
		for i in range(1, self.getInputNum()):
			self._addOutputValue(i, 1)

		self._addOutputValue(0, 0);

class NANDGate(LogicGate):

	def __init__(self, circuitid, name, nbitsInput):
	
		# Base class constructor with nbitsInput and 1 output
		super().__init__(circuitid, name, nbitsInput)
		
		# Creates all outputs from inputs
		self._createOutputs()
		
	def _createOutputs(self):
		''' Applies NAND logic  '''
		
		# (0 only if all inputs are 1) '''
		for i in range(0, self.getInputNum()-1):
			self._addOutputValue(0, 1)

		self._addOutputValue(self.nbitsInput-1, 0);

class NORGate(LogicGate):

	def __init__(self, circuitid, name, nbitsInput):
	
		# Base class constructor with nbitsInput and 1 output
		super().__init__(circuitid, name, nbitsInput)
		
		# Creates all outputs from inputs
		self._createOutputs()
		
	def _createOutputs(self):
		''' Applies NOR logic  '''
		
		# (1 only if all inputs are 0) '''
		for i in range(1, self.getInputNum()):
			self._addOutputValue(0, 0)

		self._addOutputValue(0, 1);
		
class MAJGate(LogicGate):

	def __init__(self, circuitid, name, nbitsInput):
	
		# Base class constructor with nbitsInput and 1 output
		super().__init__(circuitid, name, nbitsInput)
		
		# Creates all outputs from inputs
		self._createOutputs()
		
	def _createOutputs(self):
		''' Applies MAJORITY logic  '''
		
		# If more than half are 'X', than we have 'X' '''
		for i in range(0, self.getInputNum()):
		
			mask = 1
			times = 0
			
			for j in range(0, self.getInputNum()):
				if (mask & i):
					times += 1
				
				mask = mask << 1
					
			if times > (self.nbitsInput>>1):
				self._addOutputValue(i, 1)
			else:
				self._addOutputValue(i, 0)
				
class BUFFERGate(LogicGate):

	def __init__(self, circuitid, name, nbitsInput):
	
		# Base class constructor with nbitsInput and 1 output
		super().__init__(circuitid, name, nbitsInput, nbitsInput)
		
		# Creates all outputs from inputs
		self._createOutputs()
		
	def _createOutputs(self):
		''' Applies BUFFER logic  '''
		
		# (0=>0 and 1=>1) '''
		for i in range(0, self.getInputNum()):
			self._addOutputValue(i, i)
			
class GENERICGate(LogicGate):

	def __init__(self, circuitid, name, nbitsInput, nbitsOutput, logic_inputs, logic_outputs):
	
		# Base class constructor with nbitsInput and 1 output
		super().__init__(circuitid, name, nbitsInput, nbitsOutput)
		
		# Creates all outputs from inputs
		self.__createOutputs(logic_inputs, logic_outputs)
		
	def __createOutputs(self, logic_inputs, logic_outputs):
		''' Applies GENERIC logic  '''
		for i in range(0, logic_inputs):
			self._addOutputValue(logic_inputs[i], logic_outputs[i])
		
	def _createOutputs(self):
		''' Does nothing  '''
		pass
			
if __name__ == "__main__":
    pass