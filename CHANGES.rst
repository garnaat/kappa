Changelog
=========

0.6.0 (2016-08-03)
------------------

- Fix for the config file example. [Igor Serko]

  Github doesn't seem to support `sourcecode` blocks ... instead they're
  called `code`, see http://docutils.sourceforge.net/docs/ref/rst/directives.html#code


- S3 Event Source Status fix. [Igor Serko]

  The CLI expects to see `EventSourceArn` and `State` in the result from the `status` method in each event_source. This makes it work for the S3 event sources


- 4-space indentation fix. [Matteo Sessa]

- Add support for prefix/suffix filters on S3. [Matteo Sessa]

- Include environment at lambda function qualifier. [Matteo Sessa]

- Include datasources in distribution. [Matteo Sessa]

- Fix #73. [LaiQiang Ding]

- Cloudwatch: eliminate 'else' before return in _to_status. [James
  Cooper]

- Remove event_source.py - accidentally re-added when I rebased. [James
  Cooper]

- Add .gitignore to 'cron' sample. [James Cooper]

- Added 'cron' sample to demo CloudWatch events. [James Cooper]

- Add CloudWatchEventSource. [James Cooper]

- Test_role.py: use string.printable instead of lowercase (fixes Python
  3.x) [James Cooper]

- Role.py: only strip 'Role' from 'get_role' response if present (passes
  placebo tests) [James Cooper]

- Add unit tests for Role.delete. [James Cooper]

- Context.py: revert pep8 fix. [James Cooper]

- Context.py: pep8 - line too long. [James Cooper]

- Modify role.delete to no-op if role missing. [James Cooper]

  If "kappa delete" fails midway then re-running it will fail during
  role removal.

  This PR modifies `delete` to check if the role exists.  If it does not
  then we log a debug line and return early.

  I also consolidated various methods that were calling `get_role` so that
  error handling is consistent, and removed `_find_all_roles` as
  `get_role` is sufficient, and probably faster (particularly for accounts
  with many roles).


- Fix code smell. [Jose Diaz-Gonzalez]

- Simplify event source retrieval. [Jose Diaz-Gonzalez]

- Make output look a little nicer. [Jose Diaz-Gonzalez]

- Require that environment exist before indexing it. [Jose Diaz-
  Gonzalez]

- Refactor event sources into their own modules. [Jose Diaz-Gonzalez]

0.5.1 (2016-06-12)
------------------

- Fix exception catching. [Jose Diaz-Gonzalez]

0.5.0 (2016-06-12)
------------------

- Merge remote-tracking branch 'Miserlou/tailwait' [Jose Diaz-Gonzalez]

- Well that was embarassing. Not sure how that happened. [Rich Jones]

- Replace tabs with spaces.. my fault for cowboy coding.. [Rich Jones]

- Fixes #23 - recursive tailing hur hur. [Rich Jones]

0.4.1 (2016-06-12)
------------------

- Add utf-8 encoding to each python file. [Jose Diaz-Gonzalez]

0.4.0 (2016-06-12)
------------------

- Remove markdown version of changelog. [Jose Diaz-Gonzalez]

- Reference correct readme file. [Jose Diaz-Gonzalez]

- Fix code smells in simple.py. [Jose Diaz-Gonzalez]

- Add release script. [Jose Diaz-Gonzalez]

- Make kappa pep8 compliant. [Jose Diaz-Gonzalez]

- Move version into __init__.py. [Jose Diaz-Gonzalez]

- Make setup.py runnable. [Jose Diaz-Gonzalez]

- Cleanup setup.py. [Jose Diaz-Gonzalez]

  - Read requirements from requirements.txt
  - Support both setuptools and distutils
  - Use wrapper for opening the correct file for requirements.txt and the readme
  - Import version from package
  - Hardcode package list
  - Avoid reading in entire license file when specifying the license attribute


- Separate dev and non-dev requirements. [Jose Diaz-Gonzalez]

- Convert readme to RST format. [Jose Diaz-Gonzalez]

- Show errors and stop function.create when ClientError. [Rodrigo Saito]

  The previous code checked only for one error and if some validation error occurred on AWS API
  then an infinite loop was happening.

- Fix vpc_config parameters. [Rodrigo Saito]

  Boto expects SecurityGroupIds and SubnetIds to be arrays instead of a strings separated with ",".

- Typo in Quick Start. [laiso]

- Add vpc_config to md5. [Jose Diaz-Gonzalez]

  Changing the VPC config otherwise results in configuration being ignored during a deploy

- Fix retrieval of resources when user is using statements. [Jose Diaz-
  Gonzalez]

- Add ability to enable and disable S3EventSource. [Jose Diaz-Gonzalez]

- Fix disabling event sources. [Jose Diaz-Gonzalez]

- Typo in "event_sources disable" cli-command. [Guyon Morée]

- Getting SNS sample working again. [Mitch Garnaat]

- Cleaning up a few small things. [Mitch Garnaat]

- Bumping placebo requirement version. [Mitch Garnaat]

- Bunch of changes leading up to the merge to develop. [Mitch Garnaat]

- Fix small bug. [Samuel Soubeyran]

- Add dependencies and check for existing key in zip before writing new
  file. [Samuel Soubeyran]

- Merge remote-tracking branch 'origin/python-refactor' into python-
  refactor. [Mitch Garnaat]

- Adding a way to put in a policy as is into the kappa config file.
  [Peter Sankauskas]

- Adding missing file. [Mitch Garnaat]

- Too aggressive on the packages to delete. [Mitch Garnaat]

- Add a list of files and directories to exclude from the zip package
  because they are already installed in Lambda. [Mitch Garnaat]

- Getting event sources working again. Lots of other changes. [Mitch
  Garnaat]

- Another run at fixing the Py3 encoding problems. [Mitch Garnaat]

- Fix encoding problems. [Mitch Garnaat]

- Encode the JSON document coming out of dumps(). [Mitch Garnaat]

- Fix 2.x only syntax on an except clause. [Mitch Garnaat]

- A bunch of changes to support new unit testing strategy with placebo.
  More tests to come. [Mitch Garnaat]

- Use source_dir of Context object to find source code. [Mitch Garnaat]

- Fixing issue with aliases after the first deployment.  Make sure role
  and policy names have the environment name in them. [Mitch Garnaat]

- Fixed some deployment issues.  Also changed it so that every code
  deployment creates not just a new version but also a new alias based
  on the environment.  No longer use environment explicitly in names.
  [Mitch Garnaat]

- Adding docs directory.  Still needs lots of work. [Mitch Garnaat]

- Some tweaks to the README file. [Mitch Garnaat]

- Adding a really simple python sample. [Mitch Garnaat]

- Merge remote-tracking branch 'origin/develop' into python-refactor.
  [Mitch Garnaat]

- README.md. [Christopher Manning]

  lambda supports more than javascript

- Fixing some ugly code. [Mitch Garnaat]

- Add placebo requirement. [Mitch Garnaat]

- Another WIP commit.  Major changes in the CLI.  Also much better
  detection of changes (or no changes) in the code, configuration,
  policies, etc. when deploying.  An attempt to incorporate a test
  runner that will run unit tests associated with the Lambda function.
  [Mitch Garnaat]

- Begin updates to README. Also, introduce a version attribute in the
  config file and use that, as well as the environment, to name
  resources.  Also use this name for the zip file and eliminate
  zipfile_name from config. [Mitch Garnaat]

- Add the missing call to build the zip file. [Mitch Garnaat]

- Allow an event source to be enabled/disabled. [Mitch Garnaat]

- Fixing a LOG call. [Mitch Garnaat]

- Add the ability to generate the config files based on the environment
  specified. [Mitch Garnaat]

- Fixing a few small style issues. [Mitch Garnaat]

- Fixing some typos and silly bugs. [Mitch Garnaat]

- A WIP commit on the new refactor for support of Python and other
  features. [Mitch Garnaat]

- `update_event_sources` fails on SNS and S3 event sources. [Ryan S.
  Brown]

  Per https://github.com/garnaat/kappa/issues/32 , adding an update method
  for event sources that don't have them.


- Updating boto3 dependency to latest GA version. [Mitch Garnaat]

- Delete the log group when the function is deleted.  Fixes #28. [Mitch
  Garnaat]

0.3.1 (2015-06-22)
------------------

- Bumping version number. [Mitch Garnaat]

- Handle paginated results for roles.  Fixes #17. [Mitch Garnaat]

- Adding a README to describe how to install nodejs dependencies for the
  S3 sample.  Fixes #18. [Mitch Garnaat]

- Updating s3 event sources to use new permissions feature rather than
  invocation role.  Fixes #20. [Mitch Garnaat]

- Bumping boto3 requirement to latest version. [Mitch Garnaat]

0.3.0 (2015-04-28)
------------------

- Updating version number and adding changelog. [Mitch Garnaat]

- Updating samples and fixing some bugs found in the process. [Mitch
  Garnaat]

- Updating boto3 dependency. [Mitch Garnaat]

- Rewriting some tests and also rewriting the MockAWS module to
  automatically map all responses in responses.py to mocks in the
  client. [Mitch Garnaat]

- Add debug logging about attaching policy to role. [Mitch Garnaat]

- More WIP changes to get current with GA release of Lambda. [Mitch
  Garnaat]

- Another WIP commit on the road to an update for the new Lambda API.
  [Mitch Garnaat]

- WIP Commit.  Updating to use new GA version of the Lambda API.  Also
  moving from botocore to boto3.  Also adding SNS example.  No longer
  using CloudFormation for policies since we only need one and
  CloudFormation does not yet support managed policies.  Haven't updated
  any tests yet so they will all be failing for now.  Also need to
  update README. [Mitch Garnaat]

0.2.2 (2015-03-24)
------------------

- Bumping version number. [Mitch Garnaat]

- Print last 10 log messages when executing `kappa <config> tail` [Ryan
  S. Brown]

- Also handle the UPDATE_ROLLBACK_COMPLETE failure state in `kappa
  deploy` [Ryan S. Brown]

0.2.1 (2015-03-05)
------------------

- Bumping version number. [Mitch Garnaat]

0.2.0 (2015-03-05)
------------------

- Bumping version number. [Mitch Garnaat]

- Minor fix for landscape. [Mitch Garnaat]

- Some refactoring.  Added a status command.  Rewrote the CLI to take
  more advantage of click. [Mitch Garnaat]

- Compress function zip file to save space/$$$ [Ryan S. Brown]

- Fixing case for add-event-sources. [Mitch Garnaat]

- Merging changes. [Mitch Garnaat]

- Fix call to add_event_source. [Ryan S. Brown]

- Fix invoke/exec role mixup with existing stack. [Ryan S. Brown]

- Add trailing comma to single element tuple. [Mitch Garnaat]

- A few tweaks based on landscape.io. feedback. [Mitch Garnaat]

- Fixing a few things landscape.io found. [Mitch Garnaat]

- Adding TravisCI and landscape.io badges. [Mitch Garnaat]

- Fixing Python 3.x issues. [Mitch Garnaat]

- Adding TravisCI config file. [Mitch Garnaat]

- Adding some unit tests. [Mitch Garnaat]

- Resolving merge conflict. [Mitch Garnaat]

- Add_event_source was not being called. [Colin Panisset]

- Add note about not requiring a profile if creds are in the
  environment. [Colin Panisset]

- Handle stack create/update rollbacks as failures. [Colin Panisset]

- If there's no profile defined, assume we will use environment
  variables. [Colin Panisset]

- WIP commit on significant refactoring of code. [Mitch Garnaat]

- Adding README for Kinesis sample. [Mitch Garnaat]

- Updating the S3 example and fixing a bug in the way directories are
  zipped for upload to Lambda. [Mitch Garnaat]

- Removing Node.js packages from repo.  These should be downloaded via
  npm. [Mitch Garnaat]

- Adding an initial S3 sample and code to register for event
  notification on an S3 bucket. [Mitch Garnaat]

- Added a few comments and removed redundant timestamp when printing log
  events. [Mitch Garnaat]

- Add a sentence about redeploying. [Mitch Garnaat]

- Fixing some typos. [Mitch Garnaat]

- Add info on add-event-source command. [Mitch Garnaat]

- Add link to kinesis sample. [Mitch Garnaat]

- Adding an inadequate README file. [Mitch Garnaat]

- Adding samples directory and add-event-source command plus polling
  after create/updating CF stack. [Mitch Garnaat]

- Initial version, barely working. [Mitch Garnaat]

- Initial commit. [Mitch Garnaat]


