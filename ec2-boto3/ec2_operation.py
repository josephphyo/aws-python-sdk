import boto3

ec2 = boto3.resource("ec2")
instance_name = "workload-boto3-instance"

# --- store instance id

instance_id = None

all_instances = ec2.instances.all()  # it's come with Lists
instance_exist = False

# --- Checking Instance are exist or not.

for instance in all_instances:
    for tag in instance.tags:
        if tag["Key"] == "Name" and tag["Value"] == instance_name:
            instance_exist = True
            instance_id = instance.id
            print(
                f"An instance named '{instance_name}' with id '{instance_id}' already exists."
            )
            break
    if instance_exist:
        break

# --- Create instance - Service Resource
# --- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/create_instances.html
# --- When instance_exist = False, will create new one.

if not instance_exist:
    new_instances = ec2.create_instances(
        ImageId="ami-0fff1b9a61dec8a5f",  # Amazon Linux - us-east-1
        SubnetId="subnet-07ebc37768e9a9097",
        MinCount=1,
        MaxCount=1,
        InstanceType="t2.micro",
        KeyName="DevOps-Keys",
        TagSpecifications=[
            {
                "ResourceType": "instance",
                "Tags": [
                    {"Key": "Name", "Value": instance_name},
                ],
            },
        ],
    )
    instance_id = new_instances[0].id
    print(f"Instance named '{instance_name} with id '{instance_id}' created.")

# --- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/instance/terminate.html
# --- Stop the instance

ec2.Instance(instance_id).stop()
print(f"The instance '{instance_name}' id '{instance_id}' is stopped.")

# --- Start the instance

ec2.Instance(instance_id).start()
print(f"The instance '{instance_name}' id '{instance_id}' is started.")

# --- Terminate the instance

ec2.Instance(instance_id).terminate()
print(f"The instance '{instance_name}' id '{instance_id}' is terminated.")
