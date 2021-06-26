from qiskit import QuantumCircuit


def reflect_around_s_operation(number_of_qubits):
    s_reflection = QuantumCircuit(number_of_qubits, name='s_reflection')
    for qubit in range(number_of_qubits):
        s_reflection.h(qubit)
    for qubit in range(number_of_qubits):
        s_reflection.x(qubit)
    s_reflection.h(number_of_qubits - 1)
    s_reflection.mct([range(number_of_qubits - 1)], number_of_qubits - 1)
    s_reflection.h(number_of_qubits - 1)
    for qubit in range(number_of_qubits):
        s_reflection.x(qubit)
    for qubit in range(number_of_qubits):
        s_reflection.h(qubit)
    return s_reflection
