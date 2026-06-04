from pathlib import Path


def run_spark_file_stream(input_dir: Path, output_dir: Path) -> None:
    from pyspark.sql import SparkSession
    from pyspark.sql.functions import col, to_date
    from pyspark.sql.types import DoubleType, IntegerType, StringType, StructField, StructType, TimestampType

    spark = SparkSession.builder.appName("financial-events-stream").getOrCreate()
    schema = StructType([
        StructField("event_id", StringType()),
        StructField("event_time", TimestampType()),
        StructField("account_id", StringType()),
        StructField("symbol", StringType()),
        StructField("side", StringType()),
        StructField("quantity", IntegerType()),
        StructField("price", DoubleType()),
        StructField("currency", StringType()),
    ])

    raw = spark.readStream.schema(schema).json(str(input_dir))
    clean = (
        raw.dropna(subset=["event_id", "event_time", "account_id", "symbol", "side", "quantity", "price"])
        .filter((col("quantity") > 0) & (col("price") > 0))
        .withColumn("event_date", to_date(col("event_time")))
        .withColumn("amount", col("quantity") * col("price"))
    )

    query = (
        clean.writeStream
        .format("parquet")
        .option("checkpointLocation", str(output_dir / "_checkpoint"))
        .option("path", str(output_dir / "clean_events"))
        .outputMode("append")
        .start()
    )
    query.awaitTermination()
