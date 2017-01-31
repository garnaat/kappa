=====
kappa
=====

.. image:: https://travis-ci.org/garnaat/kappa.svg?branch=develop
    :target: https://travis-ci.org/garnaat/kappa

.. image:: https://landscape.io/github/garnaat/kappa/develop/landscape.svg
    :target: https://landscape.io/github/garnaat/kappa/develop

**Kappa** is a command line tool that (hopefully) makes it easier to
deploy, update, and test functions for AWS Lambda.

There are quite a few steps involved in developing a Lambda function.
You have to:

* Write the function itself
* Create the IAM role required by the Lambda function itself (the executing role) to allow it access to any resources it needs to do its job
* Add additional permissions to the Lambda function if it is going to be used in a Push model (e.g. S3, SNS) rather than a Pull model.
* Zip the function and any dependencies and upload it to AWS Lambda
* Test the function with mock data
* Retrieve the output of the function from CloudWatch Logs
* Add an event source to the function
* View the output of the live function

Kappa tries to help you with some of this.  It creates all IAM policies for you
based on the resources you have told it you need to access.  It creates the IAM
execution role for you and associates the policy with it.  Kappa will zip up
the function and any dependencies and upload them to AWS Lambda.  It also sends
test data to the uploaded function and finds the related CloudWatch log stream
and displays the log events.  Finally, it will add the event source to turn
your function on.

If you need to make changes, kappa will allow you to easily update your Lambda
function with new code or update your event sources as needed.

Installation
============

The quickest way to get kappa is to install the latest stable version via pip::

    pip install kappa

Or for the development version::

    pip install git+https://github.com/garnaat/kappa.git


Quick Start
===========

To get a feel for how kappa works, let's take a look at a very simple example
contained in the ``samples/simple`` directory of the kappa distribution.  This
example is so simple, in fact, that it doesn't really do anything.  It's just a
small Lambda function (written in Python) that accepts some JSON input, logs
that input to CloudWatch logs, and returns a JSON document back.

The structure of the directory is::

    simple/
    ├── _src
    │   ├── README.md
    │   ├── requirements.txt
    │   ├── setup.cfg
    │   └── simple.py
    ├── _tests
    │   └── test_one.json
    └── kappa.yml.sample

Within the directory we see:

* ``kappa.yml.sample`` which is a sample YAML configuration file for the project
* ``_src`` which is a directory containing the source code for the Lambda function
* ``_test`` which is a directory containing some test data

The first step is to make a copy of the sample configuration file:

.. code-block:: bash

    cd simple
    cp kappa.yml.sample kappa.yml

Now you will need to edit ``kappa.yml`` slightly for your use.  The file looks
like this:

.. code-block:: yaml

    ---
    name: kappa-simple
    environments:
      dev:
        profile: <your profile here>
        region: <your region here>
        environment_variables:
          <key 1>: <value 1>
          <key 2>: <value 2>
        policy:
          resources:
            - arn: arn:aws:logs:*:*:*
              actions:
                - "*"
      prod:
        profile: <your profile here>
        region: <your region here>
        policy:
          resources:
            - arn: arn:aws:logs:*:*:*
              actions:
              - "*"
    lambda:
      description: A very simple Kappa example
      handler: simple.handler
      runtime: python2.7
      memory_size: 128
      timeout: 3

The ``name`` at the top is just a name used for this Lambda function and other
things we create that are related to this Lambda function (e.g. roles,
policies, etc.).

The ``environments`` section is where we define the different environments into
which we wish to deploy this Lambda function.  Each environment is identified
by a ``profile`` (as used in the AWS CLI and other AWS tools) and a
``region``.  You can define as many environments as you wish but each
invocation of ``kappa`` will deal with a single environment.  An environment
can optionally contain ``environment variables`` as key-value pairs.  Each
environment section also includes a ``policy`` section.  This is where we tell
kappa about AWS resources that our Lambda function needs access to and what
kind of access it requires.  For example, your Lambda function may need to
read from an SNS topic or write to a DynamoDB table and this is where you would
provide the ARN (`Amazon Resource Name`_) that identifies those resources.
Since this is a very simple example, the only resource listed here is for
CloudWatch logs so that our Lambda function is able to write to the CloudWatch
log group that will be created for it automatically by AWS Lambda.

.. _`Amazon Resource Name`: http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html

The ``lambda`` section contains the configuration information about our Lambda
function.  These values are passed to Lambda when we create the function and
can be updated at any time after.

To modify this for your own use, you just need to put in the right values for
``profile`` and ``region`` in one of the environment sections.  You can also
change the names of the environments to be whatever you like but the name
``dev`` is the default value used by kappa so it's kind of handy to avoid
typing.

Once you have made the necessary modifications, you should be ready to deploy
your Lambda function to the AWS Lambda service.  To do so, just do this:

.. code-block:: bash

    kappa deploy

This assumes you want to deploy the default environment called ``dev`` and that
you have named your config file ``kappa.yml``.  If, instead, you called your
environment ``test`` and named your config file foo.yml, you would do this:

.. code-block:: bash

    kappa --env test --config foo.yml deploy

In either case, you should see output that looks something like this:

.. code-block:: bash

    kappa deploy
    # deploying
    # ...deploying policy kappa-simple-dev
    # ...creating function kappa-simple-dev
    # done

So, what kappa has done is it has created a new Managed Policy called
``kappa-simple-dev`` that grants access to the CloudWatch Logs service.  It has
also created an IAM role called ``kappa-simple-dev`` that uses that policy.
And finally it has zipped up our Python code and created a function in AWS
Lambda called kappa-simple-dev.

To test this out, try this:

.. code-block:: bash

    kappa invoke _tests/test_one.json
    # invoking
    # START RequestId: 0f2f9ecf-9df7-11e5-ae87-858fbfb8e85f Version: $LATEST
    # [DEBUG]	2015-12-08T22:00:15.363Z	0f2f9ecf-9df7-11e5-ae87-858fbfb8e85f	{u'foo': u'bar', u'fie': u'baz'}
    # END RequestId: 0f2f9ecf-9df7-11e5-ae87-858fbfb8e85f
    # REPORT RequestId: 0f2f9ecf-9df7-11e5-ae87-858fbfb8e85f	Duration: 0.40 ms	Billed Duration: 100 ms 	Memory Size: 256 MB	Max Memory Used: 23 MB
    #
    # Response:
    # {"status": "success"}
    # done

We have just called our Lambda function, passing in the contents of the file
``_tests/test_one.json`` as input to our function.  We can see the output of
the CloudWatch logs for the call and we can see the logging call in the Python
function that prints out the ``event`` (the data) passed to the function.  And
finally, we can see the Response from the function which, for now, is just a
hard-coded data structure returned by the function.

Need to make a change in your function, your list of resources, or your
function configuration?  Just go ahead and make the change and then re-run the
``deploy`` command:

.. code-block:: bash

    kappa deploy

Kappa will figure out what has changed and make the necessary updates for you.

That gives you a quick overview of kappa.  To learn more about it, I recommend
you check out the tutorial.

Policies
========

Hands up who loves writing IAM policies. Yeah, that's what I thought. With
Kappa, there is a simplified way of writing policies and granting your Lambda
function the permissions it needs.

The simplified version allows you to specify, in your ``kappa.yml`` file, the
ARN of the resource you want to access, and then a list of the API methods you
want to allow. For example:

.. code-block:: yaml

    policy:
      resources:
        - arn: arn:aws:logs:*:*:*
          actions:
            - "*"

To express this using the official IAM policy format, you can instead use a
statement:

.. code-block:: yaml

    policy:
      statements:
        - Effect: Allow
          Resource: "*"
          Action:
            - "logs:*"

Both of these do the same thing.
