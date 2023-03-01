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
import uuid

from pyflink.table import DataTypes, TableDescriptor, Schema
from pyflink.table.udf import udf

from test_utils import PyFlinkStreamTableTestCase


class TableTests(PyFlinkStreamTableTestCase):

    @staticmethod
    def generate_table_name(prefix="Table"):
        return "{0}_{1}".format(prefix, str(uuid.uuid1()).replace("-", "_"))

    def test_scalar_function(self):
        add_one = udf(lambda i: i + 1, result_type=DataTypes.BIGINT())

        sink_table = self.generate_table_name("Result")
        self.t_env.execute_sql(f"""
            CREATE TABLE {sink_table} (
                a BIGINT,
                b BIGINT
            ) WITH (
                'connector' = 'test-sink'
            )
        """)

        t = self.t_env.from_elements([(1, 2, 3), (2, 5, 6), (3, 1, 9)], ['a', 'b', 'c'])
        t.select(t.a, add_one(t.a)) \
            .execute_insert(sink_table).wait()
        actual = self.get_results()
        self.assert_equals(actual, ["+I[1, 2]", "+I[2, 3]", "+I[3, 4]"])

    def test_scalar_function_using_table_descriptor(self):
        add_one = udf(lambda i: i + 1, result_type=DataTypes.BIGINT())

        sink_table = self.generate_table_name("Result")
        self.t_env.create_table(
            sink_table,
            TableDescriptor.for_connector('test-sink')
                           .schema(Schema
                                   .new_builder()
                                   .column('a', DataTypes.BIGINT())
                                   .column('b', DataTypes.BIGINT())
                                   .build())
                           .build())

        t = self.t_env.from_elements([(1, 2, 3), (2, 5, 6), (3, 1, 9)], ['a', 'b', 'c'])
        t.select(t.a, add_one(t.a)) \
            .execute_insert(sink_table).wait()
        actual = self.get_results()
        self.assert_equals(actual, ["+I[1, 2]", "+I[2, 3]", "+I[3, 4]"])
