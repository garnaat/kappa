The Code Is Here!
=================

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

