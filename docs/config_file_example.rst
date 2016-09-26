The Config File
===============

The config file is at the heart of kappa.  It is what describes your functions
and drives your deployments.  This section provides a reference for all of the
elements of the kappa config file.


Example
-------

Here is an example config file showing all possible sections.

.. code:: yaml
    :number-lines:

    ---
    name: kappa-python-sample
    environments:
      env1:
        profile: profile1
        region: us-west-2
        policy:
          resources:
            - arn: arn:aws:dynamodb:us-west-2:123456789012:table/foo
              actions:
              - "*"
            - arn: arn:aws:logs:*:*:*
              actions:
              - "*"
       event_sources:
         -
           arn: arn:aws:kinesis:us-west-2:123456789012:stream/foo
           starting_position: LATEST
           batch_size: 100
      env2:
        profile: profile2
        region: us-west-2
        policy_resources:
          - arn: arn:aws:dynamodb:us-west-2:234567890123:table/foo
            actions:
            - "*"
          - arn: arn:aws:logs:*:*:*
            actions:
            - "*"
       event_sources:
         -
           arn: arn:aws:kinesis:us-west-2:234567890123:stream/foo
           starting_position: LATEST
           batch_size: 100
    lambda:
      description: A simple Python sample
      handler: simple.handler
      runtime: python2.7
      memory_size: 256
      timeout: 3
      log_retention_policy: 7
      vpc_config:
        security_group_ids:
          - sg-12345678
          - sg-23456789
        subnet_ids:
          - subnet-12345678
          - subnet-23456789


Explanations:

===========    =============================================================
Line Number    Description
===========    =============================================================
2              This name will be used to name the function itself as well as
               any policies and roles created for use by the function.
3              A map of environments.  Each environment represents one
               possible deployment target.  For example, you might have a
               dev and a prod.  The names can be whatever you want but the
               environment names are specified using the --env option when
               you deploy.
5              The profile name associated with this environment.  This
               refers to a profile in your AWS credential file.
6              The AWS region associated with this environment.
7              This section defines the elements of the IAM policy that will
               be created for this function in this environment.
9              Each resource your function needs access to needs to be
               listed here.  Provide the ARN of the resource as well as
               a list of actions.  This could be wildcarded to allow all
               actions but preferably should list the specific actions you
               want to allow.
15             If your Lambda function has any event sources, this would be
               where you list them.  Here, the example shows a Kinesis
               stream but this could also be a DynamoDB stream, an SNS
               topic, or an S3 bucket.
18             For Kinesis streams and DynamoDB streams, you can specify
               the starting position (one of LATEST or TRIM_HORIZON) and
               the batch size.
35             This section contains settings specify to your Lambda
               function.  See the Lambda docs for details on these.
===========    =============================================================
