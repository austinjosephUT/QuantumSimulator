import numpy as np


class Parser:

    # algo. As you go compile- make a list of the controlled and target qubits
    # Should keep track which column the controlled gate with the controlled and target qubits are
    # go though the gates and create a transpiling order
    # if the values have both  (col== Col#ofControlled/MQ  && qubitNumber = Control or Target #)
    # store values when compiling of each multiqubit gate as the Col# qubit #

    def __init__(self, qasm_list):

        self.instructions = qasm_list
        del self.instructions[:3]  # delete header
        self.num_qubits = ((self.instructions[0].split("["))[1])[0]
        del self.instructions[:3]  # delete qreg, creg, and empty line
        self.new_instructions = []
        self.qubit_numbers = []
        self.controlled_numbers = []

        multi_qubit_gates = ['cx', 'cz', 'ccx']
        measurement_gates = ['measure']  # assume all the gates are measured
        controlled_gates = ['cx', 'cz', 'ccx', 'crz']  # double check for controlled gates when doing cont
        parameter_gates = ['u3', 'rz', 'rx', 'ry', 'u2', 'u1', 'crz']  # use and split into the parameters

        for i in range(len(self.instructions)):
            instr_parts = self.instructions[i].split(" ")
            print((instr_parts[0]))
            if (not (((instr_parts[0]) in measurement_gates) or ((instr_parts[0]) in multi_qubit_gates))):
                gate = instr_parts[0]
                qubit_number = (instr_parts[1])[2]
                self.new_instructions.append(gate)
                self.qubit_numbers.append(qubit_number)
                self.controlled_numbers.append(0)
            elif (instr_parts[0] in controlled_gates):
                gate = instr_parts[0]
                qubit_number = ''
                qubit_number += (instr_parts[1])[2]
                # qubit_number += '-'
                # qubit_number += (instr_parts[1])[7]
                self.new_instructions.append(gate)
                self.qubit_numbers.append(qubit_number)
                self.controlled_numbers.append((instr_parts[1])[7])
            elif ('swap' in (instr_parts[0])[0]):
                self.new_instructions.append(instr_parts[0])
            # same thing wiht appending the qubit numbers in a way that allows them to both be appended
            else:
                pass
            # frfkrmfkmfr
            # JUST MAKE SURE THAT THIS COVERS EVERYTHING

    def getGates(self):
        return self.new_instructions

    def getQubitNumbers(self):
        return self.qubit_numbers

    def getNumber_Qubits(self):
        return self.num_qubits

    def getControlledNumbers(self):
        return self.controlled_numbers
