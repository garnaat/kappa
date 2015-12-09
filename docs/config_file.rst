The Config File
===============

The config file is at the heart of kappa.  It is what describes your functions
and drives your deployments.  This section provides a reference for all of the
elements of the kappa config file.

Example
-------

Here is a simple example config file from the sample/simple directory::

    ---
    name: foobar
    environments:
      dev:
        profile: fiebaz-dev
        region: us-west-2
        policy:
          arn: arn:aws:iam::aws:policy/service-role/AWSLambdaRole
      prod:
        profile: fiebaz-prod
        region: us-west-2
        policy:
          arn: arn:aws:iam::aws:policy/service-role/AWSLambdaRole
    lambda:
      description: A simple Python Lambda example
      path: code/
      handler: foobar.handler
      runtime: python2.7
      memory_size: 256
      timeout: 3
      test_data: input.json

This config file is defining 

