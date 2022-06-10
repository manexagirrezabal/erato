



class generalevaluator(object):
    def __init__(self):
        pass

    def __str__(self):
        pass


    @staticmethod
    def evaluate(self, input_text, expected_value):
        result = self.analyze(input_text)
        if expected_value == result:
            return ("syllablecheck", 1)
        else:
            return ("syllablecheck", 0)
