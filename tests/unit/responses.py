import datetime
from dateutil.tz import tzutc

iam_list_policies = [{u'IsTruncated': True,
 u'Marker': 'ABcyoYmSlphARcitCJruhVIxKW3Hg1LJD3Fm4LAW8iGKykrSNrApiUoz2rjIuNiLJpT6JtUgP5M7wTuPZcHu1KsvMarvgFBFQObTPSa4WF22Zg==',
 u'Policies': [{u'Arn': 'arn:aws:iam::123456789012:policy/FooPolicy',
   u'AttachmentCount': 0,
   u'CreateDate': datetime.datetime(2015, 2, 24, 3, 16, 24, tzinfo=tzutc()),
   u'DefaultVersionId': 'v2',
   u'IsAttachable': True,
   u'Path': '/',
   u'PolicyId': 'ANPAJHWE6R7YT7PLAH3KG',
   u'PolicyName': 'FooPolicy',
   u'UpdateDate': datetime.datetime(2015, 2, 25, 0, 19, 12, tzinfo=tzutc())},
  {u'Arn': 'arn:aws:iam::123456789012:policy/BarPolicy',
   u'AttachmentCount': 1,
   u'CreateDate': datetime.datetime(2015, 2, 25, 0, 11, 57, tzinfo=tzutc()),
   u'DefaultVersionId': 'v2',
   u'IsAttachable': True,
   u'Path': '/',
   u'PolicyId': 'ANPAJU7MVBQXOQTVQN3VM',
   u'PolicyName': 'BarPolicy',
   u'UpdateDate': datetime.datetime(2015, 2, 25, 0, 13, 8, tzinfo=tzutc())},
  {u'Arn': 'arn:aws:iam::123456789012:policy/FiePolicy',
   u'AttachmentCount': 1,
   u'CreateDate': datetime.datetime(2015, 3, 21, 19, 18, 21, tzinfo=tzutc()),
   u'DefaultVersionId': 'v4',
   u'IsAttachable': True,
   u'Path': '/',
   u'PolicyId': 'ANPAIXQ72B2OH2RZPYQ4Y',
   u'PolicyName': 'FiePolicy',
   u'UpdateDate': datetime.datetime(2015, 3, 26, 23, 26, 52, tzinfo=tzutc())}],
'ResponseMetadata': {'HTTPStatusCode': 200,
  'RequestId': '4e87c995-ecf2-11e4-bb10-51f1499b3162'}}]

iam_create_policy = [{u'Policy': {u'PolicyName': 'LambdaChatDynamoDBPolicy', u'CreateDate': datetime.datetime(2015, 4, 27, 12, 13, 35, 240000, tzinfo=tzutc()), u'AttachmentCount': 0, u'IsAttachable': True, u'PolicyId': 'ANPAISQNU4EPZZDVZUOKU', u'DefaultVersionId': 'v1', u'Path': '/kappa/', u'Arn': 'arn:aws:iam::658794617753:policy/kappa/LambdaChatDynamoDBPolicy', u'UpdateDate': datetime.datetime(2015, 4, 27, 12, 13, 35, 240000, tzinfo=tzutc())}, 'ResponseMetadata': {'HTTPStatusCode': 200, 'RequestId': 'd403e95f-ecd6-11e4-9ee0-15e8b71db930'}}]

iam_list_roles = [{'ResponseMetadata': {'HTTPStatusCode': 200, 'RequestId': 'd41415ff-ecd6-11e4-bb10-51f1499b3162'}, u'IsTruncated': False, u'Roles': [{u'AssumeRolePolicyDocument': {u'Version': u'2012-10-17', u'Statement': [{u'Action': u'sts:AssumeRole', u'Principal': {u'Service': u'lambda.amazonaws.com'}, u'Effect': u'Allow', u'Sid': u''}]}, u'RoleId': 'AROAJ4JSNL3M4UYI6GDYS', u'CreateDate': datetime.datetime(2015, 4, 27, 11, 59, 19, tzinfo=tzutc()), u'RoleName': 'FooRole', u'Path': '/kappa/', u'Arn': 'arn:aws:iam::123456789012:role/kappa/FooRole'}]}]

iam_create_role = [{u'Role': {u'AssumeRolePolicyDocument': {u'Version': u'2012-10-17', u'Statement': [{u'Action': [u'sts:AssumeRole'], u'Effect': u'Allow', u'Principal': {u'Service': [u'lambda.amazonaws.com']}}]}, u'RoleId': 'AROAIT2ZRRPQBOIBBHPZU', u'CreateDate': datetime.datetime(2015, 4, 27, 12, 13, 35, 426000, tzinfo=tzutc()), u'RoleName': 'BazRole', u'Path': '/kappa/', u'Arn': 'arn:aws:iam::123456789012:role/kappa/BazRole'}, 'ResponseMetadata': {'HTTPStatusCode': 200, 'RequestId': 'd41fd55c-ecd6-11e4-9fd8-03ee0021e940'}}]

iam_get_role = [{u'Role': {u'AssumeRolePolicyDocument': {u'Version': u'2012-10-17', u'Statement': [{u'Action': u'sts:AssumeRole', u'Principal': {u'Service': u's3.amazonaws.com'}, u'Effect': u'Allow', u'Condition': {u'ArnLike': {u'sts:ExternalId': u'arn:aws:s3:::*'}}, u'Sid': u''}, {u'Action': u'sts:AssumeRole', u'Principal': {u'Service': u'lambda.amazonaws.com'}, u'Effect': u'Allow', u'Sid': u''}]}, u'RoleId': 'AROAIEVJHUJG2I4MG5PSC', u'CreateDate': datetime.datetime(2015, 1, 6, 17, 37, 44, tzinfo=tzutc()), u'RoleName': 'TestKinesis-InvokeRole-IF6VUXY9MBJN', u'Path': '/', u'Arn': 'arn:aws:iam::0123456789012:role/TestKinesis-InvokeRole-FOO'}, 'ResponseMetadata': {'HTTPStatusCode': 200, 'RequestId': 'dd6e8d42-9699-11e4-afe6-d3625e8b365b'}}]

iam_attach_role_policy = [{'ResponseMetadata': {'HTTPStatusCode': 200, 'RequestId': 'd43e32dc-ecd6-11e4-9fd8-03ee0021e940'}}]

iam_detach_role_policy = [{'ResponseMetadata': {'HTTPStatusCode': 200, 'RequestId': 'a7d30b51-ecd6-11e4-bbe4-d996b8ad5d9e'}}]

iam_delete_role = [{'ResponseMetadata': {'HTTPStatusCode': 200, 'RequestId': 'a7e5a97e-ecd6-11e4-ae9e-6dee7bf37e66'}}]

lambda_create_function = [{u'FunctionName': u'LambdaChatDynamoDB', 'ResponseMetadata': {'HTTPStatusCode': 201, 'RequestId': 'd7840efb-ecd6-11e4-b8b0-f7f3177894e9'}, u'CodeSize': 22024, u'MemorySize': 128, u'FunctionArn': u'arn:aws:lambda:us-east-1:123456789012:function:FooBarFunction', u'Handler': u'FooBarFunction.handler', u'Role': u'arn:aws:iam::123456789012:role/kappa/BazRole', u'Timeout': 3, u'LastModified': u'2015-04-27T12:13:41.147+0000', u'Runtime': u'nodejs', u'Description': u'A FooBar function'}]

lambda_delete_function = [{'ResponseMetadata': {'HTTPStatusCode': 204, 'RequestId': 'a499b2c2-ecd6-11e4-8d2a-77b7e55836e7'}}]

logs_describe_log_groups = [{'ResponseMetadata': {'HTTPStatusCode': 200,
  'RequestId': 'da962431-afed-11e4-8c17-1776597471e6'},
 u'logGroups': [{u'arn': u'arn:aws:logs:us-east-1:0123456789012:log-group:/aws/lambda/KinesisSample*',
   u'creationTime': 1423175925414,
   u'logGroupName': u'foo/bar',
   u'metricFilterCount': 1,
                 u'storedBytes': 0}]},
{'ResponseMetadata': {'HTTPStatusCode': 200,
  'RequestId': 'da962431-afed-11e4-8c17-1776597471e6'},
 u'logGroups': [{u'arn': u'arn:aws:logs:us-east-1:0123456789012:log-group:/aws/lambda/KinesisSample*',
   u'creationTime': 1423175925414,
   u'logGroupName': u'foo/bar',
   u'metricFilterCount': 1,
                 u'storedBytes': 0}]}]                       

logs_describe_log_streams = [{u'logStreams': [{u'firstEventTimestamp': 1417042749449, u'lastEventTimestamp': 1417042749547, u'creationTime': 1417042748263, u'uploadSequenceToken': u'49540114640150833041490484409222729829873988799393975922', u'logStreamName': u'1cc48e4e613246b7974094323259d600', u'lastIngestionTime': 1417042750483, u'arn': u'arn:aws:logs:us-east-1:0123456789012:log-group:/aws/lambda/KinesisSample:log-stream:1cc48e4e613246b7974094323259d600', u'storedBytes': 712}, {u'firstEventTimestamp': 1417272406988, u'lastEventTimestamp': 1417272407088, u'creationTime': 1417272405690, u'uploadSequenceToken': u'49540113907504451034164105858363493278561872472363261986', u'logStreamName': u'2782a5ff88824c85a9639480d1ed7bbe', u'lastIngestionTime': 1417272408043, u'arn': u'arn:aws:logs:us-east-1:0123456789012:log-group:/aws/lambda/KinesisSample:log-stream:2782a5ff88824c85a9639480d1ed7bbe', u'storedBytes': 712}, {u'firstEventTimestamp': 1420569035842, u'lastEventTimestamp': 1420569035941, u'creationTime': 1420569034614, u'uploadSequenceToken': u'49540113907883563702539166025438885323514410026454245426', u'logStreamName': u'2d62991a479b4ebf9486176122b72a55', u'lastIngestionTime': 1420569036909, u'arn': u'arn:aws:logs:us-east-1:0123456789012:log-group:/aws/lambda/KinesisSample:log-stream:2d62991a479b4ebf9486176122b72a55', u'storedBytes': 709}, {u'firstEventTimestamp': 1418244027421, u'lastEventTimestamp': 1418244027541, u'creationTime': 1418244026907, u'uploadSequenceToken': u'49540113964795065449189116778452984186276757901477438642', u'logStreamName': u'4f44ffa128d6405591ca83b2b0f9dd2d', u'lastIngestionTime': 1418244028484, u'arn': u'arn:aws:logs:us-east-1:0123456789012:log-group:/aws/lambda/KinesisSample:log-stream:4f44ffa128d6405591ca83b2b0f9dd2d', u'storedBytes': 1010}, {u'firstEventTimestamp': 1418242565524, u'lastEventTimestamp': 1418242565641, u'creationTime': 1418242564196, u'uploadSequenceToken': u'49540113095132904942090446312687285178819573422397343074', u'logStreamName': u'69c5ac87e7e6415985116e8cb44e538e', u'lastIngestionTime': 1418242566558, u'arn': u'arn:aws:logs:us-east-1:0123456789012:log-group:/aws/lambda/KinesisSample:log-stream:69c5ac87e7e6415985116e8cb44e538e', u'storedBytes': 713}, {u'firstEventTimestamp': 1417213193378, u'lastEventTimestamp': 1417213193478, u'creationTime': 1417213192095, u'uploadSequenceToken': u'49540113336360065754596187770479764234792559857643841394', u'logStreamName': u'f68e3d87b8a14cdba338f6926f7cf50a', u'lastIngestionTime': 1417213194421, u'arn': u'arn:aws:logs:us-east-1:0123456789012:log-group:/aws/lambda/KinesisSample:log-stream:f68e3d87b8a14cdba338f6926f7cf50a', u'storedBytes': 711}], 'ResponseMetadata': {'HTTPStatusCode': 200, 'RequestId': '2a6d4941-969b-11e4-947f-19d1c72ede7e'}}]

logs_get_log_events = [{'ResponseMetadata': {'HTTPStatusCode': 200, 'RequestId': '2a7deb71-969b-11e4-914b-8f1f3d7b023d'}, u'nextForwardToken': u'f/31679748107442531967654742688057700554200447759088287749', u'events': [{u'ingestionTime': 1420569036909, u'timestamp': 1420569035842, u'message': u'2015-01-06T18:30:35.841Z\tko2sss03iq7l2pdk\tLoading event\n'}, {u'ingestionTime': 1420569036909, u'timestamp': 1420569035899, u'message': u'START RequestId: 23007242-95d2-11e4-a10e-7b2ab60a7770\n'}, {u'ingestionTime': 1420569036909, u'timestamp': 1420569035940, u'message': u'2015-01-06T18:30:35.940Z\t23007242-95d2-11e4-a10e-7b2ab60a7770\t{\n  "Records": [\n    {\n      "kinesis": {\n        "partitionKey": "partitionKey-3",\n        "kinesisSchemaVersion": "1.0",\n        "data": "SGVsbG8sIHRoaXMgaXMgYSB0ZXN0IDEyMy4=",\n        "sequenceNumber": "49545115243490985018280067714973144582180062593244200961"\n      },\n      "eventSource": "aws:kinesis",\n      "eventID": "shardId-000000000000:49545115243490985018280067714973144582180062593244200961",\n      "invokeIdentityArn": "arn:aws:iam::0123456789012:role/testLEBRole",\n      "eventVersion": "1.0",\n      "eventName": "aws:kinesis:record",\n      "eventSourceARN": "arn:aws:kinesis:us-east-1:35667example:stream/examplestream",\n      "awsRegion": "us-east-1"\n    }\n  ]\n}\n'}, {u'ingestionTime': 1420569036909, u'timestamp': 1420569035940, u'message': u'2015-01-06T18:30:35.940Z\t23007242-95d2-11e4-a10e-7b2ab60a7770\tDecoded payload: Hello, this is a test 123.\n'}, {u'ingestionTime': 1420569036909, u'timestamp': 1420569035941, u'message': u'END RequestId: 23007242-95d2-11e4-a10e-7b2ab60a7770\n'}, {u'ingestionTime': 1420569036909, u'timestamp': 1420569035941, u'message': u'REPORT RequestId: 23007242-95d2-11e4-a10e-7b2ab60a7770\tDuration: 98.51 ms\tBilled Duration: 100 ms \tMemory Size: 128 MB\tMax Memory Used: 26 MB\t\n'}], u'nextBackwardToken': u'b/31679748105234758193000210997045664445208259969996226560'}]
