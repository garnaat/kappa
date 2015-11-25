kappa
=====

[![Build Status](https://travis-ci.org/garnaat/kappa.svg?branch=develop)](https://travis-ci.org/garnaat/kappa)

[![Code Health](https://landscape.io/github/garnaat/kappa/develop/landscape.svg)](https://landscape.io/github/garnaat/kappa/develop)

**Kappa** is a command line tool that (hopefully) makes it easier to
deploy, update, and test functions for AWS Lambda.

There are quite a few steps involved in developing a Lambda function.
You have to:

* Write the function itself (Javascript only for now)
* Create the IAM role required by the Lambda function itself (the executing
role) to allow it access to any resources it needs to do its job
* Add additional permissions to the Lambda function if it is going to be used
in a Push model (e.g. S3, SNS) rather than a Pull model.
* Zip the function and any dependencies and upload it to AWS Lambda
* Test the function with mock data
* Retrieve the output of the function from CloudWatch Logs
* Add an event source to the function
* View the output of the live function

Kappa tries to help you with some of this.  It allows you to create an IAM
managed policy or use an existing one.  It creates the IAM execution role for
you and associates the policy with it.  Kappa will zip up the function and
any dependencies and upload them to AWS Lambda.  It also sends test data
to the uploaded function and finds the related CloudWatch log stream and
displays the log events.  Finally, it will add the event source to turn
your function on.

If you need to make changes, kappa will allow you to easily update your Lambda
function with new code or update your event sources as needed.

Installation
------------

The quickest way to get kappa is to install the latest stable version via pip:

    pip install kappa
    
Or for the development version:

    pip install git+https://github.com/garnaat/kappa.git


Getting Started
---------------

Kappa is a command line tool.  The basic command format is:

    kappa <path to config file> <command> [optional command args]

Where ``command`` is one of:

* create - creates the IAM policy (if necessary), the IAM role, and zips and
  uploads the Lambda function code to the Lambda service
* invoke - make a synchronous call to your Lambda function, passing test data
  and display the resulting log data
* invoke_async - make an asynchronous call to your Lambda function passing test
  data.
* dryrun - make the call but only check things like permissions and report
  back.  Don't actually run the code.
* tail - display the most recent log events for the function (remember that it
  can take several minutes before log events are available from CloudWatch)
* add_event_sources - hook up an event source to your Lambda function
* delete - delete the Lambda function, remove any event sources, delete the IAM
  policy and role
* update_code - Upload new code for your Lambda function
* update_event_sources - Update the event sources based on the information in
  your kappa config file
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
* Create any custom IAM policy you need to execute your Lambda function
* Create some sample data
* Create the YAML config file with all of the information
* Run ``kappa <path-to-config> create`` to create roles and upload function
* Run ``kappa <path-to-config> invoke`` to invoke the function with test data
* Run ``kappa <path-to-config> update_code`` to upload new code for your Lambda
  function
* Run ``kappa <path-to-config> add_event_sources`` to hook your function up to the event source
* Run ``kappa <path-to-config> tail`` to see more output
