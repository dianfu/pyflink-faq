It gives a basic example on how to write unit tests in an external project which depends on PyFlink.

You could execute the unit tests according to the following steps:
- Create a Python virtual environment and install PyFlink
```shell
cd testing
python3 -m venv .venv
source .venv/bin/activate
pip install .
```

- Check that PyFlink is installed successfully
```shell
python -c "import pyflink;import os;print(os.path.dirname(os.path.abspath(pyflink.__file__)))"
```

It will print something like the following: 
```shell
/Users/dianfu/code/src/github/pyflink-faq/testing/.venv/lib/python3.8/site-packages/pyflink
```

Execute the following command:
```shell
ls -lh /Users/dianfu/code/src/github/pyflink-faq/testing/.venv/lib/python3.8/site-packages/pyflink/
```

The structure should be as following:
```
total 136
-rw-r--r--   1 dianfu  staff   1.3K Apr 25 09:26 README.txt
-rw-r--r--   1 dianfu  staff   1.9K Apr 25 09:26 __init__.py
drwxr-xr-x  11 dianfu  staff   352B Apr 25 09:26 __pycache__
drwxr-xr-x  25 dianfu  staff   800B Apr 25 09:26 bin
drwxr-xr-x  21 dianfu  staff   672B Apr 25 09:26 common
drwxr-xr-x  13 dianfu  staff   416B Apr 25 09:26 conf
drwxr-xr-x  20 dianfu  staff   640B Apr 25 09:26 datastream
drwxr-xr-x   4 dianfu  staff   128B Apr 25 09:26 examples
-rw-r--r--   1 dianfu  staff   3.2K Apr 25 09:26 find_flink_home.py
drwxr-xr-x  25 dianfu  staff   800B Apr 25 09:26 fn_execution
-rw-r--r--   1 dianfu  staff   9.1K Apr 25 09:26 gen_protos.py
-rw-r--r--   1 dianfu  staff   7.6K Apr 25 09:26 java_gateway.py
drwxr-xr-x  11 dianfu  staff   352B Apr 25 09:26 lib
drwxr-xr-x  28 dianfu  staff   896B Apr 25 09:26 licenses
drwxr-xr-x   4 dianfu  staff   128B Apr 25 09:26 log
drwxr-xr-x   5 dianfu  staff   160B Apr 25 09:26 metrics
drwxr-xr-x   4 dianfu  staff   128B Apr 25 09:26 opt
drwxr-xr-x  11 dianfu  staff   352B Apr 25 09:26 plugins
-rw-r--r--   1 dianfu  staff   1.3K Apr 25 09:26 pyflink_callback_server.py
-rw-r--r--   1 dianfu  staff    12K Apr 25 09:26 pyflink_gateway_server.py
-rw-r--r--   1 dianfu  staff   5.3K Apr 25 09:26 serializers.py
-rw-r--r--   1 dianfu  staff   7.9K Apr 25 09:26 shell.py
drwxr-xr-x  31 dianfu  staff   992B Apr 25 09:26 table
drwxr-xr-x   6 dianfu  staff   192B Apr 25 09:26 util
-rw-r--r--   1 dianfu  staff   1.1K Apr 25 09:26 version.py
```
Please checks whether the directories `lib`, `opt` are available.

- Execute command `python3 -m unittest test_table_api.TableTests.test_scalar_function` to run the unit test

You will see the following output, which means that the test has run successfully:
```
(.venv) (base) dianfu@B-7174MD6R-1908 testing % python3 -m unittest test_table_api.TableTests.test_scalar_function                            
Using %s as FLINK_HOME... /Users/dianfu/code/src/github/pyflink-faq/testing/.venv/lib/python3.7/site-packages/pyflink
Skipped download /Users/dianfu/code/src/github/pyflink-faq/testing/flink-python-1.16.1-tests.jar since it already exists.
/Users/dianfu/opt/miniconda3/lib/python3.7/subprocess.py:883: ResourceWarning: subprocess 27896 is still running
  ResourceWarning, source=self)
ResourceWarning: Enable tracemalloc to get the object allocation traceback
.
----------------------------------------------------------------------
Ran 1 test in 15.313s

OK
```
