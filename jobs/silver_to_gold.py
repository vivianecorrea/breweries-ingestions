from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count


class GoldLayerAggregator:
    def __init__(self, spark: SparkSession, input_path: str, output_path: str):
        self.spark = spark
        self.input_path = input_path
        self.output_path = output_path

    def read_data(self):
        return self.spark.read.format("delta").load(self.input_path)

    def aggregate_data(self, df):
        return (df.groupBy("state_partition", "city_partition", "brewery_type")
                .agg(count("*").alias("brewery_count")))

    def write_data(self, df):
        (df.write
           .format("delta")
           .mode("overwrite")
           .save(self.output_path))

    def process(self):
        df = self.read_data()
        df_aggregated = self.aggregate_data(df)
        self.write_data(df_aggregated)


if __name__ == "__main__":
    spark = (SparkSession.builder
             .appName("GoldLayerAggregator")
             .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
             .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
             .getOrCreate())

    aggregator = GoldLayerAggregator(
        spark,
        input_path="s3://meu-bucket/silver/breweries/",
        output_path="s3://meu-bucket/gold/breweries_aggregated/"
    )

    aggregator.process()
    spark.stop()