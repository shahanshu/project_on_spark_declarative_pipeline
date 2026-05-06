from pyspark.sql import functions as F
from pyspark import pipelines as dp 


@dp.materialized_view(
    name ="sdp_project.silver.city",
    comment="Cleaned and standardized products dimensions with business tranformations",
   table_properties={
        "quality": "silver",
        "layer": "silver",
        "delta.enableChangeDataFeed": "true",
        "delta.autoOptimize.optimizeWrite": "true",
        "delta.autoOptimize.autoCompact": "true",
        "pipelines.autoOptimize.managed": "true"
   }
)
def silver_bronze():
    df= spark.read.table("sdp_project.bronze.city")
    df_silver=df.select(
        F.col('city_id').alias("city_id"),
        F.col("city_name").alias("city_name"),
        F.col("ingest_datetime").alias("bronze_ingtest_timestamp")
    )
    df_silver=df_silver.withColumn("silver_ingtest_timestamp",F.current_timestamp())
    return df_silver