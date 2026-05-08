from pyspark import pipelines as dp 
from pyspark.sql import functions as F


@dp.view(
    name="trips_silver_staging", comment="Transformed trips data ready for cdc"
)
@dp.expect("vsalid_date","year(business_date)>=2025")
@dp.expect("valid_driver_rating","driver_rating BETWEEN 1 AND 10")
def trips_silver():
    df= spark.readStream.table("sdp_project.bronze.trips")
    df_silver = df.select(
        F.col("trip_id").alias("id"),
        F.col("date").cast("date").alias("business_date"),
        F.col("city_id").alias("city_id"),
        F.col("passenger_type").alias("passenger_category"),
        F.col("distance_travelled_km").alias("distance_kms"),
        F.col("fare_amount").alias("sales_amt"),
        F.col("passenger_rating").alias("passenger_rating"),
        F.col("driver_rating").alias("driver_rating"),
        F.col("ingest_datatime").alias("bronze_ingest_timestamp")
        )
    
    df_silver=df_silver.withColumn("silver_ingest_timestamp",F.current_timestamp())
    return df_silver
