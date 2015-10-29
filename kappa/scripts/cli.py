#!/usr/bin/env python
# Copyright (c) 2014, 2015 Mitch Garnaat http://garnaat.org/
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
# http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.

from datetime import datetime
import base64

import click

from kappa.context import Context


@click.group()
@click.argument(
    'config',
    type=click.File('rb'),
    envvar='KAPPA_CONFIG',
)
@click.option(
    '--debug/--no-debug',
    default=False,
    help='Turn on debugging output'
)
@click.option(
    '--environment',
    help='Specify which environment to work with'
)
@click.pass_context
def cli(ctx, config=None, debug=False, environment=None):
    config = config
    ctx.obj['debug'] = debug
    ctx.obj['config'] = config
    ctx.obj['environment'] = environment


@cli.command()
@click.pass_context
def deploy(ctx):
    """Deploy the Lambda function and any policies and roles required"""
    context = Context(ctx.obj['config'], ctx.obj['environment'],
                      ctx.obj['debug'])
    click.echo('deploying...')
    context.deploy()
    click.echo('...done')


@cli.command()
@click.pass_context
def tag(ctx):
    """Deploy the Lambda function and any policies and roles required"""
    context = Context(ctx.obj['config'], ctx.obj['environment'],
                      ctx.obj['debug'])
    click.echo('deploying...')
    context.deploy()
    click.echo('...done')


@cli.command()
@click.pass_context
def invoke(ctx):
    """Invoke the command synchronously"""
    context = Context(ctx.obj['config'], ctx.obj['environment'],
                      ctx.obj['debug'])
    click.echo('invoking...')
    response = context.invoke()
    log_data = base64.b64decode(response['LogResult'])
    click.echo(log_data)
    click.echo(response['Payload'].read())
    click.echo('...done')


@cli.command()
@click.pass_context
def dryrun(ctx):
    """Show you what would happen but don't actually do anything"""
    context = Context(ctx.obj['config'], ctx.obj['environment'],
                      ctx.obj['debug'])
    click.echo('invoking dryrun...')
    response = context.dryrun()
    click.echo(response)
    click.echo('...done')


@cli.command()
@click.pass_context
def invoke_async(ctx):
    """Invoke the Lambda function asynchronously"""
    context = Context(ctx.obj['config'], ctx.obj['environment'],
                      ctx.obj['debug'])
    click.echo('invoking async...')
    response = context.invoke_async()
    click.echo(response)
    click.echo('...done')


@cli.command()
@click.pass_context
def tail(ctx):
    """Show the last 10 lines of the log file"""
    context = Context(ctx.obj['config'], ctx.obj['environment'],
                      ctx.obj['debug'])
    click.echo('tailing logs...')
    for e in context.tail()[-10:]:
        ts = datetime.utcfromtimestamp(e['timestamp']//1000).isoformat()
        click.echo("{}: {}".format(ts, e['message']))
    click.echo('...done')


@cli.command()
@click.pass_context
def status(ctx):
    """Print a status of this Lambda function"""
    context = Context(ctx.obj['config'], ctx.obj['environment'],
                      ctx.obj['debug'])
    status = context.status()
    click.echo(click.style('Policy', bold=True))
    if status['policy']:
        line = '    {} ({})'.format(
            status['policy']['PolicyName'],
            status['policy']['Arn'])
        click.echo(click.style(line, fg='green'))
    click.echo(click.style('Role', bold=True))
    if status['role']:
        line = '    {} ({})'.format(
            status['role']['Role']['RoleName'],
            status['role']['Role']['Arn'])
        click.echo(click.style(line, fg='green'))
    click.echo(click.style('Function', bold=True))
    if status['function']:
        line = '    {} ({})'.format(
            status['function']['Configuration']['FunctionName'],
            status['function']['Configuration']['FunctionArn'])
        click.echo(click.style(line, fg='green'))
    else:
        click.echo(click.style('    None', fg='green'))
    click.echo(click.style('Event Sources', bold=True))
    if status['event_sources']:
        for event_source in status['event_sources']:
            if event_source:
                line = '    {}: {}'.format(
                    event_source['EventSourceArn'], event_source['State'])
                click.echo(click.style(line, fg='green'))
            else:
                click.echo(click.style('    None', fg='green'))


@cli.command()
@click.pass_context
def delete(ctx):
    """Delete the Lambda function and related policies and roles"""
    context = Context(ctx.obj['config'], ctx.obj['environment'],
                      ctx.obj['debug'])
    click.echo('deleting...')
    context.delete()
    click.echo('...done')


@cli.command()
@click.pass_context
def add_event_sources(ctx):
    """Add any event sources specified in the config file"""
    context = Context(ctx.obj['config'], ctx.obj['environment'],
                      ctx.obj['debug'])
    click.echo('adding event sources...')
    context.add_event_sources()
    click.echo('...done')


@cli.command()
@click.pass_context
def update_event_sources(ctx):
    """Update event sources specified in the config file"""
    context = Context(ctx.obj['config'], ctx.obj['environment'],
                      ctx.obj['debug'])
    click.echo('updating event sources...')
    context.update_event_sources()
    click.echo('...done')


cli(obj={})
