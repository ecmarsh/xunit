# The test for the test suite itself

from .suite import TestCase, TestResult, TestSuite, Suite
from .mocks import WasRun, WasSetup


class TestCaseTest(TestCase, metaclass=Suite):
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
