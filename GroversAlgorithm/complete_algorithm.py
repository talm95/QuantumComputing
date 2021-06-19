from qiskit import QuantumCircuit


def grover_algorithm(oracle, s_reflection, iterations, number_of_qubits):
    grover_circuit = QuantumCircuit(number_of_qubits)
    for qubit in range(number_of_qubits):
        grover_circuit.h(qubit)
        for iteration in range(iterations):
            grover_circuit.append(oracle, range(number_of_qubits))
            grover_circuit.append(s_reflection, range(number_of_qubits))
    return grover_circuit
