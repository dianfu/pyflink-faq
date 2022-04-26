################################################################################
#  Licensed to the Apache Software Foundation (ASF) under one
#  or more contributor license agreements.  See the NOTICE file
#  distributed with this work for additional information
#  regarding copyright ownership.  The ASF licenses this file
#  to you under the Apache License, Version 2.0 (the
#  "License"); you may not use this file except in compliance
#  with the License.  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
# limitations under the License.
################################################################################
from pyflink.java_gateway import get_gateway
from pyflink.table import DataTypes
from pyflink.table.udf import udf

from test_utils import PyFlinkStreamTableTestCase, TestAppendSink, results


class TableTests(PyFlinkStreamTableTestCase):

    def get_results(self, table_name):
        gateway = get_gateway()
        TestValuesTableFactory = gateway.jvm.org.apache.flink.table.planner.factories.TestValuesTableFactory
        return TestValuesTableFactory.getResults(table_name)

    def test_scalar_function(self):
        add_one = udf(lambda i: i + 1, result_type=DataTypes.BIGINT())

        table_sink = TestAppendSink(
            ['a', 'b'],
            [DataTypes.BIGINT(), DataTypes.BIGINT()])
        self.t_env.register_table_sink("Results", table_sink)

        t = self.t_env.from_elements([(1, 2, 3), (2, 5, 6), (3, 1, 9)], ['a', 'b', 'c'])
        t.select(t.a, add_one(t.a)) \
            .execute_insert("Results").wait()
        actual = results()
        self.assert_equals(actual, ["+I[1, 2]", "+I[2, 3]", "+I[3, 4]"])

    def test_sink_ddl(self):
        add_one = udf(lambda i: i + 1, result_type=DataTypes.BIGINT())

        self.t_env.execute_sql("""
            CREATE TABLE Results(
                a BIGINT,
                b BIGINT
            ) with (
                'connector' = 'values'
            )
        """)

        t = self.t_env.from_elements([(1, 2, 3), (2, 5, 6), (3, 1, 9)], ['a', 'b', 'c'])
        t.select(t.a, add_one(t.a)) \
            .execute_insert("Results").wait()
        actual = self.get_results("Results")
        self.assert_equals(actual, ["+I[1, 2]", "+I[2, 3]", "+I[3, 4]"])
