from wire import Wire


class Gate:
    def __init__(self, inputs, output):
        self._inputs = None
        self._output = None

        self.inputs = inputs
        self.output = output

    @property
    def inputs(self):
        return self._inputs

    @inputs.setter
    def inputs(self, inputs):
        for i in inputs:
            if isinstance(i, Wire):
                i += self
        self._inputs = inputs

    @property
    def output(self):
        return self._output

    @output.setter
    def output(self, output):
        if isinstance(output, Wire):
            output.input = self
        self._output = output

    @property
    def value(self):
        raise NotImplementedError()


class AND(Gate):
    def __init__(self, a, b, output):
        super().__init__([a, b], output)

        self.a = a
        self.b = b

    def __repr__(self):
        return f"AND({self.a} & {self.b})"

    @property
    def value(self):
        return self.a.value & self.b.value


class NOT(Gate):
    def __init__(self, a, output):
        super().__init__([a], output)

        self.a = a

    def __repr__(self):
        return f"NOT(~{self.a})"

    @property
    def value(self):
        return ~self.a.value


class OR(Gate):
    def __init__(self, a, b, output):
        super().__init__([a, b], output)

        self.a = a
        self.b = b

    def __repr__(self):
        return f"AND({self.a} | {self.b})"

    @property
    def value(self):
        return self.a.value | self.b.value


class LSHIFT(Gate):
    def __init__(self, a, shift, output):
        super().__init__([a], output)

        self.a = a
        self.shift = int(shift)

    def __repr__(self):
        return f"LSHIFT({self.a} << {self.shift})"

    @property
    def value(self):
        return self.a.value << self.shift


class RSHIFT(Gate):
    def __init__(self, a, shift, output):
        super().__init__([a], output)

        self.a = a
        self.shift = int(shift)

    def __repr__(self):
        return f"RSHIFT({self.a} >> {self.shift})"

    @property
    def value(self):
        return self.a.value >> self.shift
