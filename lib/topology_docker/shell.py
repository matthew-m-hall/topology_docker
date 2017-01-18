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
Docker shell helper class module.
"""

from __future__ import unicode_literals, absolute_import
from __future__ import print_function, division

from topology.platforms.shell import PExpectShell, PExpectBashShell


class DockerShell(PExpectShell):
    """
    Generic ``docker exec`` shell for unspecified interactive session.
    """


class DockerBashShell(PExpectBashShell):
    """
    Specialized ``docker exec`` shell that will run and setup a bash
    interactive session.
    """


class DockerBashFrontPanelShell(DockerBashShell):
    """
    Openswitch Telnet-connected ``bash`` ``swns`` shell.

    This shell spawns a ``bash`` shell inside the ``swns`` network namespace.
    """

    def __init__(self):
        self._start_command = 'ip netns exec front_panel bash'

        super(DockerBashFrontPanelShell, self).__init__()

    def enter(self):
        """
        see :meth:`topology.platforms.shell.BaseShell.enter` for more
        information.
        """
        spawn = self._parent_connection._spawn
        spawn.sendline(self._start_command)
        spawn.expect(self._prompt)

    def exit(self):
        """
        see :meth:`topology.platforms.shell.BaseShell.exit` for more
        information.
        """
        spawn = self._parent_connection._spawn
        spawn.sendline('exit')
        spawn.expect(self._prompt)

    def _setup_shell(self):
        """
        See :meth:`topology.platforms.shell.BaseShell._setup_shell` for more
        information.
        """

        super(DockerBashFrontPanelShell, self)._setup_shell()

        spawn = self._parent_connection._spawn
        spawn.sendline(self._start_command)
        spawn.expect(self._initial_prompt)

        # some docker images have an issue where subshells dont inherit
        # the environment, so we call setup_shell again
        super(DockerBashFrontPanelShell, self)._setup_shell()


__all__ = ['DockerShell', 'DockerBashShell']
