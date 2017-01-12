# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import json

import logging
import logging.handlers
import pprint
import socket

from ansible.plugins.callback import CallbackBase

class CallbackModule(CallbackBase):
    """
    logs ansible-playbook and ansible runs to a syslog server in json format
    make sure you have in ansible.cfg:
        callback_plugins   = <path_to_callback_plugins_folder>
    and put the plugin in <path_to_callback_plugins_folder>

    This plugin makes use of the following environment variables:
        SYSLOG_SERVER   (optional): defaults to localhost
        SYSLOG_PORT     (optional): defaults to 514
        SYSLOG_FACILITY (optional): defaults to user
    """
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'aggregate'
    CALLBACK_NAME = 'syslog_json'
    CALLBACK_NEEDS_WHITELIST = True

    def __init__(self):

        super(CallbackModule, self).__init__()

    def print_to_stdoutout(self, status, msg):
        print("Status: {}".format(status))
        pprint.pprint(json.dumps(msg))
        print()

    def runner_on_failed(self, host, res, ignore_errors=False):
        self._dump_results('FAILED', res)
        # self.self.print_to_stdoutout('ansible-command: task execution FAILED; message: %s' % (self._dump_results(res)))

    def runner_on_ok(self, host, res):
        self.print_to_stdoutout('OK', res)

    def runner_on_skipped(self, host, item=None):
        self.print_to_stdoutout('SKIPPED', res)


    def runner_on_unreachable(self, host, res):
        self.print_to_stdoutout('UNREACHABLE', res)


    def runner_on_async_failed(self, host, res, jid):
        self.print_to_stdoutout('FAILED', res)


    def playbook_on_import_for_host(self, host, imported_file):
        self.print_to_stdoutout('IMPORT_FOR_HOST', res)


    def playbook_on_not_import_for_host(self, host, missing_file):
        self.print_to_stdoutout('NOT_IMPORT_FOR_HOST', res)


    def v2_runner_on_skipped(self, res):
        self.print_to_stdoutout('V2_SKIPPED', res)
