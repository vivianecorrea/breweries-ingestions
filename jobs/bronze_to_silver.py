from pyspark.sql import SparkSession
from pyspark.sql.functions import col


class SilverLayerProcessor:
    def __init__(self, spark: SparkSession, input_path: str, output_path: str):
        self.spark = spark
        self.input_path = input_path
        self.output_path = output_path

    def read_data(self):
        return self.spark.read.json(self.input_path)

    def transform_data(self, df): # facilitate users filters
        return (df
                .filter(col("state").isNotNull() & col("city").isNotNull())
                .withColumnRenamed("state", "state_partition")
                .withColumnRenamed("city", "city_partition"))

    def write_data(self, df):
        df.write.mode("overwrite").partitionBy("state_partition", "city_partition").parquet(self.output_path)

    def process(self):
        df = self.read_data()
        df_transformed = self.transform_data(df)
        self.write_data(df_transformed)


if __name__ == "__main__":
    spark = SparkSession.builder.appName("SilverLayerProcessor").getOrCreate()

    processor = SilverLayerProcessor(
        spark,
        input_path="s3://meu-bucket/raw/breweries.json",
        output_path="s3://meu-bucket/silver/breweries/"
    )

    processor.process()
    spark.stop()