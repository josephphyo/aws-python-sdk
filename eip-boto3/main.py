import boto3


def main():
    ec2 = boto3.resource("ec2")

    for eips in ec2.vpc_addresses.all():
        if eips.association_id is None:  #https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/vpcaddress/association_id.html
            eips.release()
            print(f"The disassociated elastic-ip {eips} are released... ")
        else:
            print(f"The associated elastic-ip are {eips.instance_id} and public address are {eips.public_ip}")


if __name__ == "__main__":
    main()
