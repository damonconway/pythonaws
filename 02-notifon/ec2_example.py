# coding: utf-8
import boto3
session = boto3.Session(profile_name='pythonAutomation'
)
ec2 = session.resource('ec2')
key_name = 'python_automation_key'
key_path = key_name + '.pem'
key = ec2.create_key_pair(KeyName=key_name)
key.key_material
with open(key_path, 'w') as key_file:
    key_file.write(key.key_material)
    
get_ipython().run_line_magic('ls', '-l python_automation_key.pem')
chmod 600 python_automation_key.pem
import os, stat
os.chmod(key_path, stat.S_IRUSR | stat.S_IWUSR)
get_ipython().run_line_magic('ls', '-l python_automation_key.pem')
img = ec2.Image('ami-013be31976ca2c322')
img.name
img
instances = ec2.create_instances(ImageId=img.id, MinCount=1, MaxCount=1, InstanceType='t2.micro', KeyName=key.key_name)
inst = instances[0]
inst.public_dns_name
inst.reload
inst.public_dns_name
inst.wait_until_running()
inst.public_dns_name
inst.reload
inst.reload()
inst.public_dns_name
inst.security_groups
inst.id
ec2.create_security_group(Description='Allow SSH from home', GroupName='home_ssh', VpcId=inst.id)
inst.vpc_id
ec2.create_security_group(Description='Allow SSH from home', GroupName='home_ssh', VpcId=inst.vpc_id)
sg = ec2.SecurityGroup(id='sg-0da060a46f76d89ac')
sg
response = sg.authorize_ingress(
CidrIp='76.72.151.27/32',
FromPort=22)
response = sg.authorize_ingress(
CidrIp='76.72.151.27/32',
FromPort=22,
ToPort=22,
Protocol='tcp'
)
response = sg.authorize_ingress(
CidrIp='76.72.151.27/32',
FromPort=22,
ToPort=22,
IpProtocol='tcp')
response
inst.security_groups
sg.terminate
sg.delete()
sg = ec2.SecurityGroup(inst.security_groups[0]['GroupId'])
sg.authorize_ingress(IpPermissions=[{'FromPort': 22, 'ToPort': 22, 'IpProtocol': 'TCP', 'IpRanges': [{'CidrIp': '76.72.151.27/32'}]}])
sg.authorize_ingress(IpPermissions=[{'FromPort': 80, 'ToPort': 80, 'IpProtocol': 'TCP', 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}])
