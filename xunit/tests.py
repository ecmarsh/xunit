import re


class TestSuite:
    def __init__(self):
        self.tests = []

    def add(self, test):
        self.tests.append(test)

    def run(self, result):
        for test in self.tests:
            test.run(result)


class TestCase:
    def __init__(self, name):
        self.name = name

    suite = TestSuite()

    def setup(self):
        """Default if a subclass does not shadow"""
        self.result = TestResult()

    def teardown(self):
        pass

    def run(self, result):
        result.test_started()
        method = getattr(self, self.name)
        try:
            self.setup()
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
        self.failed_tests.append(method)
        self.fail_count = self.fail_count + 1

    @property
    def summary(self):
        return f'{self.run_count} run, {self.fail_count} failed'

    @property
    def summary_detail(self):
        if (self.fail_count > 0):
            return f'Failed: {" ".join(self.failed_tests)}'
        return 'All tests pass ✅'

    def report(self):
        print(self.summary)
        print(self.summary_detail)


class MetaSuite(type):
    def __new__(meta, name, bases, class_dict):
        suite = bases[0].suite
        Cls = type.__new__(meta, name, bases, class_dict)

        for key in class_dict:
            if len(re.findall('^test', key)):
                suite.add(Cls(key))

        return Cls


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


class WasSetup(TestCase):
    """
    Sole purpose is for test case that
    ensures error in `setup()` is caught
    """

    def setup(self):
        raise Exception

    def other_method(self):
        pass


class TestCaseTest(TestCase, metaclass=MetaSuite):
    def setup(self):
        self.result = TestResult()

    def test_template_method(self):
        test = WasRun('TEST_METHOD')
        test.run(self.result)
        assert test.log == 'setup TEST_METHOD teardown'

    def test_catch_setup_error(self):
        test = WasSetup('other_method')
        test.run(self.result)
        assert self.result.summary == '1 run, 1 failed'

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

    def test_fail_result_detail(self):
        test = WasRun('TEST_BROKEN_METHOD')
        test.run(self.result)
        assert self.result.summary_detail == 'Failed: TEST_BROKEN_METHOD'

    def test_test_suite(self):
        suite = TestSuite()
        suite.add(WasRun('TEST_METHOD'))
        suite.add(WasRun('TEST_BROKEN_METHOD'))
        suite.run(self.result)
        assert self.result.summary == '2 run, 1 failed'


class Test:
    def run(Cls):
        result = TestResult()
        Cls.suite.run(result)
        result.report()
