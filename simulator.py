# Written by Austin Joseph
import numpy as np
from textInput import Parser
from fractions import Fraction
import cmath
import math
import random
import matplotlib.pyplot as plt

############################################################# USER INPUT VARIABLES #######################################################################

filepath = "qasm.qasm"  # NOTE FOR USER: keep the simulator files in the same directory as the QASM files you need to run
num_shots = 1024  # number of shots

# code for prompt based answer will be left out for ease of use and running the file.

############################################################ READING IN INPUT ##################################################################################


file = open(filepath, "r")
content = file.read()

qasm_str = content.splitlines()
file.close()
print(qasm_str)

# create parser object
qasm_parser = Parser(qasm_str)
numQubits = int(qasm_parser.num_qubits)
gates = qasm_parser.getGates()
qubit_numbers = qasm_parser.getQubitNumbers()
controlled_numbers = qasm_parser.getControlledNumbers()

print("Num Qubits:" + str(numQubits))
print("Gates:")
for i in range(len(gates)):
    print(gates[i])
print("Qubit Numbers")
for i in range(len(qubit_numbers)):
    print(qubit_numbers[i])
print("Controlled Numbers:")
for i in range(len(controlled_numbers)):
    print(controlled_numbers[i])

print()

############################################################ SETTING GATE VALUES ##############################################################################

zero_state = np.array([1, 0])
one_state = np.array([0, 1])
H_gate = np.array([[1, 1], [1, -1]] * 1 / np.sqrt(2))
Y_gate = np.array([[0, -1j], [1j, 0]])
X_gate = np.array([[0, 1], [1, 0]])
Z_gate = np.array([[1, 0], [0, -1]])
Id_gate = np.array([[1, 0], [0, 1]])
S_gate = np.array([[1, 0], [0, 1j]])
Sdg_gate = np.array([[1, 0], [0, -1j]])
T_gate = np.array([[1, 0], [0, np.exp(1j * np.pi / 4)]])
Tdg_gate = np.array([[1, 0], [0, np.exp(-1j * np.pi / 4)]])
# Rx_gate = [[np.cos(theta/2),-1j*np.sin(theta)/2],[-1j*np.sin(theta/2),np.cos(theta/2)]]
# Ry_gate = [[np.cos(theta/2),-np.sin(theta/2)],[np.sin(theta/2),np.cos(theta/2)]]
# Rz_gate = [[np.exp(-1j*theta/2),0],[0,np.exp(1j*theta/2)]]
# U3,U2,U1
# CX
# These 7 gates are implemented but depend on more complicated parsing

############################################################ SIMULATE GOING THROUGH GATES #######################################################################


# Go iterate from 0 to numQubits-1 and go ahead apply the matrix by matmul to each current state
# keep current state array initialize with all values of zero
currentState = [0] * numQubits
for i in range(0, numQubits):
    currentState[i] = zero_state

# now iterate through gates
for i in range(len(gates)):
    gate_str = gates[i]
    currentQubitOp = int(qubit_numbers[i])
    target = int(controlled_numbers[i])
    print("Initial States")
    print(currentState)
    if gate_str == 'h':
        currentState[currentQubitOp] = np.matmul(H_gate, currentState[currentQubitOp])
    elif gate_str == 'x':
        currentState[currentQubitOp] = np.matmul(X_gate, currentState[currentQubitOp])
    elif gate_str == 'y':
        currentState[currentQubitOp] = np.matmul(Y_gate, currentState[currentQubitOp])
    elif gate_str == 'z':
        currentState[currentQubitOp] = np.matmul(Z_gate, currentState[currentQubitOp])
    elif gate_str == 'id':
        currentState[currentQubitOp] = np.matmul(Id_gate, currentState[currentQubitOp])
    elif gate_str == 'rx':
        a = gate_str.find('(') + 1
        b = gate_str.find(')')
        if 'pi' in gate_str[a:b]:
            theta = float(Fraction(gate_str[a:b].replace('pi', '1'))) * math.pi
        else:
            theta = float(Fraction(gate_str[a:b]))
        RxGate = np.array([[np.cos(theta / 2), -1j * np.sin(theta) / 2], [-1j * np.sin(theta / 2), np.cos(theta / 2)]])
        currentState[currentQubitOp] = np.matmul(Rx_gate, currentState[currentQubitOp])
    elif gate_str == 'ry':
        a = gate_str.find('(') + 1
        b = gate_str.find(')')
        if 'pi' in gate_str[a:b]:
            theta = float(Fraction(gate_str[a:b].replace('pi', '1'))) * math.pi
        else:
            theta = float(Fraction(gate_str[a:b]))
        RyGate = np.array([[np.cos(theta / 2), -np.sin(theta / 2)], [np.sin(theta / 2), np.cos(theta / 2)]])
        currentState[currentQubitOp] = np.matmul(Ry_gate, currentState[currentQubitOp])
    elif gate_str == 'rz':
        a = gate_str.find('(') + 1
        b = gate_str.find(')')
        if 'pi' in gate_str[a:b]:
            theta = float(Fraction(gate_str[a:b].replace('pi', '1'))) * math.pi
        else:
            theta = float(Fraction(gate_str[a:b]))
        RzGate = np.array([[np.exp(-1j * theta / 2), 0], [0, np.exp(1j * theta / 2)]])
        currentState[currentQubitOp] = np.matmul(Rz_gate, currentState[currentQubitOp])
    elif gate_str == 's':
        currentState[currentQubitOp] = np.matmul(S_gate, currentState[currentQubitOp])
    elif gate_str == 'sdg':
        currentState[currentQubitOp] = np.matmul(Sdg_gate, currentState[currentQubitOp])
    elif gate_str == 't':
        currentState[currentQubitOp] = np.matmul(T_gate, currentState[currentQubitOp])
    elif gate_str == 'tdg':
        currentState[currentQubitOp] = np.matmul(Tdg_gate, currentState[currentQubitOp])
    elif 'u1' in gate_str:
        a = gate_str.find('(') + 1
        b = gate_str.find(')')
        print(gate_str[a:b])
        if 'pi' in gate_str[a:b]:
            lamb = float(Fraction(gate_str[a:b].replace('pi', '1'))) * math.pi
        else:
            lamb = float(Fraction(gate_str[a:b]))
        currentGate = np.array([[1, 0], [0, cmath.rect(1, lamb)]])
        currentState[currentQubitOp] = np.matmul(currentGate, currentState[currentQubitOp])
    elif 'u2' in gate_str:
        a = gate_str.find('(') + 1
        b = gate_str.find(',')
        print(gate_str[a:b])
        if 'pi' in gate_str[a:b]:
            phi = float(Fraction(gate_str[a:b].replace('pi', '1'))) * math.pi
        else:
            phi = float(Fraction(gate_str[a:b]))
        c = b + 1
        d = gate_str.find(')')
        print(gate_str[c:d])
        if 'pi' in gate_str[c:d]:
            lamb = float(Fraction(gate_str[c:d].replace('pi', '1'))) * math.pi
        else:
            lamb = float(Fraction(gate_str[c:d]))
        currentGate = 1 / 2 ** (1 / 2) * np.array(
            [[1, cmath.rect(-1, lamb)], [cmath.rect(1, phi), cmath.rect(1, lamb + phi)]])
        currentState[currentQubitOp] = np.matmul(currentGate, currentState[currentQubitOp])
    elif 'u3' in gate_str:
        angles = gate_str.split(',')
        print("Angles:")
        print(angles)
        first_angle = angles[0].split("(")
        a = first_angle[1]
        # a = (angles[0])[3:]
        b = (angles[1])
        c = (angles[2])[:-1]
        print(a)
        print(b)
        print(c)
        if 'pi' in a:
            theta = float(Fraction((a.replace('pi', '1')))) * math.pi
        else:
            theta = float(Fraction(a))
        if 'pi' in b:
            phi = float(Fraction(b.replace('pi', '1'))) * math.pi
        else:
            phi = float(Fraction(b))
        if 'pi' in c:
            lamb = float(Fraction((c.replace('pi', '1')))) * math.pi
        else:
            lamb = float(Fraction(c))
        currentGate = np.array([[math.cos(theta / 2), cmath.rect(-1, lamb) * math.sin(theta / 2)],
                                [cmath.rect(1, phi) * math.sin(theta / 2),
                                 cmath.rect(1, lamb + phi) * math.cos(theta / 2)]])
        currentState[currentQubitOp] = np.matmul(currentGate, currentState[currentQubitOp])
    elif gate_str == 'cx':
        control = qubit_numbers[0]
        target = int(
            controlled_numbers[i])  # means you have to put in a zero when there isn't a control gate in parsing
        if ((currentState[currentQubitOp] == one_state).all()):
            currentState[target] = np.matmul(X_gate, currentState[target])
    print("After Operation:")
    print(currentState[currentQubitOp])

print("Final QubitState:")
print(currentState)
print()

################################################################# TENSORIZE STATES ###########################################################################################################################

currentTensor = currentState[numQubits - 1]
for i in range(numQubits - 2, -1, -1):
    print("Current Tensor")
    print(currentTensor)
    print(i)
    currentTensor = np.kron(currentTensor, currentState[i])
print("final tensor")
print(currentTensor)

print("Ideal Quantum State")
print(currentTensor)
print()
# if these two are the same then we are doing the correct thing


################################################################# SET PROBABILITIES UP ############################################################################################################################


prob_array = [0] * (2 ** numQubits)
print("initialized Prob array:")
print(prob_array)

for i in range(2 ** numQubits):
    print(currentTensor[i])
    print(np.conj(currentTensor[i]))
    prob_array[i] = currentTensor[i] * np.conj(currentTensor[i])
    print("New PROB VALUE")
    print(prob_array[i])

print("Prob Array")
print(prob_array)

##################################################################### RUN SIMULATOR COUNTS ##############################################################################################3


count_array = [0] * len(prob_array)
for i in range(num_shots):
    probValue = 0
    rand = random.uniform(0, 1)
    for j in range(len(prob_array)):
        prob = prob_array[j]
        if rand < prob + probValue:
            count_array[j] = count_array[j] + 1
            break
        else:
            probValue += prob
print("Count Array")
print(count_array)
print()

################################################################## RETURN STATE OUTPUT ##############################################################################################################


states_counted = []
counts_ofRelevantStates = []
for i in range(len(count_array)):
    if count_array[i] != 0:
        binary_rep = np.binary_repr(i, width=numQubits)
        states_counted.append(str(binary_rep))
        counts_ofRelevantStates.append(count_array[i])
        # biNum = bin(i).replace('b','')
        print('Shots Registered in |' + binary_rep + '> = ', count_array[i])
print()

################################################################## VISUALIZATION OUTPUT ######################################################################################

print("states_counted")
print(states_counted)
print("counts_ofRelevantStates")
print(counts_ofRelevantStates)

# using matplotlib to make a histogram of results
y_pos = np.arange(len(states_counted))
plt.barh(y_pos, counts_ofRelevantStates, align='center', alpha=0.5)
plt.yticks(y_pos, states_counted)
plt.xlabel('Counts')
plt.title('Ideal Quantum Simulator Counts')
plt.show()

################################################################## ADVANCED VISUALIZATION #############################################################################################


# took it out because at the moment the complexities were a bit much but would love to talk to the professors over the break and send them
# something cool that I'm making


################################################################## NOTES #################################################################################################################


"""
	The hardest thing about the project was learning the ins and outs of the language
	This was my third iteration of coding this and the most simple at the end
	Without knowing the language well, we were held back for a while with some more complex errors that took a lot more time than expected to 
	fix


"""

