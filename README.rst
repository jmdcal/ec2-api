OpenStack EC2 API README
-----------------------------

Support of EC2 API for OpenStack.
This project provides a standalone EC2 API service which pursues two goals:
 1. Implement VPC API which is now absent in nova's EC2 API
 2. Create a standalone service for EC2 API support which accommodates
not only the VPC API but the rest of the EC2 API currently present in nova as
well.

It doesn't replace existing nova EC2 API service in deployment, it gets
installed to a different port (8788 by default).

Installation
=====

Run install.sh

The EC2 API service gets installed on port 8788 by default. It can be changed
before the installation in install.sh script.

The services afterwards can be started as binaries:

::

 /usr/bin/ec2-api
 /usr/bin/ec2-api-metadata

or set up as Linux services.

To configure OpenStack for EC2 API metadata service:

for Nova-network
  add::

    [DEFAULT]
    metadata_port = 8789
    [neutron]
    service_metadata_proxy = True

  to /etc/nova.conf

  then restart nova-metadata (can be run as part of nova-api service) and
  nova-network services.

for Neutron
  add::

    [DEFAULT]
    nova_metadata_port = 8789

  to /etc/neutron/metadata_agent.ini

  then restart neutron-metadata service.

Usage
=====

Download aws cli from Amazon.
Create configuration file for aws cli in your home directory ~/.aws/config:

::

 [default]
 aws_access_key_id = 1b013f18d5ed47ae8ed0fbb8debc036b
 aws_secret_access_key = 9bbc6f270ffd4dfdbe0e896947f41df3
 region = us-east-1

Change the aws_access_key_id and aws_secret_acces_key above to the values
appropriate for your cloud (can be obtained by "keystone ec2-credentials-list"
command).

Run aws cli commands using new EC2 API endpoint URL (can be obtained from
keystone with the new port 8788) like this:

aws --endpoint-url http://10.0.2.15:8788/services/Cloud ec2 describe-instances


Limitations
===========

General:
- DryRun option is not supported.
- Some exceptions are not exactly the same as reported by AWS.

Not supported functionality features:
- VPN
- Network ACL
- VPC Peering connection
- Classic Link
- Reserved Instances
- Spot Instances
- Placement Groups
- Monitoring Instances and Volumes
- Instances Tasks - Bundle, Export, Import

Availability zone related:
- messages AvailabilityZone property
- regionName AvailabilityZone property

Image related:
- CopyImage
- ResetImageAttribute
- creationDate  Image property
- platform Image property
- productCodes Image property
- description Image property
- hypervisor Image property
- imageOwnerAlias Image property
- sriovNetSupport Image property
- stateReason Image property
- virtualizationType Image property
- encrypted EbsBlockDevice property
- iops EbsBlockDevice property
- volumeType EbsBlockDevice property
- selective filtering by Image Owner

Instance related:
- DescribeInstanceStatus
- ReportInstanceStatus
- ModifyInstanceAttribute
- ResetInstanceAttribute
- productCodes Instance property
- sourceDestCheck Instance property
- ebsOptimized Instance property
- sriovNetSupport Instance property
- monitoring Instance property
- placement Instance property
- platform Instance property
- publicDnsName Instance property
- stateTransitionReason Instance property
- architecture Instance property
- ebsOptimized Instance property
- hypervisor Instance property
- iamInstanceProfile Instance property
- instanceLifecycle Instance property
- spotInstanceRequestId Instance property
- stateReason Instance property
- virtualizationType Instance property
- attachTime EbsInstanceBlockDevice property

Network interface related:
- availabilityZone NetworkInterface property
- deleteOnTermination (modification is not supported)

Snapshot related:
- CopySnapshot
- ModifySnapshotAttribute
- ResetSnapshotAttribute
- encryption Snapshot property
- kmsKeyId Snapshot property
- ownerAlias Snapshot property
- selective filtering by Snapshot Owner, RestorableBy

Subnet related:
- ModifySubnetAttribute
- availabilityZone Subnet property
- defaultForAz Subnet property
- mapPublicIpOnLaunch Subnet property

Volume related:
- DescribeVolumeAttribute
- DescribeVolumeStatus
- ModifyVolumeAttribute
- kmsKeyId Volume property
- iops Volume property
- deleteOnTermination property (supported for describing instances only)
- volumeType (current implementation isn't AWS compatible) Volume property

VPC related:
- describeVpcAttribute
- modifyVpcAttribute
- instanceTenancy VPC property

DescribeAccountAttributes result properties:
- pc-max-security-groups-per-interface AccountAttribute property
- max-elastic-ips AccountAttribute property
- vpc-max-elastic-ips AccountAttribute property

Supported Features
==================

EC2 API with VPC API except for the limitations above.

Additions to the legacy nova's EC2 API include:
1. VPC API
2. Filtering
3. Tags

References
==========

Blueprint:
https://blueprints.launchpad.net/nova/+spec/ec2-api

Spec:
https://review.openstack.org/#/c/147882/
