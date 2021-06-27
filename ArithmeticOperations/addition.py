from qiskit import QuantumCircuit, Aer, transpile, assemble
import matplotlib.pyplot as plt
from qiskit.visualization import plot_histogram
from ShorsAlgorithm.QuantumFourierTransform import qft
from math import pi


def addition_3n_plus_1(a, b):
    single_circuit_size = max(a.num_qubits, b.num_qubits)
    a_plus_b = QuantumCircuit(single_circuit_size * 3 + 1, single_circuit_size + 1)
    a_plus_b.append(a, range(single_circuit_size))
    a_plus_b.append(b, range(single_circuit_size, 2 * single_circuit_size))

    for qubit in range(0, single_circuit_size):
        if qubit > 0:
            a_plus_b.ccx(qubit, qubit + 2 * single_circuit_size, qubit + 2 * single_circuit_size + 1)
            a_plus_b.ccx(qubit + single_circuit_size, qubit + 2*single_circuit_size, qubit + 2*single_circuit_size + 1)

        a_plus_b.ccx(qubit, qubit + single_circuit_size, qubit + 2*single_circuit_size + 1)
        a_plus_b.cx(qubit, qubit + 2 * single_circuit_size)
        a_plus_b.cx(qubit + single_circuit_size, qubit + 2 * single_circuit_size)
        a_plus_b.barrier()

    for register in range(single_circuit_size + 1):
        a_plus_b.measure(register + single_circuit_size * 2, register)

    return a_plus_b


def addition_with_qft(a, b):
    single_circuit_size = max(a.num_qubits, b.num_qubits) + 1

    # create a_plus_b circuit
    a_plus_b = QuantumCircuit(2 * single_circuit_size, single_circuit_size)
    a_plus_b.append(a, range(single_circuit_size - 1))
    a_plus_b.append(b, range(single_circuit_size, 2 * single_circuit_size - 1))

    # use qft circuit on b value
    qft_circuit = QuantumCircuit(single_circuit_size, name='QFT')
    qft(qft_circuit, single_circuit_size)
    a_plus_b.append(qft_circuit, range(single_circuit_size, 2 * single_circuit_size))

    # add a to b in the fourier space
    for power in range(0, single_circuit_size):
        for controlled in range(single_circuit_size - 1 - power, -1, -1):
            a_plus_b.cp(pi / (2 ** power), controlled, single_circuit_size + controlled + power)

    # reverse qft
    a_plus_b.append(qft_circuit.inverse(), range(single_circuit_size, 2 * single_circuit_size))

    # perform measure
    for register in range(single_circuit_size):
        a_plus_b.measure(register + single_circuit_size, register)

    return a_plus_b


a = QuantumCircuit(4, name='a')
a.x([2, 3])
b = QuantumCircuit(4, name='b')
b.x([0, 1, 3])

a_plus_b = addition_with_qft(a, b)
a_plus_b.draw(output='mpl', scale=0.5)
plt.show()

aer_sim = Aer.get_backend('aer_simulator')
t_qc = transpile(a_plus_b, aer_sim)
t_qc.draw(output='mpl', scale=0.5)
plt.show()
qobj = assemble(t_qc)
results = aer_sim.run(qobj).result()
counts = results.get_counts()
plot_histogram(counts)
plt.show()
