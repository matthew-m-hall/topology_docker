# -*- coding: utf-8 -*-
#
# Copyright (C) 2015-2016 Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""
topology_docker base connection module.
"""

from __future__ import unicode_literals, absolute_import
from __future__ import print_function, division

from logging import getLogger

from topology.platforms.connection import CommonConnection

log = getLogger(__name__)


class DockerConnection(CommonConnection):
    """
    Docker ``exec`` connection for the Topology docker.

    This class implements a ``_get_connect_command()`` method that allows to
    interact with a shell through a ``docker exec`` interactive command, and
    extends the constructor to request for container related parameters.

    :param str container: Container unique identifier.
    :param str command: Command to be executed with the ``docker exec`` that
     will launch an interactive session.
    """

    def __init__(self, identifier, parent_node, **kwargs):
        self._container_id = parent_node.container_id
        super(DockerConnection, self).__init__(
            identifier, parent_node, initial_prompt='(^|\n).*[#$] ',
            **kwargs)

    def _get_connect_command(self):
        return 'docker exec -i -t {} bash'.format(
            self._container_id
        )


class DockerSSHConnection(CommonConnection):
    """
    SSH engine connection class

    This will create an SSH connection for the given user with the
    following SSH options:

     1. StrictHostKeyChecking=no
     2. UserKnownHostsFile=/dev/null
    """

    def __init__(self, identifier, parent_node, ip_address,
                 ip_port='22', initial_prompt='\n.+?@.+?[#$]',
                 *args, **kwargs):
        super(DockerSSHConnection, self).__init__(
            identifier, parent_node, initial_prompt=initial_prompt,
            *args, **kwargs
        )

        # user is sent in the ssh command
        # this disables the user prompt check
        self._user_match = None
        self._ip_address = ip_address
        self._ip_port = ip_port

    def _get_connect_command(self):
        """
        Get the command to be used when connecting to the node.

        :rtype: str
        :return: The command to be used when connecting to the node.
        """

        return (
            'ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null'
            ' {}@{} -p {}'.format(self._user, self._ip_address, self._ip_port)
        )


__all__ = ['DockerConnection']
