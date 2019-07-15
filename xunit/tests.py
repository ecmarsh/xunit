class TestCase:
    def __init__(self, name):
        self.name = name

    def run(self):
        method = getattr(self, self.name)
        method()


class WasRun(TestCase):
    def __init__(self, name):
        self.was_run = None
        TestCase.__init__(self, name)

    def test_method(self):
        self.was_run = 1


class TestCaseTest(TestCase):
    def test_running(self):
        test = WasRun('test_method')
        assert(test.was_run), 'Test method was run'
        test.run()
        assert(test.was_run), 'Test method was not run'


class Test:
    def run():
        TestCaseTest('test_running').run()
