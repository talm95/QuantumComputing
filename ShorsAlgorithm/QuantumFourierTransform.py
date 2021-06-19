from qiskit import QuantumCircuit, QuantumRegister
from math import pi as pi


def qft_rotations(qc, n):
    if n == 0:
        return qc
    n -= 1
    qc.h(n)
    for qubit in range(n):
        qc.cp(pi/(2**(n-qubit)), qubit, n)
    qft_rotations(qc, n)


def qft_swap(qc, n):
    for qubit in range(n//2):
        qc.swap(qubit, n-1-qubit)
    return qc


def qft(qc, n):
    qft_rotations(qc, n)
    qft_swap(qc, n)
    return qc
