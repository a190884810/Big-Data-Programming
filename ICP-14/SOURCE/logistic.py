from pyspark.sql import SparkSession
from pyspark.sql.functions import col,
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.feature import VectorAssembler
import os
os.environ["SPARK_HOME"] = "C:\\Users\\Niteesha\\Desktop\\spark-2.4.3-bin-hadoop2.7\\spark-2.4.3-bin-hadoop2.7\\"
os.environ["HADOOP_HOME"] = "C:\\winutils\\"
# Create spark session
spark = SparkSession.builder.appName("ICP 14").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

# Define input path
input_path = "/home/Niteesha/Desktop/CS5590_Spark/ICP/14/"

# Load data and select feature and label columns
data = spark.read.format("csv").option("header", True).option("inferSchema", True).option("delimiter", ",").load("C:\\Users\\Niteesha\\Desktop\\data1.csv")
data = data.withColumn("label", when(col("eng") == "front", 1).otherwise(0)).select("label", "len")


# Create vector assembler for feature columns
assembler = VectorAssembler(inputCols=data.columns[1:], outputCol="features")
data = assembler.transform(data)

lr = LogisticRegression(maxIter=10, regParam=0.3, elasticNetParam=0.8)

# Fit the model
model = lr.fit(data)

# Print the coefficients and intercept for logistic regression
print("Coefficients: " + str(model.coefficients))
print("Intercept: " + str(model.intercept))

# We can also use the multinomial family for binary classification
mlr = LogisticRegression(maxIter=10, regParam=0.3, elasticNetParam=0.8, family="multinomial")

# Fit the model
mlr_model = mlr.fit(data)

# Print the coefficients and intercepts for logistic regression with multinomial family
print("Multinomial coefficients: " + str(mlr_model.coefficientMatrix))
print("Multinomial intercepts: " + str(mlr_model.interceptVector))