import glob

import csv

from Test_Framework_Klenitskaya.test import CSVfile, TEXTfile, accessfile


class TestProcessor:
    def __init__(self, config, connector, logger):
        self.config = config
        self.connector = connector
        self.logger = logger

    def process(self):
        test_data_files = self.check_test_folder()

        for f in test_data_files:
            self.do_testing(f)

    def check_test_folder(self):
        test_data_folder = self.config.get_test_data_folder()
        return [f for f in glob.glob(test_data_folder + 'smoke_tests.json', recursive=True)]

    def do_testing(self, file_name):
        self.logger.start_test(file_name)

        with open(file_name) as f:
            test_data = eval(f.read())

        for test in test_data['tests']:
            self.logger.start_case(test['name'])

            query = test['query']
            expected_result = test['expected']
            actual_result = self.connector.execute(query)

            if actual_result == expected_result:
                self.logger.add_pass(query, actual_result)
            else:
                self.logger.add_fail(query, actual_result, expected_result)

    def process_tables(self):
        test_data_files = self.check_test_folder()

        for f in test_data_files:
            self.compare_table_with_sorce(f)

    def check_test_folder(self):
        test_data_folder = self.config.get_test_data_folder()
        return [f for f in glob.glob(test_data_folder + 'compare_tables_queries.json', recursive=True)]

    def compare_table_with_sorce(self, file_name):
        self.logger.start_test(file_name)

        with open(CSVfile) as csv_file:
            reader = csv.DictReader(csv_file, delimiter=',')
            for row in reader:
                csv_data = {row['п»їregion_id'], row['region_name']}
                diff = sorted(csv_data.difference(accessfile))
                print(diff)
            with open(TEXTfile, 'w') as result:
                for missing in diff:
                    print(missing)
                    result.write("".join(missing))