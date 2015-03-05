kappa
=====

[![Build Status](https://travis-ci.org/garnaat/kappa.svg?branch=develop)](https://travis-ci.org/garnaat/kappa)

[![Code Health](https://landscape.io/github/garnaat/kappa/develop/landscape.svg)](https://landscape.io/github/garnaat/kappa/develop)

**Kappa** is a command line tool that (hopefully) makes it easier to
deploy, update, and test functions for AWS Lambda.

There are quite a few steps involved in developing a Lambda function.
You have to:

* Write the function itself (Javascript only for now)
* Create the IAM roles required by the Lambda function itself (the executing
role) as well as the policy required by whoever is invoking the Lambda
function (the invocation role)
* Zip the function and any dependencies and upload it to AWS Lambda
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

Kappa is a command line tool.  The basic command format is:

    kappa <path to config file> <command> [optional command args]

Where ``command`` is one of:

* deploy - deploy the CloudFormation template containing the IAM roles and zip
  the function and upload it to AWS Lambda
* test - send test data to the new Lambda function
* tail - display the most recent log events for the function (remember that it
  can take several minutes before log events are available from CloudWatch)
* add-event-sources - hook up an event source to your Lambda function
* delete - delete the CloudFormation stack containing the IAM roles and delete
  the Lambda function
* status - display summary information about functions, stacks, and event
  sources related to your project.

The ``config file`` is a YAML format file containing all of the information
about your Lambda function.

If you use environment variables for your AWS credentials (as normally supported by boto),
simply exclude the ``profile`` element from the YAML file.

An example project based on a Kinesis stream can be found in
[samples/kinesis](https://github.com/garnaat/kappa/tree/develop/samples/kinesis).

The basic workflow is:

* Create your Lambda function
* Create your CloudFormation template with the execution and invocation roles
* Create some sample data
* Create the YAML config file with all of the information
* Run ``kappa <path-to-config> deploy`` to create roles and upload function
* Run ``kappa <path-to-config> test`` to invoke the function with test data
* Run ``kappa <path-to-config> tail`` to view the functions output in CloudWatch logs
* Run ``kappa <path-to-config> add-event-source`` to hook your function up to the event source
* Run ``kappa <path-to-config> tail`` to see more output

If you have to make changes in your function or in your IAM roles, simply run
``kappa deploy`` again and the changes will be uploaded as necessary.
