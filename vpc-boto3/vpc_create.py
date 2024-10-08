import boto3

# --- Create VPC

ec2 = boto3.client("ec2")
vpc_name = "vpc-boto-hol"

# --- check the vpc is already exist or not

response = ec2.describe_vpcs(
    Filters=[
        {
            "Name": "tag:Name",
            "Values": [
                vpc_name,
            ],
        }
    ]
)

vpcs = response.get("Vpcs", [])

if vpcs:
    vpc_id = vpcs[0]["VpcId"]
    print(f"VPC '{vpc_name} with ID '{vpc_id}' already exist")
else:
    vpc_response = ec2.create_vpc(
        CidrBlock="192.168.0.0/16",
    )
    vpc_id = vpc_response["Vpc"]["VpcId"]

    # --- Create Tags for VPC
    # --- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_tags.html

    ec2.create_tags(
        Resources=[
            vpc_id,
        ],
        Tags=[
            {
                "Key": "Name",
                "Value": vpc_name,
            },
        ],
    )

    print(f"VPC '{vpc_name} with ID '{vpc_id}' has been created")

# --- Create internet gateway

ig_name = "ig-vpc-boto-hol"

# --- check the internet gateway is already exist or not

response = ec2.describe_internet_gateways(
    Filters=[
        {
            "Name": "tag:Name",
            "Values": [
                ig_name,
            ],
        }
    ]
)

igw = response.get("InternetGateways", [])

if igw:
    ig_id = igw[0]["InternetGatewayId"]
    print(f"Internet Gateway '{ig_name} with ID '{ig_id}' already exist")
else:
    ig_response = ec2.create_internet_gateway()
    ig_id = ig_response["InternetGateway"]["InternetGatewayId"]

    # --- Create Tags for IGW
    # --- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_tags.html

    ec2.create_tags(
        Resources=[
            ig_id,
        ],
        Tags=[
            {
                "Key": "Name",
                "Value": ig_name,
            },
        ],
    )

    # --- Attach IGW to VPC

    ec2.attach_internet_gateway(VpcId=vpc_id, InternetGatewayId=ig_id)
    print(f"VPC '{ig_name} with ID '{ig_id}' has been created and attached to '{vpc_id}'")

# --- Create Route and Route Table
# --- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_route_table.html
# --- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/create_route.html

rt_response = ec2.create_route_table(VpcId=vpc_id)
rt_id = rt_response["RouteTable"]["RouteTableId"]

route = ec2.create_route(
    RouteTableId=rt_id, DestinationCidrBlock="0.0.0.0/0", GatewayId=ig_id
)
print(f"Route Table '{rt_id}' and Route '{route}' are created.")

# --- Create Subnets

pub_subnet_1 = ec2.create_subnet(
    AvailabilityZone="us-east-1a", CidrBlock="192.168.1.0/24", VpcId=vpc_id
)

pub_subnet_2 = ec2.create_subnet(
    AvailabilityZone="us-east-1b", CidrBlock="192.168.2.0/24", VpcId=vpc_id
)
print(f"Public Subnet 1 ID = {pub_subnet_1['Subnet']['SubnetId']} and CIDR {pub_subnet_1['Subnet']['CidrBlock']}")
print(f"Public Subnet 2 ID = {pub_subnet_2['Subnet']['SubnetId']} and CIDR {pub_subnet_2['Subnet']['CidrBlock']}")
