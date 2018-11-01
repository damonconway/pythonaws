#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Webotron: Deploy sites with AWS.

Webotron automates the process of deploying static sites to AWS.
- Configure AWS S3 buckets
  - Create them
  - Set them up for static website hosting
  - Deploy local files to them
- Configure DNS with AWS Route 53
- Configure a Content Delivery Network and SSL with AWS CloudFront
"""

import boto3
import click

from bucket import BucketManager
from domain import DomainManager
from certificate import CertificateManager
from cdn import DistributionManager
import util

SESSION = None
BUCKET_MANAGER = None
DOMAIN_MANAGER = None
CERT_MANAGER = None
DIST_MANAGER = None


@click.group()
@click.option(
    '--profile',
    default=None,
    help="Use a given AWS profile.")
def cli(profile):
    """Webotron deploys websites to AWS."""
    global SESSION, BUCKET_MANAGER, DOMAIN_MANAGER, CERT_MANAGER, DIST_MANAGER 

    session_cfg = {}
    if profile:
        session_cfg['profile_name'] = profile

    SESSION = boto3.Session(**session_cfg)
    BUCKET_MANAGER = BucketManager(SESSION)
    DOMAIN_MANAGER = DomainManager(SESSION)
    CERT_MANAGER = CertificateManager(SESSION)
    DIST_MANAGER = DistributionManager(SESSION)


@cli.command('list-buckets')
def list_buckets():
    """List all S3 buckets."""
    for bucket in BUCKET_MANAGER.all_buckets():
        print(bucket)


@cli.command('list-bucket-objects')
@click.argument('bucket')
def list_bucket_objects(bucket):
    """List objects in an S3 bucket."""
    for obj in BUCKET_MANAGER.all_objects(bucket):
        print(obj)


@cli.command('setup-bucket')
@click.argument('bucket')
def setup_bucket(bucket):
    """Create and configure S3 bucket."""
    s3_bucket = BUCKET_MANAGER.init_bucket(bucket)
    BUCKET_MANAGER.set_policy(s3_bucket)
    BUCKET_MANAGER.configure_website(s3_bucket)


@cli.command('sync')
@click.argument('pathname', type=click.Path(exists=True))
@click.argument('bucket')
def sync(pathname, bucket):
    """Sync contents of PATHNAME to BUCKET."""
    BUCKET_MANAGER.sync(pathname, bucket)
    print(BUCKET_MANAGER.get_bucket_url(BUCKET_MANAGER.s3.Bucket(bucket)))


@cli.command('setup-domain')
@click.argument('domain')
def setup_domain(domain, bucket):
    """Configure DOMAIN to point to BUCKET."""
    bucket = BUCKET_MANAGER.get_bucket(domain)
    zone = DOMAIN_MANAGER.find_hosted_zone(domain) \
        or DOMAIN_MANAGER.create_hosted_zone(domain)

    endpoint = util.get_endpoint(BUCKET_MANAGER.get_region_name(bucket))
    record = DOMAIN_MANAGER.create_s3_domain_record(zone, domain, endpoint)
    print("Domain configured: http://{}".format(domain))


@cli.command('find-cert')
@click.argument('domain')
def find_cert(domain):
    print(CERT_MANAGER.find_matching_cert(domain))


@cli.command('setup-cdn')
@click.argument('domain')
@click.argument('bucket')
def setup_cdn(domain, bucket):
    dist = DIST_MANAGER.find_matching_dist(domain)

    if not dist:
        cert = CERT_MANAGER.find_matching_cert(domain)
        if not cert:
            print("Error: No matching certificate found.")
            return

        dist = DIST_MANAGER.create_dist(domain, cert)
        print("Waiting for deployment ...")
        DIST_MANAGER.await_deploy(dist)

    zone = DOMAIN_MANAGER.find_hosted_zone(domain) \
        or DOMAIN_MANAGER.create_hosted_zone(domain)

    record = DOMAIN_MANAGER.create_cf_domain_record(zone, domain, endpoint)
    print("Domain configured: https://{}".format(domain))

    return


if __name__ == '__main__':
    cli()
