class UnitTester:
    """ Object to collect results of unit tests (boolean only for now) and then print() results to stdout """
    def __init__(self):
        self.test_results = []
    def add_result(self,result):
        if type(result) != bool: TypeError
        else: self.test_results.append(result)
    def output(self,reset=False,indent=1):
        if reset:
            if type(reset) is not bool: TypeError
        if len(self.test_results) < 1:
            print('\nNo test results exist!\n')
        elif self.test_results.count(True) != len(self.test_results):
            print('\n{} of {} tests successful'.format(self.test_results.count(True),len(self.test_results)))
            print('\nSome tests failed, here are the results:\n')
            out_string = [' '*4*indent + 'test {} status: {}'.format(idx+1,'OK' if value is True else 'FAIL') for idx,value in enumerate(self.test_results)]
            print('\n'.join(out_string) + '\n')
        else:
            print('\nAll of {} tests successful\n'.format(len(self.test_results)))
        if reset is True: self.__init__()
