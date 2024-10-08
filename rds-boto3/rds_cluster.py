import boto3
import time

rds = boto3.client('rds')

username = 'RDS_ADMIN'
password = 'RANDOM_PASS'
db_subnet_group = 'rds-db-subnetgroup-name'
db_cluster_id = 'rds-boto-hol'
db_engine_mode = 'serverless'  # serverless for aurora serverless V1, V2 is provisioned.

# --- create db cluster , check cluster is already exist or not.
try:
    response = rds.describe_db_clusters(DBClusterIdentifier=db_cluster_id)
    print(f"The DB Cluster '{db_cluster_id}' already exist. ")
except rds.exceptions.DBClusterNotFoundFault:
    response = rds.create_db_cluster(
        DBSubnetGroupName=db_subnet_group,
        DBClusterIdentifier=db_cluster_id,
        Engine='aurora-mysql',
        EngineVersion='5.7.mysql_aurora.2.80.3',
        MasterUsername=username,
        MasterUserPassword=password,
        EngineMode=db_engine_mode,
        EnableHttpEndpoint=True,

        ScalingConfiguration={
            'MinCapacity': 1,
            'MaxCapacity': 8,
            'AutoPause': True,
            'SecondsUntilAutoPause': 300  # Pause after 5 minutes IDLE. (Cost Saving)
        }
    )
    print(f"The DB Cluster '{db_cluster_id}' Created")

    # --- Wait for DB Cluster Available.
    while True:
        response = rds.describe_db_clusters(DBClusterIdentifier=db_cluster_id)
        status = response['DBClusters'][0]['Status']
        print(f"The status of the cluster is '{status}'")
        if status == "available":
            break

        print("Waiting for the DB cluster to become available....")
        time.sleep(40)

# --- modified the DB cluster.
# --- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds/client/modify_db_cluster.html

response = rds.modify_db_cluster(
        DBClusterIdentifier=db_cluster_id,

        ScalingConfiguration={
            'MinCapacity': 1,
            'MaxCapacity': 16,
            'AutoPause': True,
            'SecondsUntilAutoPause': 900  # Pause after 15 minutes IDLE. (Cost Saving)
        }
    )
print(f"The DB Cluster '{db_cluster_id}' Updated")

# --- Delete the DB cluster.

response = rds.delete_db_cluster(
        DBClusterIdentifier=db_cluster_id,
        SkipFinalSnapshot=True
)
print(f"The DB Cluster '{db_cluster_id}' Deleted")
