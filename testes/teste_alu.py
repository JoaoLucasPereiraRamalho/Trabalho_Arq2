import sys
import os
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.hardware import ALU
from src.common.constantes import Opcode

class TesteALU(unittest.TestCase):
    def setUp(self):
        self.alu = ALU()

    def test_add_basico(self):
        res = self.alu.executar(Opcode.ADD, 10, 20)
        self.assertEqual(res, 30)
        self.assertFalse(self.alu.zero)

    def test_mult_nova_instrucao(self):
        res = self.alu.executar(Opcode.MULT, 5, 4)
        self.assertEqual(res, 20)

    def test_div_nova_instrucao(self):
        res = self.alu.executar(Opcode.DIV, 20, 3)
        self.assertEqual(res, 6)
        
    def test_div_por_zero(self):
        res = self.alu.executar(Opcode.DIV, 10, 0)
        self.assertEqual(res, 0)
        self.assertTrue(self.alu.overflow)

    def test_pow_nova_instrucao(self):
        res = self.alu.executar(Opcode.POW, 2, 10)
        self.assertEqual(res, 1024)

    def test_slt_nova_instrucao(self):
        self.assertEqual(self.alu.executar(Opcode.SLT, 10, 20), 1)
        self.assertEqual(self.alu.executar(Opcode.SLT, 20, 10), 0)

if __name__ == "__main__":
    unittest.main()