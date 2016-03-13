Why kappa?
==========

You can do everything kappa does by using the AWS Management Console so why use
kappa? Basically, because using GUI interfaces to drive your production
environment is a really bad idea.  You can't really automate GUI interfaces,
you can't debug GUI interfaces, and you can't easily share techniques and best
practices with a GUI.

The goal of kappa is to put everything about your AWS Lambda function into
files on a filesystem which can be easily versioned and shared.  Once your
files are in git, people on your team can create pull requests to merge new
changes in and those pull requests can be reviewed, commented on, and
eventually approved.  This is a tried and true approach that has worked for
more traditional deployment methodologies and will also work for AWS Lambda.
