# Permissions

- SQS permissions
```shell
{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Sid": "VisualEditor0",
			"Effect": "Allow",
			"Action": [
				"sqs:DeleteMessage",
				"sqs:CancelMessageMoveTask",
				"sqs:ListMessageMoveTasks",
				"sqs:ReceiveMessage",
				"sqs:GetQueueAttributes"
			],
			"Resource": "arn:aws:sqs:us-east-1:448270596972:orders-queue"
		}
	]
}
```

- SSM permissions (Systems Manager)
```shell
{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Sid": "VisualEditor0",
			"Effect": "Allow",
			"Action": [
				"ssm:GetParameters",
				"ssm:GetParameter"
			],
			"Resource": "arn:aws:ssm:us-east-1:448270596972:parameter/mongodb-connection-string"
		}
	]
}
```

- DynamoDB permissions
```shell
{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Sid": "VisualEditor0",
			"Effect": "Allow",
			"Action": [
				"dynamodb:PutItem",
				"dynamodb:GetItem",
				"dynamodb:Query"
			],
			"Resource": "arn:aws:dynamodb:us-east-1:448270596972:table/lambda_orders_consumer_execs"
		}
	]
}
```


# Redrive
```python
import boto3

sqs = boto3.client(
	"sqs",
	region_name="sa-east-1",

)

sqs.start_message_move_task(
    SourceArn="arn:aws:sqs:sa-east-1:448270596972:orders-queue-dlq",
    DestinationArn="arn:aws:sqs:sa-east-1:448270596972:orders-queue"  # do not send this param to allow use the original source queue
)
```