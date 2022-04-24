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
import logging
import sys

from pyflink.table import EnvironmentSettings, TableEnvironment, TableDescriptor, Schema, DataTypes
from pyflink.table.expressions import lit, col
from pyflink.table.udf import udf

if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(message)s")

    t_env = TableEnvironment.create(EnvironmentSettings.in_streaming_mode())

    # define the source
    t_env.create_temporary_table(
        'source',
        TableDescriptor.for_connector('datagen')
            .schema(Schema.new_builder()
                    .column('word', DataTypes.STRING())
                    .build())
            .option('number-of-rows', '1000000')
            .build())
    tab = t_env.from_path('source')

    # define the sink
    t_env.create_temporary_table(
        'sink',
        TableDescriptor.for_connector('print')
            .schema(Schema.new_builder()
                    .column('word', DataTypes.STRING())
                    .column('count', DataTypes.BIGINT())
                    .build())
            .build())


    @udf(result_type=DataTypes.STRING())
    def normalize(word, start, end):
        return word[start:end]


    # compute word count
    tab.select(normalize(col('word'), 0, 3)).alias("word") \
       .group_by(col('word')) \
       .select(col('word'), lit(1).count) \
       .execute_insert('sink')
