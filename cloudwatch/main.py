#! /env/bin/python
from enum import auto, Enum
from pprint import pprint
import boto3


class LogType(Enum):
    info = auto()
    warning = auto()
    error = auto()


logs = LogType


def run_aws():
    aws_connection = boto3.session.Session(profile_name="default")
    cloudwatch = aws_connection.client('logs')

    log_group_to_scan = "/aws/lambda/YourLambdaName"
    log_stream_filter_prefix = "2022/05/07/"

    try:
        response = cloudwatch.describe_log_groups(
            logGroupNamePrefix='/aws',
            limit=2
        )
        # pprint(response)
        # for log_group in response["logGroups"]:
        paginator = cloudwatch.get_paginator('describe_log_groups')
        response = paginator.paginate()
        for destination in response:
            print(destination)

        response = cloudwatch.describe_log_streams(logGroupName=log_group_to_scan,
                                                   descending=True,
                                                   logStreamNamePrefix=log_stream_filter_prefix)

        for logstream in response["logStreams"]:

            logstream_name = logstream["logStreamName"]
            print(f"Extracting logs for stream {logstream_name}")

            log_details = cloudwatch.get_log_events(
                logGroupName=log_group_to_scan,
                logStreamName=logstream_name,
            )

            for event in log_details["events"]:
                timestamp = int(event["timestamp"])
                message = str(event["message"])

                print(f"{timestamp}:{message}")

    except Exception as e:
        print(e)


if __name__ == '__main__':
    run_aws()
