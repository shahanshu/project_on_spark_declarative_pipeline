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
    df= (
        spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "csv")
        .option("InferSchema", "true")
        .option("cloudFiles.schemaEvolutionMode","rescue")
        .option("cloudFiles.maxFilesPerTrigger",100)
        .load(SOURCE_PATH)
    )
    df= df.withColumnRenamed("distance_travelled(km)","distance_travelled_km")
    df=df.withColumn("file_name",F.col("_metadata.file_path")).withColumn("ingest_datatime",F.current_timestamp())
    return df