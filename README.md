kappa
=====

**Kappa** is a command line tool that (hopefully) makes it easier to
deploy, update, and test functions for AWS Lambda.

There are quite a few steps involved in developing a Lambda function.
You have to:

* Write the function itself (Javascript only for now)
* Create the IAM roles required by the Lambda function itself (the executing
role) as well as the policy required by whoever is invoking the Lambda
function (the invocation role)
* Compress the function and any dependencies and upload it to AWS Lambda
* Test the function with mock data
* Retrieve the output of the function from CloudWatch Logs
* Add an event source to the function
* View the output of the live function

Kappa tries to help you with some of this.  The IAM roles are created
in a CloudFormation template and kappa takes care of creating, updating, and
deleting the CloudFormation stack.  Kappa will also zip up the function and
any dependencies and upload them to AWS Lambda.  It also sends test data
to the uploaded function and finds the related CloudWatch log stream and
displays the log events.  Finally, it will add the event source to turn
your function on.

Kappa is a command line tool.  The basic command is:

    kappa --config <path to config file> <command>

Where commands is one of:

* deploy - deploy the CloudFormation template containing the IAM roles and zip the function and upload it to AWS Lambda
* test - send test data to the new Lambda function
* tail - display the most recent log events for the function
* add-event-source - hook up an event source to your Lambda function
* delete - delete the CloudFormation stack containing the IAM roles and delete the Lambda function

The ``config file`` is a YAML format file containing all of the information
about your Lambda function.

An example project based on a Kinesis stream can be found in
[samples/kinesis](https://github.com/garnaat/kappa/tree/develop/samples/kinesis).

The basic workflow would be to:

* Create your Lambda function
* Create your CloudFormation template with the execution and invocation roles
* Create some sample data
* Create the YAML config file with all of the information
* Run ``kappa --config <path-to-config> deploy`` to create roles and upload function
* Run ``kappa --config <path-to-config> test`` to invoke the function with test data
* Run ``kappa --config <path-to-config> tail`` to view the functions output in CloudWatch logs
* Run ``kappa --config <path-to-config> add-event-source`` to hook your function up to the event source
* Run ``kappa --config <path-to-config> tail`` to see more output

