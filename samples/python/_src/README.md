The Code Is Here!
=================

At the moment, the contents of this directory are created by hand but when
LambdaPI is complete, the basic framework would be created for you.  You would
have a Python source file that works but doesn't actually do anything.  And the
config.json file here would be created on the fly at deployment time.  The
correct resource names and other variables would be written into the config
file and then then config file would get bundled up with the code.  You can
then load the config file at run time in the Lambda Python code so you don't
have to hardcode resource names in your code.


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

