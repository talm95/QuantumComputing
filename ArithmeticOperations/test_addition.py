from unittest import TestCase
from qiskit import QuantumCircuit
from addition import qft_addition, qft_subtraction
from Utils.simulation import simulate_with_aer


class Test(TestCase):

    a = QuantumCircuit(4, name='a')
    a.x([2, 3])
    b = QuantumCircuit(4, name='b')
    b.x([0, 1, 3])

    def test_qft_addition(self):
        a_plus_b = qft_addition(self.a, self.b)
        counts = simulate_with_aer(a_plus_b, draw=False, plot_results=False)
        result = counts.most_frequent()
        self.assertEqual(result, '10111')

    def test_qft_subtraction(self):
        a_minus_b = qft_subtraction(self.a, self.b)
        counts = simulate_with_aer(a_minus_b, draw=False, plot_results=False)
        result = counts.most_frequent()
        self.assertEqual(result, '00001')
