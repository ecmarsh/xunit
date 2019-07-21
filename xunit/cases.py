# Sample classes to be tested by tests

from .suite import TestCase


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
    def setup(self):
        raise Exception

    def other_method(self):
        pass
