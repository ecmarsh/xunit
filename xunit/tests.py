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
            result.test_failed(method.__name__)
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
        self.failed_tests.append(method)
        self.fail_count = self.fail_count + 1

    def summary(self):
        return f'{self.run_count} run, {self.fail_count} failed'

    def get_failed_tests(self):
        if (self.fail_count > 0):
            return f'Failed tests: {"".join(self.failed_tests)}'
        return 'All tests passed ✅'


class WasRun(TestCase):
    def __init__(self, name):
        super().__init__(name)

    def setup(self):
        self.log = 'setup'

    def TEST_METHOD(self):
        self.log = self.log + ' TEST_METHOD'

    def TEST_BROKEN_METHOD(self):
        raise Exception

    def teardown(self):
        self.log = self.log + ' teardown'


class TestCaseTest(TestCase):
    def setup(self):
        self.result = TestResult()

    def test_template_method(self):
        test = WasRun('TEST_METHOD')
        test.run(self.result)
        assert(
            test.log == 'setup TEST_METHOD teardown'), f'Log is "{test.log}"'

    def test_result(self):
        "Records results of running the test(s)"
        test = WasRun('TEST_METHOD')
        result = test.run(self.result)
        assert('1 run, 0 failed' == self.result.summary()
               ), f'result: {self.result.summary()}'

    def test_failed_result(self):
        test = WasRun('TEST_BROKEN_METHOD')
        result = test.run(self.result)
        assert('1 run, 1 failed' == self.result.summary()
               ), f'test_failed: {self.result.summary()}'

    def test_failed_result_formatting(self):
        self.result.test_started()
        self.result.test_failed()
        assert('1 run, 1 failed' == self.result.summary()
               ), f'test_fail_format: {self.result.summary()}'

    def test_test_suite(self):
        suite = TestSuite()
        suite.add(WasRun('TEST_METHOD'))
        suite.add(WasRun('TEST_BROKEN_METHOD'))

        # Collecting Parameter
        suite.run(self.result)

        assert('2 run, 1 failed' == self.result.summary()
               ), f'test_fail_format: {self.result.summary()}'

    def teardown(self):
        pass


class TestSuite:
    def __init__(self):
        self.tests = []

    def add(self, test):
        self.tests.append(test)

    def run(self, result):
        for test in self.tests:
            test.run(result)


class Test:
    def run():
        suite = TestSuite()
        suite.add(TestCaseTest('test_template_method'))
        suite.add(TestCaseTest('test_result'))
        suite.add(TestCaseTest('test_failed_result_formatting'))
        suite.add(TestCaseTest('test_failed_result'))
        suite.add(TestCaseTest('test_test_suite'))
        result = TestResult()
        suite.run(result)
        print(result.summary())
        print(result.get_failed_tests())
