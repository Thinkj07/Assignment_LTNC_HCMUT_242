import unittest
from TestUtils import TestUtils

class TestSymbolTable(unittest.TestCase):
    def test_0(self):
        input = [
            "INSERT a3 number",
            "ASSIGN a3 ASSIGN",
        ]
        expected = ["Invalid: ASSIGN a3 ASSIGN"]
        self.assertTrue(TestUtils.check(input, expected, 100))
    def test_1(self):
        input = ["INSERT a string"]
        expected = ["success"]
        self.assertTrue(TestUtils.check(input, expected, 101))

    def test_2(self):
        input = ["INSERT b2 number"]
        expected = ["success"]
        self.assertTrue(TestUtils.check(input, expected, 102))

    def test_3(self):
        input = ["INSERT x number", "   "]
        expected = ["Invalid: Invalid command"]
        self.assertTrue(TestUtils.check(input, expected, 103))

    def test_4(self):
        input = ["INSERT b2 string"]
        expected = ["success"]
        self.assertTrue(TestUtils.check(input, expected, 104))

    def test_5(self):
        input = ["INSERT B string"]
        expected = ["Invalid: INSERT B string"]
        self.assertTrue(TestUtils.check(input, expected, 105))

    def test_6(self):
        input = [""]
        expected = ["Invalid: Invalid command"]
        self.assertTrue(TestUtils.check(input, expected, 106))

    def test_7(self):
        input = ["INSERT x number", "ASSIGN x 1"]
        expected = ["success", "success"]
        self.assertTrue(TestUtils.check(input, expected, 107))

    def test_8(self):
        input = ["Insert x number"]
        expected = ["Invalid: Invalid command"]
        self.assertTrue(TestUtils.check(input, expected, 108))

    def test_9(self):
        input = ["INSERT number number", "INSERT string string", "ASSIGN number string"]
        expected = ["TypeMismatch: ASSIGN number string"]
        self.assertTrue(TestUtils.check(input, expected, 109))

    def test_10(self):
        input = ["INSERT x number", "ASSIGN x 'a'"]
        expected = ["TypeMismatch: ASSIGN x 'a'"]
        self.assertTrue(TestUtils.check(input, expected, 110))

    def test_11(self):
        input = ["INSERT x string", "INSERT y number", "ASSIGN y x"]
        expected = ["TypeMismatch: ASSIGN y x"]
        self.assertTrue(TestUtils.check(input, expected, 111))

    def test_12(self):
        input = ["INSERT x number", "INSERT y string", "ASSIGN y x"]
        expected = ["TypeMismatch: ASSIGN y x"]
        self.assertTrue(TestUtils.check(input, expected, 112))

    def test_13(self):
        input = ["INSERT number number", "INSERT string string", "ASSIGN number string"]
        expected = ["TypeMismatch: ASSIGN number string"]
        self.assertTrue(TestUtils.check(input, expected, 113))

    def test_14(self):
        input = ["INSERT str string", "ASSIGN str 'abc cd'"]
        expected = ["Invalid: ASSIGN str 'abc cd'"]
        self.assertTrue(TestUtils.check(input, expected, 114))

    def test_15(self):
        input = ["INSERT string string", "INSERT number number", "ASSIGN number string"]
        expected = ["TypeMismatch: ASSIGN number string"]
        self.assertTrue(TestUtils.check(input, expected, 115))

    def test_16(self):
        input = ["INSERT string string", "INSERT number number", "ASSIGN string number"]
        expected = ["TypeMismatch: ASSIGN string number"]
        self.assertTrue(TestUtils.check(input, expected, 116))

    def test_17(self):
        input = ["ASSIGN jennie 1"]
        expected = ["Undeclared: ASSIGN jennie 1"]
        self.assertTrue(TestUtils.check(input, expected, 117))

    def test_18(self):
        input = ["INSERT x number", "ASSIGN x 123"]
        expected = ["success", "success"]
        self.assertTrue(TestUtils.check(input, expected, 118))

    def test_19(self):
        input = ["INSERT x number", "ASSIGN x 12.2"]
        expected = ["Invalid: ASSIGN x 12.2"]
        self.assertTrue(TestUtils.check(input, expected, 119))

    def test_20(self):
        input = ["INSERT x number", "ASSIGN x -122"]
        expected = ["Invalid: ASSIGN x -122"]
        self.assertTrue(TestUtils.check(input, expected, 120))

    def test_21(self):
        input = ["INSERT x string", "ASSIGN x 'a'"]
        expected = ["success", "success"]
        self.assertTrue(TestUtils.check(input, expected, 121))

    def test_22(self):
        input = ["BEGIN", "BEGIN", "END", "END"]
        expected = []
        self.assertTrue(TestUtils.check(input, expected, 122))

    def test_23(self):
        input = ["BEGIN", "BEGIN", "BEGIN", "END", "END", "END"]
        expected = []
        self.assertTrue(TestUtils.check(input, expected, 123))

    def test_24(self):
        input = ["BEGIN", "BEGIN", "END", "END", "BEGIN", "END"]
        expected = []
        self.assertTrue(TestUtils.check(input, expected, 124))

    def test_25(self):
        input = ["BEGIN", "INSERT x number", "BEGIN", "END", "END", "END", "BEGIN"]
        expected = ["UnknownBlock"]
        self.assertTrue(TestUtils.check(input, expected, 125))

    def test_26(self):
        input = ["INSERT x number", "END"]
        expected = ["UnknownBlock"]
        self.assertTrue(TestUtils.check(input, expected, 126))

    def test_27(self):
        input = ["BEGIN"]
        expected = ["UnclosedBlock: 1"]
        self.assertTrue(TestUtils.check(input, expected, 127))

    def test_28(self):
        input = ["INSERT x number", "BEGIN", "INSERT x number", "BEGIN", "INSERT x number", "BEGIN", "INSERT x number", "END", "END", "END"]
        expected = ["success", "success", "success", "success"]
        self.assertTrue(TestUtils.check(input, expected, 128))

    def test_29(self):
        input = ["BEGIN", "INSERT x number", "LOOKUP x", "END"]
        expected = ["success", "1"]
        self.assertTrue(TestUtils.check(input, expected, 129))

    def test_30(self):
        input = ["BEGIN", "INSERT x number", "LOOKUP x", "END"]
        expected = ["success", "1"]
        self.assertTrue(TestUtils.check(input, expected, 130))

    def test_31(self):
        input = ["BEGIN", "INSERT x number", "BEGIN",  "LOOKUP x", "END", "END"]
        expected = ["success", "1"]
        self.assertTrue(TestUtils.check(input, expected, 131))

    def test_32(self):
        input = ["BEGIN", "INSERT x number", "BEGIN", "INSERT x number", "LOOKUP x", "END", "END"]
        expected = ["success", "success", "2"]
        self.assertTrue(TestUtils.check(input, expected, 132))

    def test_33(self):
        input = ["INSERT x number", "BEGIN", "INSERT x number", "BEGIN", "LOOKUP x", "END", "END"]
        expected = ["success", "success", "1"]
        self.assertTrue(TestUtils.check(input, expected, 133))

    def test_34(self):
        input = ["INSERT x number", "BEGIN", "INSERT x number", "BEGIN", "LOOKUP x", "END", "END"]
        expected = ["success", "success", "1"]
        self.assertTrue(TestUtils.check(input, expected, 134))

    def test_35(self):
        input = ["INSERT x number", "BEGIN", "INSERT x number", "BEGIN", "INSERT x number", "END", "LOOKUP x", "END"]
        expected = ["success", "success", "success", "1"]
        self.assertTrue(TestUtils.check(input, expected, 135))

    def test_36(self):
        input = ["INSERT x string", "INSERT y string", "BEGIN", "INSERT x string", "INSERT y string", "END", "PRINT"]
        expected = ["success", "success", "success", "success","x//0 y//0"]
        self.assertTrue(TestUtils.check(input, expected, 136))

    def test_37(self):
        input = ["PRINT number"]
        expected = ["Invalid: PRINT number"]
        self.assertTrue(TestUtils.check(input, expected, 137))

    def test_38(self):
        input = ["INSERT x number", "PRINT x"]
        expected = ["Invalid: PRINT x"]
        self.assertTrue(TestUtils.check(input, expected, 138))

    def test_39(self):
        input = ["INSERT x number", "INSERT y number", "PRINT"]
        expected = ["success", "success", "x//0 y//0"]
        self.assertTrue(TestUtils.check(input, expected, 139))

    def test_40(self):
        input = ["     END"]
        expected = ["Invalid: Invalid command"]
        self.assertTrue(TestUtils.check(input, expected, 140))

    def test_41(self):
        input = ["BEGIN", "INSERT x string", "INSERT y string", "PRINT", "END"]
        expected = ["success", "success", "x//1 y//1"]
        self.assertTrue(TestUtils.check(input, expected, 141))

    def test_42(self):
        input = ["INSERT x string", "INSERT y string", "BEGIN", "INSERT x string", "INSERT y string", "PRINT", "END"]
        expected = ["success", "success", "success", "success", "x//1 y//1"]
        self.assertTrue(TestUtils.check(input, expected, 142))

    def test_43(self):
        input = ["RPRINT   "]
        expected = ["Invalid: RPRINT   "]
        self.assertTrue(TestUtils.check(input, expected, 143))

    def test_44(self):
        input = ["RPRINT number"]
        expected = ["Invalid: RPRINT number"]
        self.assertTrue(TestUtils.check(input, expected, 144))

    def test_45(self):
        input = ["INSERT x number", "RPRINT x"]
        expected = ["Invalid: RPRINT x"]
        self.assertTrue(TestUtils.check(input, expected, 145))

    def test_46(self):
        input = ["INSERT x number", "INSERT y number", "RPRINT"]
        expected = ["success", "success", "y//0 x//0"]
        self.assertTrue(TestUtils.check(input, expected, 146))

    def test_47(self):
        input = ["BEGIN", "INSERT x string", "INSERT y string", "END", "RPRINT"]
        expected = ["success", "success", ""]
        self.assertTrue(TestUtils.check(input, expected, 147))

    def test_48(self):
        input = ["BEGIN", "INSERT x string", "INSERT y string", "RPRINT", "END"]
        expected = ["success", "success", "y//1 x//1"]
        self.assertTrue(TestUtils.check(input, expected, 148))

    def test_49(self):
        input = ["INSERT x string", "INSERT y string", "BEGIN", "INSERT x string", "INSERT y string", "RPRINT", "END"]
        expected = ["success", "success", "success", "success", "y//1 x//1"]
        self.assertTrue(TestUtils.check(input, expected, 149))
