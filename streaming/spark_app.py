"""
    This Spark app connects to the data source script running in another Docker container on port 9999, which provides a stream of random integers.
    The data stream is read and processed by this spark app, where multiples of 9 are identified, and statistics are sent to a dashboard for visualization.
    Both apps are designed to be run in Docker containers.

    Made for: EECS 4415 - Big Data Systems (Department of Electrical Engineering and Computer Science, York University)
    Author: Changyuan Lin
"""


import sys
import requests
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import Row, SparkSession

def aggregate_count(new_values, total_sum):
	return sum(new_values) + (total_sum or 0)

def get_sql_context_instance(spark_context):
    if('sqlContextSingletonInstance' not in globals()):
        globals()['sqlContextSingletonInstance'] = SparkSession(spark_context)
    return globals()['sqlContextSingletonInstance']

def send_df_to_dashboard(df):
    url = 'http://webapp:5000/updateData'
    data = df.toPandas().to_dict('list')
    requests.post(url, json=data)

def send_df_to_dashboardcha(df):
    url = 'http://webapp:5000/push_change'
    datacha = df.toPandas().to_dict('list')
    requests.post(url, json=datacha)

def send_df_to_dashboardstar(df):
    url = 'http://webapp:5000/star_avg'
    datastar = df.toPandas().to_dict('list')
    requests.post(url, json=datastar)

def send_df_to_dashboard1(df):
    url = 'http://webapp:5000/Pythonword'
    data1 = df.toPandas().to_dict('list')
    requests.post(url, json=data1)

def send_df_to_dashboard2(df):
    url = 'http://webapp:5000/Csharpword'
    data2 = df.toPandas().to_dict('list')
    requests.post(url, json=data2)

def send_df_to_dashboard3(df):
    url = 'http://webapp:5000/Javaword'
    data3 = df.toPandas().to_dict('list')
    requests.post(url, json=data3)


def process_rdd(time, rdd):
    pass
    print("----------- %s -----------" % str(time))
    try:
        sql_context = get_sql_context_instance(rdd.context)
        row_rdd = rdd.map(lambda w: Row(language=w[0], count=w[1]))
        results_df = sql_context.createDataFrame(row_rdd)
        results_df.createOrReplaceTempView("results")
        new_results_df = sql_context.sql("select language, count from results order by count")
        new_results_df.show()
        send_df_to_dashboard(new_results_df)
    except ValueError:
        print("Waiting for data...")
    except:
        e = sys.exc_info()[0]
        print("Error: %s" % e)

def process_rddPY(time, rdd):
    pass
    print("----------- %s -----------" % str(time))
    try:
        sql_context = get_sql_context_instance(rdd.context)
        row_rdd = rdd.map(lambda w: Row(Pythonwords=w[0], count=w[1]))
        results_df = sql_context.createDataFrame(row_rdd)
        results_df.createOrReplaceTempView("results")
        new_results_df = sql_context.sql("select Pythonwords, count from results order by count DESC")
        new_results_df.show(10)
        send_df_to_dashboard1(new_results_df)
    except ValueError:
        print("Waiting for data...")
    except:
        e = sys.exc_info()[0]
        print("Error: %s" % e)

def process_rddCS(time, rdd):
    pass
    print("----------- %s -----------" % str(time))
    try:
        sql_context = get_sql_context_instance(rdd.context)
        row_rdd = rdd.map(lambda w: Row(CSharpwords=w[0], count=w[1]))
        results_df = sql_context.createDataFrame(row_rdd)
        results_df.createOrReplaceTempView("results")
        new_results_df = sql_context.sql("select CSharpwords, count from results order by count DESC")
        new_results_df.show(10)
        send_df_to_dashboard2(new_results_df)
    except ValueError:
        print("Waiting for data...")
    except:
        e = sys.exc_info()[0]
        print("Error: %s" % e)

def process_rddJA(time, rdd):
    pass
    print("----------- %s -----------" % str(time))
    try:
        sql_context = get_sql_context_instance(rdd.context)
        row_rdd = rdd.map(lambda w: Row(Javawords=w[0], count=w[1]))
        results_df = sql_context.createDataFrame(row_rdd)
        results_df.createOrReplaceTempView("results")
        new_results_df = sql_context.sql("select Javawords, count from results order by count DESC")
        new_results_df.show(10)
        send_df_to_dashboard3(new_results_df)
    except ValueError:
        print("Waiting for data...")
    except:
        e = sys.exc_info()[0]
        print("Error: %s" % e)

def process_rddstar(time, rdd):
    pass
    print("----------- %s -----------" % str(time))
    try:
        sql_context = get_sql_context_instance(rdd.context)
        row_rdd = rdd.map(lambda w: Row(language=w[0], star_average=w[1]))
        results_df = sql_context.createDataFrame(row_rdd)
        results_df.createOrReplaceTempView("results")
        new_results_df = sql_context.sql("select language, star_average from results")
        new_results_df.show()
        send_df_to_dashboardstar(new_results_df)
    except ValueError:
        print("Waiting for data...")
    except:
        e = sys.exc_info()[0]
        print("Error: %s" % e)

def process_rddcha(time, rdd):
    pass
    print("----------- %s -----------" % str(time))
    try:
        sql_context = get_sql_context_instance(rdd.context)
        row_rdd = rdd.map(lambda w: Row(language=w[0], count=w[1], C_time = str(time)[11:]))
        results_df = sql_context.createDataFrame(row_rdd)
        results_df.createOrReplaceTempView("results")
        new_results_df = sql_context.sql("select language, count, C_time from results order by count")
        new_results_df.show()
        send_df_to_dashboardcha(new_results_df)
    except ValueError:
        print("Waiting for data...")
    except:
        e = sys.exc_info()[0]
        print("Error: %s" % e)


def aggregate_avg(value):
    return ((value[0] + value[0], value[1] + value[1])) 
	 
# docker exec e60261a446ee spark-submit /streaming/spark_app.py
if __name__ == "__main__":
    DATA_SOURCE_IP = "data-source"
    DATA_SOURCE_PORT = 9999
    sc = SparkContext(appName="NineMultiples")
    sc.setLogLevel("ERROR")
    ssc = StreamingContext(sc, 60)
    ssc.checkpoint("checkpoint_NineMultiples")
    data = ssc.socketTextStream(DATA_SOURCE_IP, DATA_SOURCE_PORT)
    numbers = data.flatMap(lambda num: [tuple(map(str,num.split(",")))])
    lang = numbers.map(lambda num:((num[0]), 1)).reduceByKey(lambda x,y:x+y)
    lang1 = numbers.map(lambda num:((num[0]), 1)).reduceByKey(lambda x,y:x+y).mapValues(lambda x : 150 - x)
    avg = numbers.map(lambda num:((num[0]), (int(num[1]), 1))).reduceByKey(lambda x,y: (x[0] + y[0], x[1] + y[1])).mapValues(lambda x: x[0]/x[1])
    py = numbers.filter(lambda x: x[0] == "Python").filter(lambda x: x[2] != " ").flatMap(lambda x: x[2].split(" ")).map(lambda x:(x, 1)).reduceByKey(lambda x,y:x+y).filter(lambda x: x[0] != "")
    cs = numbers.filter(lambda x: x[0] == "C#").filter(lambda x: x[2] != " ").flatMap(lambda x: x[2].split(" ")).map(lambda x:(x, 1)).reduceByKey(lambda x,y:x+y).filter(lambda x: x[0] != "")
    ja = numbers.filter(lambda x: x[0] == "Java").filter(lambda x: x[2] != " ").flatMap(lambda x: x[2].split(" ")).map(lambda x:(x, 1)).reduceByKey(lambda x,y:x+y).filter(lambda x: x[0] != "")
    aggregated_counts = lang.updateStateByKey(aggregate_count)
    aggregated_counts.foreachRDD(process_rdd)
    lang1.foreachRDD(process_rddcha)
    avg.foreachRDD(process_rddstar)
    aggregated_counts1 = py.updateStateByKey(aggregate_count)
    aggregated_counts1.foreachRDD(process_rddPY)
    aggregated_counts2 = cs.updateStateByKey(aggregate_count)
    aggregated_counts2.foreachRDD(process_rddCS)
    aggregated_counts3 = ja.updateStateByKey(aggregate_count)
    aggregated_counts3.foreachRDD(process_rddJA)
    ssc.start()
    ssc.awaitTermination()
