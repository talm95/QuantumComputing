from qiskit import QuantumCircuit, Aer, assemble, transpile
from qiskit.visualization import plot_histogram
import numpy as np
from math import pi as pi
from QuantumFourierTransform import qft


def qpe_rotations(qc, measure_qubits_num, unitary_matrix, psi_qubits):
    u_gate = unitary_matrix.to_gate()
    for qubit in range(measure_qubits_num):
        qc.h(qubit)
        u2n = QuantumCircuit(psi_n, name='U^' + str(qubit**2))
        for i in range(2**qubit):
            u2n.append(u_gate, range(psi_n))
        u2n_gate = u2n.to_gate()
        controlled_u2n = u2n_gate.control()
        qc.append(controlled_u2n,
                  list(np.append([qubit], list(range(measure_qubits_num, measure_qubits_num + psi_qubits)))))
    return qc


def qpe_qft_dagger(qc, measure_qubits_num):
    qf = QuantumCircuit(measure_qubits_num)
    qft(qf, measure_qubits_num)
    inv_qf = qf.inverse()
    qc.append(inv_qf, range(measure_qubits_num))
    return qc


def qpe_measure(qc, measure_qubits_num):
    for qubit in range(measure_qubits_num):
        qc.measure(qubit, qubit)
    return qc


def qpe(qc, measure_qubits_num, unitary_matrix, psi_qubits):
    qpe_rotations(qc, measure_qubits_num, unitary_matrix, psi_qubits)
    qpe_qft_dagger(qc, measure_qubits_num)
    qpe_measure(qc, measure_qubits_num)
    return qc


n = 3
psi_n = 1
u_matrix = QuantumCircuit(psi_n, name='U')
u_matrix.p(pi/4, 0)
qc = QuantumCircuit(n + psi_n, n)
qc.x(n)
qpe(qc, n, u_matrix, psi_n)
qc.draw()

qasm_sim = Aer.get_backend('qasm_simulator')
shots = 2048
t_qpe = transpile(qc, qasm_sim)
qobj = assemble(t_qpe, shots=shots)
results = qasm_sim.run(qobj).result()
answer = results.get_counts()

plot_histogram(answer)

