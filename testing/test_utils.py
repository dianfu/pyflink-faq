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
import glob
import os
import pickle
import shutil
import tempfile
import unittest
from subprocess import check_output

from py4j.java_gateway import JavaObject
from pyflink import pyflink_gateway_server
from pyflink.datastream import StreamExecutionEnvironment, RuntimeExecutionMode, SinkFunction
from pyflink.find_flink_home import _find_flink_home
from pyflink.java_gateway import get_gateway
from pyflink.pyflink_gateway_server import on_windows
from pyflink.table import TableEnvironment, EnvironmentSettings
from pyflink.util.java_utils import is_instance_of


class PyFlinkTestCase(unittest.TestCase):
    """
    Base class for unit tests.
    """

    @classmethod
    def setUpClass(cls):
        cls.tempdir = tempfile.mkdtemp()

        os.environ['_python_worker_execution_mode'] = "process"
        os.environ["FLINK_TESTING"] = "1"
        _find_flink_home()

        print("Using %s as FLINK_HOME...", os.environ["FLINK_HOME"])

        testing_jars = [("org.apache.flink", "flink-python", "1.16.1", "tests")]
        download_testing_jars(testing_jars)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tempdir, ignore_errors=True)
        del os.environ['_python_worker_execution_mode']

    @classmethod
    def assert_equals(cls, actual, expected):
        if isinstance(actual, JavaObject):
            actual_py_list = cls.to_py_list(actual)
        else:
            actual_py_list = actual
        actual_py_list.sort()
        expected.sort()
        assert len(actual_py_list) == len(expected)
        assert all(x == y for x, y in zip(actual_py_list, expected))

    @classmethod
    def to_py_list(cls, actual):
        py_list = []

        is_list = is_instance_of(actual, get_gateway().jvm.java.util.List)
        if is_list:
            for i in range(0, actual.size()):
                py_list.append(actual.get(i))
        else:
            for i in range(0, actual.length()):
                py_list.append(actual.apply(i))
        return py_list


def download_testing_jars(testing_jars):
    output_dir = os.path.abspath(os.path.dirname(__file__))
    mvn = "mvn.cmd" if on_windows() else "mvn"
    for group_id, artifact_id, version, classifier in testing_jars:
        artifact = "%s:%s:%s:jar" % (group_id, artifact_id, version)

        test_jar_file_name = "%s-%s" % (artifact_id, version)
        if classifier:
            artifact = "%s:%s" % (artifact, classifier)
            test_jar_file_name = "%s-%s" % (test_jar_file_name, classifier)
        test_jar_file = "%s.jar" % test_jar_file_name

        if glob.glob(os.path.join(output_dir, test_jar_file)):
            print("Skipped download %s since it already exists." % os.path.join(output_dir, test_jar_file))
        else:
            print("Downloading jar %s" % artifact)
            check_output(
                [mvn,
                 "org.apache.maven.plugins:maven-dependency-plugin:2.10:copy",
                 "-Dartifact=%s" % artifact,
                 "-DoutputDirectory=%s" % output_dir],
                cwd=output_dir)


def construct_test_classpath():
    output_dir = os.path.abspath(os.path.dirname(__file__))
    test_jars = glob.glob(os.path.join(output_dir, "*.jar"))
    return os.path.pathsep.join(test_jars)


pyflink_gateway_server.construct_test_classpath = construct_test_classpath


###################### Test utilities for Table API & SQL ######################


class PyFlinkStreamTableTestCase(PyFlinkTestCase):
    """
    Base class for table stream tests.
    """

    def setUp(self):
        super(PyFlinkStreamTableTestCase, self).setUp()
        self.t_env = TableEnvironment.create(EnvironmentSettings.in_streaming_mode())

    @staticmethod
    def get_results():
        """
        Retrieves the results from a retract table sink.
        """
        gateway = get_gateway()
        results = gateway.jvm.org.apache.flink.table.utils.TestingSinks.RowCollector.getAndClearValues()
        return gateway.jvm\
            .org.apache.flink.table.utils.TestingSinks.RowCollector.retractResults(results)


###################### Test utilities for DataStream API ######################


class PyFlinkStreamingTestCase(PyFlinkTestCase):
    """
    Base class for streaming tests.
    """

    def setUp(self):
        super(PyFlinkStreamingTestCase, self).setUp()
        self.env = StreamExecutionEnvironment.get_execution_environment()
        self.env.set_runtime_mode(RuntimeExecutionMode.STREAMING)


class DataStreamTestSinkFunction(SinkFunction):
    """
    A util class to collect test DataStream transformation results.
    """

    def __init__(self):
        self.j_data_stream_collect_sink = get_gateway().jvm \
            .org.apache.flink.python.util.DataStreamTestCollectSink()
        super(DataStreamTestSinkFunction, self).__init__(sink_func=self.j_data_stream_collect_sink)

    def get_results(self, is_python_object: bool = False):
        j_results = self.get_java_function().collectAndClear(is_python_object)
        results = list(j_results)
        if not is_python_object:
            return results
        else:
            str_results = []
            for result in results:
                pickled_result = pickle.loads(result)
                str_results.append(str(pickled_result))
            return str_results

    def clear(self):
        if self.j_data_stream_collect_sink is None:
            return
        self.j_data_stream_collect_sink.clear()
