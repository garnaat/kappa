CHANGELOG
=========

1.0.0
-----

* Updated for GA release of AWS Lambda.
* Incompatible changes in available commands and in config file format.  Check
  README for details.
* Switched from botocore to boto3.
* No longer using CloudFormation to create policies and roles.  Instead we
  now use Managed policies and roles created with boto3.
