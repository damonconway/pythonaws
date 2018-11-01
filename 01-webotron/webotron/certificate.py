# -*- coding: utf-8 -*-

"""Classes for ACM Certificates."""


class CertificateManager:
    def __init__(self, session):
        self.session = session
        self.client = self.session.client('acm', region_name='us-east-1')

    def cert_matches(self, cert_arn, domain_name):
        """Check to see if a cert support a domain name."""
        cert_details = self.client.describe_certificate(CertificateArn=cert_arn)
        alt_names = cert_details['Certificate']['SubjectAlternativeNames']
        for name in alt_names:
            if name == domain_name:
                return True
            elif name[0] == '*' and domain_name.endswith(name[1:]):
                return True
        return False

    def find_matching_cert(self, domain_name):
        """Find ACM cert from domain name."""
        paginator = self.client.get_paginator('list_certificates')
        for page in paginator.paginate(CertificateStatuses=['ISSUED']):
            for cert in page['CertificateSummaryList']:
                if self.cert_matches(cert['CertificateArn'], domain_name):
                    return cert
