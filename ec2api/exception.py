# Copyright 2014
# The Cloudscaling Group, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""ec2api base exception handling.

Includes decorator for re-raising ec2api-type exceptions.

SHOULD include dedicated exception logging.

"""

import sys

from oslo_config import cfg
from oslo_log import log as logging
import six

from ec2api.i18n import _

LOG = logging.getLogger(__name__)

exc_log_opts = [
    cfg.BoolOpt('fatal_exception_format_errors',
                default=False,
                help='Make exception message format errors fatal'),
]

CONF = cfg.CONF
CONF.register_opts(exc_log_opts)


class EC2MetadataException(Exception):
    pass


class EC2MetadataNotFound(EC2MetadataException):
    pass


class EC2MetadataInvalidAddress(EC2MetadataException):
    pass


class EC2Exception(Exception):
    """Base EC2 Exception

    To correctly use this class, inherit from it and define
    a 'msg_fmt' property. That msg_fmt will get printf'd
    with the keyword arguments provided to the constructor.

    """
    msg_fmt = _("An unknown exception occurred.")
    code = 400
    headers = {}
    safe = False

    def __init__(self, message=None, **kwargs):
        self.kwargs = kwargs

        if 'code' not in self.kwargs:
            try:
                self.kwargs['code'] = self.code
            except AttributeError:
                pass

        if not message:
            try:
                message = self.msg_fmt % kwargs
            except Exception:
                exc_info = sys.exc_info()
                # kwargs doesn't match a variable in the message
                # log the issue and the kwargs
                LOG.exception(_('Exception in string format operation for '
                                '%s exception'), self.__class__.__name__)
                for name, value in kwargs.iteritems():
                    LOG.error("%s: %s" % (name, value))

                if CONF.fatal_exception_format_errors:
                    raise exc_info[0], exc_info[1], exc_info[2]
                else:
                    # at least get the core message out if something happened
                    message = self.msg_fmt
        elif not isinstance(message, six.string_types):
            LOG.error(_("Message '%(msg)s' for %(ex)s exception is not "
                        "a string"),
                      {'msg': message, 'ex': self.__class__.__name__})
            if CONF.fatal_exception_format_errors:
                raise TypeError(_('Invalid exception message format'))
            else:
                message = self.msg_fmt

        super(EC2Exception, self).__init__(message)

    def format_message(self):
        # NOTE(mrodden): use the first argument to the python Exception object
        # which should be our full EC2Exception message, (see __init__)
        return self.args[0]


class Unsupported(EC2Exception):
    msg_fmt = _("The specified request is unsupported. %(reason)s")


class Overlimit(EC2Exception):
    msg_fmt = _("Limit exceeded.")


class Invalid(EC2Exception):
    msg_fmt = _("Unacceptable parameters.")


class InvalidRequest(Invalid):
    msg_fmt = _("The request is invalid.")


class InvalidAttribute(Invalid):
    msg_fmt = _("Attribute not supported: %(attr)s")


class InvalidID(Invalid):
    msg_fmt = _("The ID '%(id)s' is not valid")


class InvalidInput(Invalid):
    msg_fmt = _("Invalid input received: %(reason)s")


class ConfigNotFound(EC2Exception):
    msg_fmt = _("Could not find config at %(path)s")


class PasteAppNotFound(EC2Exception):
    msg_fmt = _("Could not load paste app '%(name)s' from %(path)s")


class Forbidden(EC2Exception):
    ec2_code = 'AuthFailure'
    msg_fmt = _("Not authorized.")
    code = 403


class AuthFailure(Invalid):
    pass


class ValidationError(Invalid):
    msg_fmt = _("The input fails to satisfy the constraints "
                "specified by an AWS service: '%(reason)s'")


class EC2NotFound(EC2Exception):
    msg_fmt = _("Resource could not be found.")


class InvalidInstanceIDNotFound(EC2NotFound):
    ec2_code = 'InvalidInstanceID.NotFound'
    msg_fmt = _("The instance ID '%(id)s' does not exist")


class InvalidVpcIDNotFound(EC2NotFound):
    ec2_code = 'InvalidVpcID.NotFound'
    msg_fmt = _("The vpc ID '%(id)s' does not exist")


class InvalidInternetGatewayIDNotFound(EC2NotFound):
    ec2_code = 'InvalidInternetGatewayID.NotFound'
    msg_fmt = _("The internetGateway ID '%(id)s' does not exist")


class InvalidSubnetIDNotFound(EC2NotFound):
    ec2_code = 'InvalidSubnetID.NotFound'
    msg_fmt = _("The subnet ID '%(id)s' does not exist")


class InvalidNetworkInterfaceIDNotFound(EC2NotFound):
    ec2_code = 'InvalidNetworkInterfaceID.NotFound'
    msg_fmt = _("Network interface %(id)s could not "
                "be found.")


class InvalidAttachmentIDNotFound(EC2NotFound):
    ec2_code = 'InvalidAttachmentID.NotFound'
    msg_fmt = _("Attachment %(id)s could not "
                "be found.")


class InvalidDhcpOptionsIDNotFound(EC2NotFound):
    ec2_code = 'InvalidDhcpOptionsID.NotFound'
    msg_fmt = _("The dhcp options ID '%(id)s' does not exist")


class InvalidAllocationIDNotFound(EC2NotFound):
    ec2_code = 'InvalidAllocationID.NotFound'
    msg_fmt = _("The allocation ID '%(id)s' does not exist")


class InvalidAssociationIDNotFound(EC2NotFound):
    ec2_code = 'InvalidAssociationID.NotFound'
    msg_fmt = _("The association ID '%(id)s' does not exist")


class InvalidRouteTableIDNotFound(EC2NotFound):
    ec2_code = 'InvalidRouteTableID.NotFound'
    msg_fmt = _("The routeTable ID '%(id)s' does not exist")


class InvalidRouteNotFound(EC2NotFound):
    ec2_code = 'InvalidRoute.NotFound'
    msg_fmt = _('No route with destination-cidr-block '
                '%(destination_cidr_block)s in route table %(route_table_id)s')


class InvalidSecurityGroupIDNotFound(EC2NotFound):
    ec2_code = 'InvalidSecurityGroupID.NotFound'
    msg_fmt = _("The securityGroup ID '%(id)s' does not exist")


class InvalidGroupNotFound(EC2NotFound):
    ec2_code = 'InvalidGroup.NotFound'
    msg_fmg = _("The security group ID '%(id)s' does not exist")


class InvalidPermissionNotFound(EC2NotFound):
    ec2_code = 'InvalidPermission.NotFound'
    msg_fmg = _("The specified permission does not exist")


class InvalidVolumeNotFound(EC2NotFound):
    ec2_code = 'InvalidVolume.NotFound'
    msg_fmt = _("The volume '%(id)s' does not exist.")


class InvalidSnapshotNotFound(EC2NotFound):
    ec2_code = 'InvalidSnapshot.NotFound'
    msg_fmt = _("Snapshot %(id)s could not be found.")


class InvalidAMIIDNotFound(EC2NotFound):
    ec2_code = 'InvalidAMIID.NotFound'
    msg_fmt = _("The image id '[%(id)s]' does not exist")


class InvalidKeypairNotFound(EC2NotFound):
    ec2_code = 'InvalidKeyPair.NotFound'
    msg_fmt = _("Keypair %(id)s is not found")


class InvalidAvailabilityZoneNotFound(EC2NotFound):
    ec2_code = 'InvalidAvailabilityZone.NotFound'
    msg_fmt = _("Availability zone %(id)s not found")


class IncorrectState(EC2Exception):
    ec2_code = 'IncorrectState'
    msg_fmt = _("The resource is in incorrect state for the request - reason: "
                "'%(reason)s'")


class IncorrectInstanceState(IncorrectState):
    ec2_code = 'IncorrectInstanceState'
    msg_fmt = _("The instance '%(instance_id)s' is not in a state from which "
                "the requested operation can be performed.")


class InvalidVpcRange(Invalid):
    ec2_code = 'InvalidVpc.Range'
    msg_fmt = _("The CIDR '%(cidr_block)s' is invalid.")


class InvalidSubnetRange(Invalid):
    ec2_code = 'InvalidSubnet.Range'
    msg_fmt = _("The CIDR '%(cidr_block)s' is invalid.")


class InvalidSubnetConflict(Invalid):
    ec2_code = 'InvalidSubnet.Conflict'
    msg_fmt = _("The CIDR '%(cidr_block)s' conflicts with another subnet")


class MissingParameter(Invalid):
    msg_fmt = _("The required parameter '%(param)s' is missing")


class InvalidParameter(Invalid):
    msg_fmt = _("The property '%(name)s' is not valid")


class InvalidParameterValue(Invalid):
    msg_fmt = _("Value (%(value)s) for parameter %(parameter)s is invalid. "
                "%(reason)s")


class InvalidParameterCombination(Invalid):
    pass


class UnsupportedOperation(Invalid):
    pass


class OperationNotPermitted(Invalid):
    pass


class ResourceAlreadyAssociated(Invalid):
    ec2_code = 'Resource.AlreadyAssociated'


class GatewayNotAttached(Invalid):
    ec2_code = 'Gateway.NotAttached'
    msg_fmt = _("resource %(igw_id)s is not attached to network %(vpc_id)s")


class DependencyViolation(Invalid):
    msg_fmt = _('Object %(obj1_id)s has dependent resource %(obj2_id)s')


class InvalidNetworkInterfaceInUse(Invalid):
    ec2_code = 'InvalidNetworkInterface.InUse'
    msg_fmt = _('Interface: %(interface_ids)s in use.')


class InvalidInstanceId(Invalid):
    ec2_code = 'InvalidInstanceID'
    msg_fmt = _("There are multiple interfaces attached to instance "
                "'%(instance_id)s'. Please specify an interface ID for "
                "the operation instead.")


class InvalidIPAddressInUse(Invalid):
    ec2_code = 'InvalidIPAddress.InUse'
    msg_fmt = _('Address %(ip_address)s is in use.')


class InvalidAddressNotFound(Invalid):
    ec2_code = 'InvalidAddress.NotFound'
    msg_fmt = _('The specified elastic IP address %(ip)s cannot be found.')


class RouteAlreadyExists(Invalid):
    msg_fmt = _('The route identified by %(destination_cidr_block)s '
                'already exists.')


class VpcLimitExceeded(Overlimit):
    msg_fmt = _('The maximum number of VPCs has been reached.')


class SubnetLimitExceeded(Overlimit):
    msg_fmt = _('You have reached the limit on the number of subnets that you '
                'can create')


class NetworkInterfaceLimitExceeded(Overlimit):
    msg_fmt = _('You have reached the limit of network interfaces for subnet'
                '%(subnet_id)s.')


class ResourceLimitExceeded(Overlimit):
    msg_fmt = _('You have reached the limit of %(resource)s')


class SecurityGroupLimitExceeded(Overlimit):
    msg_fmt = _('You have reached the limit of security groups')


class AddressLimitExceeded(Overlimit):
    msg_fmt = _('The maximum number of addresses has been reached.')


class ImageNotActive(Invalid):
    ec2_code = 'InvalidAMIID.Unavailable'
    # TODO(ft): Change the message with the real AWS message
    msg_fmt = _("Image %(image_id)s is not active.")


class InvalidSnapshotIDMalformed(Invalid):
    ec2_code = 'InvalidSnapshotID.Malformed'
    # TODO(ft): Change the message with the real AWS message
    msg_fmg = _('The snapshot %(id)s ID is not valid')


class InvalidKeyPairDuplicate(Invalid):
    ec2_code = 'InvalidKeyPair.Duplicate'
    msg_fmt = _("Key pair '%(key_name)s' already exists.")


class InvalidPermissionDuplicate(Invalid):
    ec2_code = 'InvalidPermission.Duplicate'
    msg_fmt = _("The specified rule already exists for that security group.")


class InvalidFilter(Invalid):
    msg_fmt = _("The filter is invalid.")


class RulesPerSecurityGroupLimitExceeded(Overlimit):
    msg_fmt = _("You've reached the limit on the number of rules that "
                "you can add to a security group.")


class NovaDbInstanceNotFound(EC2Exception):
    code = 500
