Commands
========

Kappa is a command line tool.  The basic command format is:

``kappa [options] <command> [optional command args]``

Available ``options`` are:

* --config <config_file> to specify where to find the kappa config file.  The
  default is to look in ``kappa.yml``.
* --env <environment> to specify which environment in your config file you are
  using.  The default is ``dev``.
* --debug/--no-debug to turn on/off the debug logging.
* --help to access command line help.

And ``command`` is one of:

* deploy
* delete
* invoke
* tag
* tail
* event_sources
* status

Details of each command are provided below.

deploy
------

The ``deploy`` command does whatever is required to deploy the
current version of your Lambda function such as creating/updating policies and
roles, creating or updating the function itself, and adding any event sources
specified in your config file.

When the command is run the first time, it creates all of the relevant
resources required.  On subsequent invocations, it will attempt to determine
what, if anything, has changed in the project and only update those resources.

delete
------

The ``delete`` command deletes the Lambda function, remove any event sources,
delete the IAM  policy and role.

invoke
------

The ``invoke`` command makes a synchronous call to your Lambda function,
passing test data and display the resulting log data and any response returned
from your Lambda function.

The ``invoke`` command takes one positional argument, the ``data_file``.  This
should be the path to a JSON data file that will be sent to the function as
data.
  
tag
---

The ``tag`` command tags the current version of the Lambda function with a
symbolic tag.  In Lambda terms, this creates an ``alias``.

The ``tag`` command requires two additional positional arguments:

* name - the name of tag or alias
* description - the description of the alias

tail
----

The ``tail`` command displays the most recent log events for the function
(remember that it can take several minutes before log events are available from CloudWatch)

test
----

The ``test`` command provides a way to run unit tests of code in your Lambda
function.  By default, it uses the ``nose`` Python testrunner but this can be
overridden my specifying an alternative value using the ``unit_test_runner``
attribute in the kappa config file.

When using nose, it expects to find standard Python unit tests in the
``_tests/unit`` directory of your project.  It will then run those tests in an
environment that also makes any python modules in your ``_src`` directory
available to the tests.

event_sources
-------------

The ``event_sources`` command provides access the commands available for
dealing with event sources.  This command takes an additional positional
argument, ``command``.

* command - the command to run (list|enable|disable)

status
------

The ``status`` command displays summary information about functions, stacks,
and event sources related to your project.
