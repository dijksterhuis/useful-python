class UnitTester:
    """ Object to collect results of unit tests (boolean only for now) and then print() results to stdout """
    def __init__(self):
        self.test_results = []
    def add_result(self,result):
        assert type(result) is bool,'Wrong input type for result arg in UnitTester.add_result() - must be type bool'
        self.test_results.append(result)
    def output(self,reset=False,indent=1):
        assert type(reset) is bool,'Wrong input type for reset arg in UnitTester.output() - must be type bool'
        assert type(indent) is int,'Wrong input type for indent arg in UnitTester.output() - must be type int'
        if len(self.test_results) < 1:
            print('\nNo test results exist!\n')
        elif self.test_results.count(True) != len(self.test_results):
            # (True tests, test count, % success)
            t = ( self.test_results.count(True) , len(self.test_results) ,  int(self.test_results.count(True)/len(self.test_results) * 100) )
            print('\n{} of {} ({}%) tests successful'.format(*t))
            print('\nTest results:\n')
            out_string = [' '*4*indent + 'test {} status: {}'.format(idx+1,'OK' if value is True else 'FAIL') for idx,value in enumerate(self.test_results)]
            print('\n'.join(out_string) + '\n')
        else:
            print('\nAll of {} tests successful\n'.format(len(self.test_results)))
            if reset is True: self.__init__()
