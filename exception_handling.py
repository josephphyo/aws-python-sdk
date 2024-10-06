def no_service_in_dict(service):
    print(f"There is no service {service} in the dictionary")


def get_service_status(service_name):
    aws_services_statuses = {
        "EC2": "Maintenance",
        "S3": "Operational",
        "Lambda": "Issues Detected",
        "DynamoDB": "Operational",
        "RDS": "Operational",
    }

    return aws_services_statuses[service_name]


def main():
    try:
        service = "DynamoDB"

        service_status = get_service_status(service)

        print(f"\n{service} service status: '{service_status}'")

        if service_status == "Operational":
            print(f"Performing operation on '{service}'.")
        else:
            print(f"'{service}' is NOT operational.")

    except KeyError as e:
        print(f"Error: {e}")
        no_service_in_dict(e)


if __name__ == "__main__":
    main()
