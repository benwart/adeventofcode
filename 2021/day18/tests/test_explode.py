from exercise_1b import explode

# def str_to_number(n):
#     return [c if tryint for c in n if c != ","]
#     for c in n:
#         if 


class TestExplode(object):
    def test_one(self):
        input = ['[', '[', '[', '[', '[', 9, 8, ']', 1, ']', 2, ']', 3, ']', 4, ']']
        expected = ['[', '[', '[', '[', 0, 9, ']', 2, ']', 3, ']', 4, ']']

        result = explode(input)

        assert(result == True)
        assert(input == expected)

    def test_two(self):
        input = ['[',7,'[',6,'[',5,'[',4,'[',3,2,']',']',']',']',']']
        expected = ['[',7,'[',6,'[',5,'[',7,0,']',']',']',']']

        result = explode(input)

        assert(result == True)
        assert(input == expected)

    # def test_three(self):
    #     input = "[[6,[5,[4,[3,2]]]],1]"
    #     expected = ['[',7,'[',6,'[',5,'[',7,0,']',']',']',']']

    #     result = explode(input)

    #     assert(result == True)
    #     assert(input == expected)

    # def test_four(self):
    #     input = ['[',7,'[',6,'[',5,'[',4,'[',3,2,']',']',']',']',']']
    #     expected = ['[',7,'[',6,'[',5,'[',7,0,']',']',']',']']

    #     result = explode(input)

    #     assert(result == True)
    #     assert(input == expected)

    # def test_five(self):
    #     input = ['[',7,'[',6,'[',5,'[',4,'[',3,2,']',']',']',']',']']
    #     expected = ['[',7,'[',6,'[',5,'[',7,0,']',']',']',']']

    #     result = explode(input)

    #     assert(result == True)
    #     assert(input == expected)