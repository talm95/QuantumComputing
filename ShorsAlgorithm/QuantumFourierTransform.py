from math import pi as pi


# This qft is without concerning qiskit's reverse order
# def qft_rotations(qc, n):
#     for qubit in range(n):
#         qc.h(qubit)
#         for controlled in range(qubit + 1, n):
#             qc.cp(pi/(2 ** (controlled - qubit)), qubit, controlled)


def qft_rotations(qc, n):
    if n == 0:
        return qc
    n -= 1
    qc.h(n)
    for qubit in range(n):
        qc.cp(pi/(2**(n-qubit)), qubit, n)
    qft_rotations(qc, n)


# I modified the rotations method to be directly the desired circuit instead of the need to swap
def qft_swap(qc, n):
    for qubit in range(n//2):
        qc.swap(qubit, n-1-qubit)
    return qc


def qft(qc, n):
    qft_rotations(qc, n)
    return qc
