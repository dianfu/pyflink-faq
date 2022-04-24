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
from pyflink.common import Types

from test_utils import PyFlinkStreamingTestCase, DataStreamTestSinkFunction


class DataStreamTests(PyFlinkStreamingTestCase):

    def setUp(self) -> None:
        super(DataStreamTests, self).setUp()
        self.test_sink = DataStreamTestSinkFunction()

    def tearDown(self) -> None:
        self.test_sink.clear()

    def assert_equals_sorted(self, expected, actual):
        expected.sort()
        actual.sort()
        self.assertEqual(expected, actual)

    def test_map(self):
        ds = self.env.from_collection([("a", 1), ("b", 2), ("c", 3)],
                                      type_info=Types.ROW([Types.STRING(), Types.INT()]))
        ds.map(lambda x: (x[0], x[1] + 1)) \
          .add_sink(self.test_sink)
        self.env.execute()
        results = self.test_sink.get_results(True)
        expected = ["('a', 2)", "('b', 3)", "('c', 4)"]
        self.assert_equals_sorted(expected, results)
