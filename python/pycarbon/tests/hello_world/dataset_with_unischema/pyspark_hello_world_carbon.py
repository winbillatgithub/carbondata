# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Minimal example of how to read samples from a dataset generated by `generate_pycarbon_dataset.py`
using pyspark"""

from __future__ import print_function

from pyspark.sql import SparkSession


def pyspark_hello_world(dataset_url='file:///tmp/carbon_pycarbon_dataset'):
  spark = SparkSession \
    .builder \
    .master('local[1]') \
    .getOrCreate()

  dataset_path = dataset_url[7:]
  # Create a dataframe object from carbon files
  spark.sql("create table readcarbon using carbon location '" + str(dataset_path) + "'")
  dataframe = spark.sql("select * from readcarbon")

  # Show a schema
  dataframe.printSchema()

  # Count all
  dataframe.count()

  # Show just some columns
  dataframe.select('id').show()

  # This is how you can use a standard SQL to query a dataset. Note that the data is not decoded in this case.
  number_of_rows = spark.sql(
    'SELECT count(id) '
    'from carbon.`{}` '.format(dataset_url)).collect()
  print('Number of rows in the dataset: {}'.format(number_of_rows[0][0]))


if __name__ == '__main__':
  pyspark_hello_world()
