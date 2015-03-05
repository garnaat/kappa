Kinesis Example
===============

This is a simple Lambda example that listens for events on a Kinesis stream.
This example is based on the one from the
[AWS Lambda Documentation](http://docs.aws.amazon.com/lambda/latest/dg/walkthrough-kinesis-events-adminuser.html).  The Lambda function in this example doesn't really do anything other than log some data but this example does show how all of the pieces go together and how to use ``kappa`` to deploy the Lambda function.

What You Need To Do
-------------------

1. Edit the ``config.yml`` file.  Specifically, you will need to edit the ``profile`` and ``region`` values and the ``event_source``
2. Run ``kappa --config config.yml deploy``
3. Run ``kappa --config config.yml test``
4. Run ``kappa --config config.yml tail``.  You may have to run this command a few times before the log events become available in CloudWatch Logs.
5. Run ``kappa --config config.yml add-event-source``
6. Try sending data to the Kinesis stream and then tailing the logs again to see if your function is getting called.



