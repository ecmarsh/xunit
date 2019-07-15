class TestCase:
    def __init__(self, name):
        self.name = name

    def setup(self):
        pass

    def run(self):
        self.setup()
        method = getattr(self, self.name)
        method()
        self.teardown()


class WasRun(TestCase):
    def __init__(self, name):
        super().__init__(name)

    def TEST_METHOD(self):
        self.log = self.log + ' TEST_METHOD'

    def setup(self):
        self.log = 'setup'

    def teardown(self):
        self.log = self.log + ' teardown '


class TestCaseTest(TestCase):
    def test_template_method(self):
        test = WasRun('TEST_METHOD')
        test.run()
        assert(
            test.log == 'setup TEST_METHOD teardown '), f'Log is "{test.log}"'

    def teardown(self):
        pass


class Test:
    def test_started():
        print('Test started')

    def run():
        TestCaseTest('test_template_method').run()
