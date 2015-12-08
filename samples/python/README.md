A Simple Python Example
=======================

In this Python example, we will build a Lambda function that can be hooked up
to methods in API Gateway to provide a simple CRUD REST API that persists JSON
objects in DynamoDB.

To implement this, we will create a single Lambda function that will be
associated with the GET, POST, PUT, and DELETE HTTP methods of a single API
Gateway resource.  We will show the API Gateway connections later.  For now, we
will focus on our Lambda function.



Installing Dependencies
-----------------------

Put all dependencies in the `requirements.txt` file in this directory and then
run the following command to install them in this directory prior to uploading
the code.

    $ pip install -r requirements.txt -t /full/path/to/this/code

This will install all of the dependencies inside the code directory so they can
be bundled with your own code and deployed to Lambda.

The ``setup.cfg`` file in this directory is required if you are running on
MacOS and are using brew.  It may not be needed on other platforms.

