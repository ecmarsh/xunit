class TestCase:
    def __init__(self, name):
        self.name = name

    def setup(self):
        pass

    def run(self, result):
        result.test_started()
        self.setup()
        method = getattr(self, self.name)
        try:
            method()
        except:
            result.test_failed(self.name)
        finally:
            self.teardown()


class TestResult:
    def __init__(self):
        self.run_count = 0
        self.fail_count = 0
        self.failed_tests = []

    def test_started(self):
        self.run_count = self.run_count + 1

    def test_failed(self, method):
        self.failed_tests.append(f'{method}')
        self.fail_count = self.fail_count + 1

    @property
    def summary(self):
        return f'{self.run_count} run, {self.fail_count} failed'

    def failed_summary(self):
        if (self.fail_count > 0):
            separator = ''
            if len(self.failed_tests) > 1:
                separator = ','
            return f'Failed tests: {separator.join(self.failed_tests)}'

        return 'All tests passed ✅'


class TestSuite:
    def __init__(self):
        self.tests = []

    def add(self, test):
        self.tests.append(test)

    def run(self, result):
        for test in self.tests:
            test.run(result)


class WasRun(TestCase):
    def __init__(self, name):
        super().__init__(name)

    def setup(self):
        self.log = 'setup'

    def TEST_METHOD(self):
        self.log = self.log + ' TEST_METHOD'

    def TEST_BROKEN_METHOD(self):
        self.log = self.log + ' TEST_BROKEN_METHOD'
        raise Exception

    def teardown(self):
        self.log = self.log + ' teardown'


class TestCaseTest(TestCase):
    def setup(self):
        self.result = TestResult()

    def test_template_method(self):
        test = WasRun('TEST_METHOD')
        test.run(self.result)
        assert test.log == 'setup TEST_METHOD teardown'

    def test_teardown_after_fail(self):
        test = WasRun('TEST_BROKEN_METHOD')
        test.run(self.result)
        assert test.log == 'setup TEST_BROKEN_METHOD teardown'

    def test_result(self):
        test = WasRun('TEST_METHOD')
        test.run(self.result)
        assert self.result.summary == '1 run, 0 failed'

    def test_failed_result(self):
        test = WasRun('TEST_BROKEN_METHOD')
        test.run(self.result)
        assert self.result.summary == '1 run, 1 failed'

    def test_test_suite(self):
        suite = TestSuite()
        suite.add(WasRun('TEST_METHOD'))
        suite.add(WasRun('TEST_BROKEN_METHOD'))

        # Collecting Parameter
        suite.run(self.result)

        assert self.result.summary == '2 run, 1 failed', \
            f'test_fail_format: {self.result.summary}'

    def teardown(self):
        pass


class Test:
    def run():
        suite = TestSuite()
        suite.add(TestCaseTest('test_template_method'))
        suite.add(TestCaseTest('test_teardown_after_fail'))
        suite.add(TestCaseTest('test_result'))
        suite.add(TestCaseTest('test_failed_result'))
        suite.add(TestCaseTest('test_test_suite'))
        result = TestResult()
        suite.run(result)
        print(result.summary)
        print(result.failed_summary())
