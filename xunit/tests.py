class TestCase:
    def __init__(self, name):
        self.name = name

    def setup(self):
        pass

    def run(self):
        self.setup()
        method = getattr(self, self.name)
        method()


class WasRun(TestCase):
    def __init__(self, name):
        TestCase.__init__(self, name)

    def test_method(self):
        self.was_run = 1

    def setup(self):
        self.was_run = None
        self.was_setup = 1


class TestCaseTest(TestCase):
    def setup(self):
        self.test = WasRun('test_method')

    def test_running(self):
        self.test.run()
        assert(self.test.was_run), 'test_method was not run'

    def test_setup(self):
        self.test.run()
        assert(self.test.was_setup), f'test_method was not setup'


class Test:
    def run():
        TestCaseTest('test_running').run()
        TestCaseTest('test_setup').run()
