SOURCE_PATH="/Volumes/sdp_project/data/volume101/Full Load/"
from pyspark import pipelines as dp
import pyspark.sql.functions as F

@dp.table(
    name="sdp_project.bronze.trips",
    comment="Streaming ingesting of raw orders data with Auto Loader",
    table_properties={
        "quality": "bronze",
        "layer": "bronze",
        "source_format": "csv",
        "delta.enableChangeDataFeed": "true",
        "delta.autoOptimize.optimizeWrite": "true",
        "delta.autoOptimize.autoCompact": "true"
    },
)
def order_bronze():
    df = (
        spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "csv")
        .option("InferSchema", "true")
        .option("cloudFiles.schemaEvolutionMode", "rescue")
        .option("cloudFiles.maxFilesPerTrigger", 100)
        .load(SOURCE_PATH)
    )
    df = df.withColumnRenamed("distance_travelled(km)", "distance_travelled_km")
    df = df.withColumn("file_name", F.col("_metadata.file_path")).withColumn("ingest_datatime", F.current_timestamp())
    return df


dp.create_streaming_table(
    name="sdp_project.silver.trips",
    comment="Cleaned and validated Orders with CDC upsert capability",
    table_properties={
        "quality": "silver",
        "layer": "silver",
        "delta.enableChangeDataFeed": "true",
        "delta.autoOptimize.optimizeWrite": "true",
        "delta.autoOptimize.autoCompact": "true"
    },
)

dp.create_auto_cdc_flow(
    target="sdp_project.silver.trips",
    source="sdp_project.bronze.trips",
    keys=["trip_id"],                              
    sequence_by=F.col("ingest_datatime"),   
    stored_as_scd_type=1,
    except_column_list=[]                   
)