def data_type():
    """entrypoint and fstrings"""

    instance_type = "t2.micro"
    message = "My Instance are of type: "

    number_of_instance = 5
    hours_running = 10

    print(
        f"{message} {instance_type}. I have {number_of_instance} of them and they have been running {hours_running} hours."
    )

    instance_running = True
    print(f"My instance are running {instance_running}?")


if __name__ == "__main__":
    data_type()
