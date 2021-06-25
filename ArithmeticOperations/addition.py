from qiskit import QuantumCircuit, Aer, transpile, assemble
import matplotlib.pyplot as plt
from qiskit.visualization import plot_histogram


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


a = QuantumCircuit(4, name='a')
a.x([0, 2])
b = QuantumCircuit(4, name='b')
b.x([2, 3])

a_plus_b = addition_3n_plus_1(a, b)
a_plus_b.draw(output='mpl', scale=0.5)
plt.show()

aer_sim = Aer.get_backend('aer_simulator')
t_qc = transpile(a_plus_b, aer_sim)
qobj = assemble(t_qc)
results = aer_sim.run(qobj).result()
counts = results.get_counts()
plot_histogram(counts)
plt.show()
