# pyflink-faq
Frequently Asked Questions around PyFlink.

# Frequently Asked Questions

## JDK issues:

Q1: [InaccessibleObjectException: Unable to make field private final byte[] java.lang.String.value accessible: module java.base does not "opens java.lang" to unnamed module @4e4aea35](#q1-inaccessibleobjectexception-unable-to-make-field-private-final-byte-javalangstringvalue-accessible-module-javabase-does-not-opens-javalang-to-unnamed-module-4e4aea35)

## Connector issues:

Q1: [Could not find any factory for identifier 'xxx' that implements 'org.apache.flink.table.factories.DynamicTableFactory' in the classpath](#q1-could-not-find-any-factory-for-identifier-xxx-that-implements-orgapacheflinktablefactoriesdynamictablefactory-in-the-classpath)

Q2: [ClassNotFoundException: com.mysql.cj.jdbc.Driver](#q2-classnotfoundexception-commysqlcjjdbcdriver)

Q3: [NoSuchMethodError: org.apache.flink.table.factories.DynamicTableFactory$Context.getCatalogTable()Lorg/apache/flink/table/catalog/CatalogTable](#q3-nosuchmethoderror-orgapacheflinktablefactoriesdynamictablefactorycontextgetcatalogtablelorgapacheflinktablecatalogcatalogtable)

## Runtime issues:

Q1: [OverflowError: timeout value is too large](#q1-overflowerror-timeout-value-is-too-large)

Q2: [An error occurred while calling z:org.apache.flink.client.python.PythonEnvUtils.resetCallbackClient](#q2-an-error-occurred-while-calling-zorgapacheflinkclientpythonpythonenvutilsresetcallbackclient)

# JDK issues

## Q1: InaccessibleObjectException: Unable to make field private final byte[] java.lang.String.value accessible: module java.base does not "opens java.lang" to unnamed module @4e4aea35

```
: java.lang.reflect.InaccessibleObjectException: Unable to make field private final byte[] java.lang.String.value accessible: module java.base does not "opens java.lang" to unnamed module @4e4aea35
	at java.base/java.lang.reflect.AccessibleObject.checkCanSetAccessible(AccessibleObject.java:354)
	at java.base/java.lang.reflect.AccessibleObject.checkCanSetAccessible(AccessibleObject.java:297)
	at java.base/java.lang.reflect.Field.checkCanSetAccessible(Field.java:178)
	at java.base/java.lang.reflect.Field.setAccessible(Field.java:172)
	at org.apache.flink.api.java.ClosureCleaner.clean(ClosureCleaner.java:106)
	at org.apache.flink.api.java.ClosureCleaner.clean(ClosureCleaner.java:132)
	at org.apache.flink.api.java.ClosureCleaner.clean(ClosureCleaner.java:132)
	at org.apache.flink.api.java.ClosureCleaner.clean(ClosureCleaner.java:132)
	at org.apache.flink.api.java.ClosureCleaner.clean(ClosureCleaner.java:132)
	at org.apache.flink.api.java.ClosureCleaner.clean(ClosureCleaner.java:69)
	at org.apache.flink.streaming.api.environment.StreamExecutionEnvironment.clean(StreamExecutionEnvironment.java:2138)
	at org.apache.flink.table.planner.plan.nodes.exec.common.CommonExecSink.createSinkFunctionTransformation(CommonExecSink.java:331)
	at org.apache.flink.table.planner.plan.nodes.exec.common.CommonExecSink.applySinkProvider(CommonExecSink.java:306)
	at org.apache.flink.table.planner.plan.nodes.exec.common.CommonExecSink.createSinkTransformation(CommonExecSink.java:146)
	at org.apache.flink.table.planner.plan.nodes.exec.stream.StreamExecSink.translateToPlanInternal(StreamExecSink.java:140)
	at org.apache.flink.table.planner.plan.nodes.exec.ExecNodeBase.translateToPlan(ExecNodeBase.java:134)
```

This is an issue around Java 17. It still doesn't support Java 17 in Flink. You can refer to [FLINK-15736]( https://issues.apache.org/jira/browse/FLINK-15736) for more details. To solve this issue, you need to use JDK 1.8 or JDK 11.


# Connector issues

## Q1: Could not find any factory for identifier 'xxx' that implements 'org.apache.flink.table.factories.DynamicTableFactory' in the classpath.

Exception Stack:
```
py4j.protocol.Py4JJavaError: An error occurred while calling o13.execute.
: org.apache.flink.table.api.ValidationException: Unable to create a source for reading table 'default_catalog.default_database.sourceKafka'.

Table options are:

'connector'='kafka'
'format'='json'
'properties.bootstrap.servers'='192.168.101.109:9092'
'scan.startup.mode'='earliest-offset'
'topic'='pyflink_test'
	at org.apache.flink.table.factories.FactoryUtil.createTableSource(FactoryUtil.java:150)
	at org.apache.flink.table.planner.plan.schema.CatalogSourceTable.createDynamicTableSource(CatalogSourceTable.java:116)
	at org.apache.flink.table.planner.plan.schema.CatalogSourceTable.toRel(CatalogSourceTable.java:82)
	at org.apache.calcite.rel.core.RelFactories$TableScanFactoryImpl.createScan(RelFactories.java:495)
	at org.apache.calcite.tools.RelBuilder.scan(RelBuilder.java:1099)
	at org.apache.calcite.tools.RelBuilder.scan(RelBuilder.java:1123)
	at org.apache.flink.table.planner.plan.QueryOperationConverter$SingleRelVisitor.visit(QueryOperationConverter.java:351)
	at org.apache.flink.table.planner.plan.QueryOperationConverter$SingleRelVisitor.visit(QueryOperationConverter.java:154)
	at org.apache.flink.table.operations.CatalogQueryOperation.accept(CatalogQueryOperation.java:68)
	at org.apache.flink.table.planner.plan.QueryOperationConverter.defaultMethod(QueryOperationConverter.java:151)
	at org.apache.flink.table.planner.plan.QueryOperationConverter.defaultMethod(QueryOperationConverter.java:133)
	at org.apache.flink.table.operations.utils.QueryOperationDefaultVisitor.visit(QueryOperationDefaultVisitor.java:92)
	at org.apache.flink.table.operations.CatalogQueryOperation.accept(CatalogQueryOperation.java:68)
	at org.apache.flink.table.planner.plan.QueryOperationConverter.lambda$defaultMethod$0(QueryOperationConverter.java:150)
	at java.util.Collections$SingletonList.forEach(Collections.java:4824)
	at org.apache.flink.table.planner.plan.QueryOperationConverter.defaultMethod(QueryOperationConverter.java:150)
	at org.apache.flink.table.planner.plan.QueryOperationConverter.defaultMethod(QueryOperationConverter.java:133)
	at org.apache.flink.table.operations.utils.QueryOperationDefaultVisitor.visit(QueryOperationDefaultVisitor.java:47)
	at org.apache.flink.table.operations.ProjectQueryOperation.accept(ProjectQueryOperation.java:76)
	at org.apache.flink.table.planner.calcite.FlinkRelBuilder.queryOperation(FlinkRelBuilder.scala:184)
	at org.apache.flink.table.planner.delegation.PlannerBase.translateToRel(PlannerBase.scala:219)
	at org.apache.flink.table.planner.delegation.PlannerBase$$anonfun$1.apply(PlannerBase.scala:182)
	at org.apache.flink.table.planner.delegation.PlannerBase$$anonfun$1.apply(PlannerBase.scala:182)
	at scala.collection.TraversableLike$$anonfun$map$1.apply(TraversableLike.scala:234)
	at scala.collection.TraversableLike$$anonfun$map$1.apply(TraversableLike.scala:234)
	at scala.collection.Iterator$class.foreach(Iterator.scala:891)
	at scala.collection.AbstractIterator.foreach(Iterator.scala:1334)
	at scala.collection.IterableLike$class.foreach(IterableLike.scala:72)
	at scala.collection.AbstractIterable.foreach(Iterable.scala:54)
	at scala.collection.TraversableLike$class.map(TraversableLike.scala:234)
	at scala.collection.AbstractTraversable.map(Traversable.scala:104)
	at org.apache.flink.table.planner.delegation.PlannerBase.translate(PlannerBase.scala:182)
	at org.apache.flink.table.api.internal.TableEnvironmentImpl.translate(TableEnvironmentImpl.java:1665)
	at org.apache.flink.table.api.internal.TableEnvironmentImpl.translateAndClearBuffer(TableEnvironmentImpl.java:1657)
	at org.apache.flink.table.api.internal.TableEnvironmentImpl.execute(TableEnvironmentImpl.java:1607)
	at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
	at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
	at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
	at java.lang.reflect.Method.invoke(Method.java:498)
	at org.apache.flink.api.python.shaded.py4j.reflection.MethodInvoker.invoke(MethodInvoker.java:244)
	at org.apache.flink.api.python.shaded.py4j.reflection.ReflectionEngine.invoke(ReflectionEngine.java:357)
	at org.apache.flink.api.python.shaded.py4j.Gateway.invoke(Gateway.java:282)
	at org.apache.flink.api.python.shaded.py4j.commands.AbstractCommand.invokeMethod(AbstractCommand.java:132)
	at org.apache.flink.api.python.shaded.py4j.commands.CallCommand.execute(CallCommand.java:79)
	at org.apache.flink.api.python.shaded.py4j.GatewayConnection.run(GatewayConnection.java:238)
	at java.lang.Thread.run(Thread.java:748)
Caused by: org.apache.flink.table.api.ValidationException: Cannot discover a connector using option: 'connector'='kafka'
	at org.apache.flink.table.factories.FactoryUtil.enrichNoMatchingConnectorError(FactoryUtil.java:587)
	at org.apache.flink.table.factories.FactoryUtil.getDynamicTableFactory(FactoryUtil.java:561)
	at org.apache.flink.table.factories.FactoryUtil.createTableSource(FactoryUtil.java:146)
	... 45 more
Caused by: org.apache.flink.table.api.ValidationException: Could not find any factory for identifier 'kafka' that implements 'org.apache.flink.table.factories.DynamicTableFactory' in the classpath.

Available factory identifiers are:

blackhole
datagen
filesystem
print
	at org.apache.flink.table.factories.FactoryUtil.discoverFactory(FactoryUtil.java:399)
	at org.apache.flink.table.factories.FactoryUtil.enrichNoMatchingConnectorError(FactoryUtil.java:583)
	... 47 more
```

It reuses the Java connectors implementations in PyFlink and most connectors are not bundled in the official PyFlink (and also Flink) distribution except the following connectors: blackhole, datagen, filesystem and print. So you need to specify the connector JAR package explicitly when executing PyFlink jobs:
- The connector JAR package could be found in the corresponding connector page in the official Flink documentation. For example, you can open the [Kafka connector page](https://nightlies.apache.org/flink/flink-docs-stable/docs/connectors/table/kafka/) and search keyword "SQL Client JAR" which is a fat JAR of Kafka connector.
- It should be noted that you should use the fat JAR which contains all the dependencies. Besides, the version of the connector JAR should be consistent with PyFlink version. 
- For how to specify the connector JAR in PyFlink jobs, you can refer to the [dependency management](https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/python/dependency_management/#jar-dependencies) page of official PyFlink documentation.

## Q2: ClassNotFoundException: com.mysql.cj.jdbc.Driver

```
py4j.protocol.Py4JJavaError: An error occurred while calling o13.execute.
: org.apache.flink.runtime.client.JobExecutionException: Job execution failed.
...
Caused by: java.io.IOException: unable to open JDBC writer
	at org.apache.flink.connector.jdbc.internal.JdbcOutputFormat.open(JdbcOutputFormat.java:145)
	at org.apache.flink.connector.jdbc.internal.GenericJdbcSinkFunction.open(GenericJdbcSinkFunction.java:52)
	at org.apache.flink.api.common.functions.util.FunctionUtils.openFunction(FunctionUtils.java:34)
	at org.apache.flink.streaming.api.operators.AbstractUdfStreamOperator.open(AbstractUdfStreamOperator.java:100)
	at org.apache.flink.streaming.api.operators.StreamSink.open(StreamSink.java:46)
	at org.apache.flink.streaming.runtime.tasks.RegularOperatorChain.initializeStateAndOpenOperators(RegularOperatorChain.java:110)
	at org.apache.flink.streaming.runtime.tasks.StreamTask.restoreGates(StreamTask.java:711)
	at org.apache.flink.streaming.runtime.tasks.StreamTaskActionExecutor$1.call(StreamTaskActionExecutor.java:55)
	at org.apache.flink.streaming.runtime.tasks.StreamTask.restoreInternal(StreamTask.java:687)
	at org.apache.flink.streaming.runtime.tasks.StreamTask.restore(StreamTask.java:654)
	at org.apache.flink.runtime.taskmanager.Task.runWithSystemExitMonitoring(Task.java:958)
	at org.apache.flink.runtime.taskmanager.Task.restoreAndInvoke(Task.java:927)
	at org.apache.flink.runtime.taskmanager.Task.doRun(Task.java:766)
	at org.apache.flink.runtime.taskmanager.Task.run(Task.java:575)
	at java.lang.Thread.run(Thread.java:748)
Caused by: java.lang.ClassNotFoundException: com.mysql.cj.jdbc.Driver
	at java.net.URLClassLoader.findClass(URLClassLoader.java:382)
	at java.lang.ClassLoader.loadClass(ClassLoader.java:418)
	at org.apache.flink.util.FlinkUserCodeClassLoader.loadClassWithoutExceptionHandling(FlinkUserCodeClassLoader.java:64)
	at org.apache.flink.util.ChildFirstClassLoader.loadClassWithoutExceptionHandling(ChildFirstClassLoader.java:74)
	at org.apache.flink.util.FlinkUserCodeClassLoader.loadClass(FlinkUserCodeClassLoader.java:48)
	at java.lang.ClassLoader.loadClass(ClassLoader.java:351)
	at org.apache.flink.runtime.execution.librarycache.FlinkUserCodeClassLoaders$SafetyNetWrapperClassLoader.loadClass(FlinkUserCodeClassLoaders.java:172)
	at java.lang.Class.forName0(Native Method)
	at java.lang.Class.forName(Class.java:348)
	at org.apache.flink.connector.jdbc.internal.connection.SimpleJdbcConnectionProvider.loadDriver(SimpleJdbcConnectionProvider.java:90)
	at org.apache.flink.connector.jdbc.internal.connection.SimpleJdbcConnectionProvider.getLoadedDriver(SimpleJdbcConnectionProvider.java:100)
	at org.apache.flink.connector.jdbc.internal.connection.SimpleJdbcConnectionProvider.getOrEstablishConnection(SimpleJdbcConnectionProvider.java:117)
	at org.apache.flink.connector.jdbc.internal.JdbcOutputFormat.open(JdbcOutputFormat.java:143)
```

This indicates that it the JDBC driver JAR package is missing. It should be noted that the JDBC driver is also required when using JDBC connector. The JAR packages of the JDBC drivers could be found in the [JDBC connector page](https://nightlies.apache.org/flink/flink-docs-stable/docs/connectors/table/jdbc/).

## Q3: NoSuchMethodError: org.apache.flink.table.factories.DynamicTableFactory$Context.getCatalogTable()Lorg/apache/flink/table/catalog/CatalogTable

```
java.lang.NoSuchMethodError: org.apache.flink.table.factories.DynamicTableFactory$Context.getCatalogTable()Lorg/apache/flink/table/catalog/CatalogTable;
    at org.apache.flink.streaming.connectors.kafka.table.KafkaDynamicTableFactory.createDynamicTableSource(KafkaDynamicTableFactory.java:145)
    at org.apache.flink.table.factories.FactoryUtil.createTableSource(FactoryUtil.java:147)
    ... 39 more
```

It indicates that the version of the Kafka connector JAR package isn't consistent with the PyFlink version. This is the same case for all connectors. You need to make sure that the connector version is consistent with the PyFlink version.

# Runtime issues

## Q1: OverflowError: timeout value is too large

```
File "D:\Anaconda3\envs\py37\lib\threading.py", line 926, in _bootstrap_inner
	self.run()
File "D:\Anaconda3\envs\py37\lib\site-packages\apache_beam\runners\worker\data_plane.py", line 218, in run
	while not self._finished.wait(next_call - time.time()):
File "D:\Anaconda3\envs\py37\lib\threading.py", line 552, in wait
	signaled = self._cond.wait(timeout)
File "D:\Anaconda3\envs\py37\lib\threading.py", line 300, in wait
	gotit = waiter.acquire(True, timeout)
OverflowError: timeout value is too large
```

This exception only occurs on Windows. It doesn't affect the execution of PyFlink jobs and so you could ignore it usually. Besides, you could also upgrade PyFlink versions to 1.12.8, 1.13.7, 1.14.4 or 1.15.0 where this issue has been fixed. You could refer to [FLINK-25883]( https://issues.apache.org/jira/browse/FLINK-25883) for more details.

## Q2: An error occurred while calling z:org.apache.flink.client.python.PythonEnvUtils.resetCallbackClient

```
py4j.protocol.Py4jError: An error occurred while calling z:org.apache.flink.client.python.PythonEnvUtils.resetCallbackClient. Trace:
org.apache.flink.api.python.shaded.py4j.Py4jException: Method resetCallbackClient([class java.lang.String, class java.lang.Integer]) does not exist
    at org.apache.flink.api.python.shaded.py4j.reflection.ReflectionEngine.getMethod(ReflectionEngine.java:318)
    ...
```

This exception only occurs when the version of the flink-python jar (located in site-packages/pyflink/opt) isn't consistent with PyFlink version. It usually happens when you have tried to install multiple PyFlink versions and something wrong happens which make multiple versions mixed in your environment. You can try to reinstall PyFlink in a clean environment.
