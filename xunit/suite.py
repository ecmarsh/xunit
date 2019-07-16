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
        """Default if subclass does not shadow"""
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


class Test:
    suites = {}

    def addSuite(k, v):
        Test.suites[k] = v

    def run():
        """
        Driver to run and report all
        registered suites in `tests.py`
        """
        for suite_name, suite in Test.suites.items():
            result = TestResult()
            suite.run(result)
            print('------------------------')
            print(f'{suite_name} Results:')
            result.report()
            print('------------------------')


class Suite(type):
    def __new__(meta, name, bases, class_dict):
        """
        Adds all method names starting with test to the
        test suite so they can be run collectively.

        usage: `class ClassWithTests(TestCase, metaclass=Suite)`
        """

        suite = bases[0].suite
        Cls = type.__new__(meta, name, bases, class_dict)

        for key in class_dict:
            if len(re.findall('^test', key)):
                suite.add(Cls(key))

        Test.addSuite(name, suite)

        return Cls
