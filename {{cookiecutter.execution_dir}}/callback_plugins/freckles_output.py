# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Inspired from: https://github.com/redhat-openstack/khaleesi/blob/master/plugins/callbacks/human_log.py
# Further improved support Ansible 2.0

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pprint
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from json import JSONEncoder
from uuid import UUID

try:
    import simplejson as json
except ImportError:
    import json

# Fields to reformat output for
ALL_FIELDS = ['cmd', 'command', 'start', 'end', 'delta', 'msg', 'stdout',
          'stderr', 'results']
FIELDS = ['results']


class CallbackModule(object):

    """
    Ansible callback plugin for human-readable result logging
    """
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'stdout'
    CALLBACK_NAME = 'human_log'
    CALLBACK_NEEDS_WHITELIST = False

    def human_log(self, data, entry="n/a", host="n/a"):
        if not data:
            return
            # print("NO DATA: {}".format(entry))
        if type(data) == dict:
            for field in FIELDS:
                no_log = data.get('_ansible_no_log')
                output = self._convert_output(data[field])
                print(json.dumps(output))
                # pprint.pprint(output)

            # for field in ALL_FIELDS:
                # no_log = data.get('_ansible_no_log')
                # if field in data.keys() and data[field] and no_log != True:
                    # output = self._format_output(data[field])
                    # print("FIELD: {}".format(field))
                    # print("ENTRY: {}".format(entry))
                    # print("PLAYBOOK: {}".format(self.playbook._file_name))
                    # print("ENTRIES: {}".format(self.playbook._entries))
                    # print("PLAY: {}".format(self.play))
                    # print("TASK: {}".format(self.task))
                    # print("{0}: {1}\n".format(field, output.replace("\\n","\n")))

    def _parse_role(self):

        role = self.task._role
        result = {}
        result["name"] = role._role_name
        result["path"] = role._role_path
        result["params"] = role._role_params


        return result

    def _parse_task(self):

        result = {}
        result["full_name"] = self.task.get_name()
        result["name"] = self.task.name
        # result["details"] = self.task.serialize()

        return result


    def _parse_play(self):

        result = {}
        result["name"] = self.play.get_name()
        result["vars"] = self.play.get_vars()
        # result["details"] = self.play.serialize()
        # result["play"] = self.play

        return result

    def _convert_output(self, output):

        result = []
        for o in output:
            msg = o.get("msg", "n/a")
            failed = o.get("failed", False)
            changed = o.get("changed", True)
            item = o.get("item", "n/a")

            result.append({"msg": msg, "failed": failed, "changed": changed, "role": self._parse_role(), "play": self._parse_play(), "task": self._parse_task(), "item": item})

        return result

    def _parse_output(self, output):
        # Strip unicode
        if type(output) == unicode:
            output = output.encode(sys.getdefaultencoding(), 'replace')

        # If output is a dict
        if type(output) == dict:
            return self._format_output([output])


        # If output is a list of dicts
        if type(output) == list and type(output[0]) == dict:
            #TODO: verify that this is not totally braindead, too tired at the moment and I don't think this is a case I'll encounter just now. Sorry...
            real_output = list()
            for item in output:
                if type(item) == dict:
                    for field in FIELDS:
                        if field in item.keys():
                            real_output.append(self._parse_output(item[field]))
            return real_output

        return []

    def _format_output(self, output):
        # Strip unicode
        if type(output) == unicode:
            output = output.encode(sys.getdefaultencoding(), 'replace')

        # If output is a dict
        if type(output) == dict:
            return json.dumps(output, indent=2)

        # If output is a list of dicts
        if type(output) == list and type(output[0]) == dict:
            # This gets a little complicated because it potentially means
            # nested results, usually because of with_items.
            real_output = list()
            for index, item in enumerate(output):
                copy = item
                if type(item) == dict:
                    for field in FIELDS:
                        if field in item.keys():
                            copy[field] = self._format_output(item[field])
                real_output.append(copy)
            return json.dumps(output, indent=2)

        # If output is a list of strings
        if type(output) == list and type(output[0]) != dict:
            # Strip newline characters
            real_output = list()
            for item in output:
                if "\n" in item:
                    for string in item.split("\n"):
                        real_output.append(string)
                else:
                    real_output.append(item)

            # Reformat lists with line breaks only if the total length is
            # >75 chars
            if len("".join(real_output)) > 75:
                return "\n" + "\n".join(real_output)
            else:
                return " ".join(real_output)

        # Otherwise it's a string, (or an int, float, etc.) just return it
        return str(output)

    def on_any(self, *args, **kwargs):
        pass

    def runner_on_failed(self, host, res, ignore_errors=False):
        self.human_log(res, "runner_on_failed", host)

    def runner_on_ok(self, host, res):
        self.human_log(res, "runner_on_ok", host)

    def runner_on_skipped(self, host, item=None):
        pass

    def runner_on_unreachable(self, host, res):
        self.human_log(res, "runner_on_unreachable", host)

    def runner_on_no_hosts(self):
        pass

    def runner_on_async_poll(self, host, res, jid, clock):
        self.human_log(res, "runner_on_async_poll", host)

    def runner_on_async_ok(self, host, res, jid):
        self.human_log(res, "runner_on_async_ok")

    def runner_on_async_failed(self, host, res, jid):
        self.human_log(res, "runner_on_async_failed", host)

    def playbook_on_start(self):
        pass

    def playbook_on_notify(self, host, handler):
        pass

    def playbook_on_no_hosts_matched(self):
        pass

    def playbook_on_no_hosts_remaining(self):
        pass

    def playbook_on_task_start(self, name, is_conditional):
        pass

    def playbook_on_vars_prompt(self, varname, private=True, prompt=None, encrypt=None, confirm=False, salt_size=None, salt=None, default=None):
        pass

    def playbook_on_setup(self):
        pass

    def playbook_on_import_for_host(self, host, imported_file):
        pass

    def playbook_on_not_import_for_host(self, host, missing_file):
        pass

    def playbook_on_play_start(self, name):
        pass

    def playbook_on_stats(self, stats):
        pass

    def on_file_diff(self, host, diff):
        pass


    ####### V2 METHODS ######
    def v2_on_any(self, *args, **kwargs):
        pass

    def v2_runner_on_failed(self, result, ignore_errors=False):
        self.human_log(result._result, "v2_runner_on_failed")

    def v2_runner_on_ok(self, result):
        self.human_log(result._result, "v2_runner_on_ok")

    def v2_runner_on_skipped(self, result):
        pass

    def v2_runner_on_unreachable(self, result):
        self.human_log(result._result, "v2_runner_on_unreachable")

    def v2_runner_on_no_hosts(self, task):
        pass

    def v2_runner_on_async_poll(self, result):
        self.human_log(result._result, "v2_runner_on_async_poll")

    def v2_runner_on_async_ok(self, host, result):
        self.human_log(result._result, "v2_runner_on_async_ok", host)

    def v2_runner_on_async_failed(self, result):
        self.human_log(result._result, "v2_runner_on_async_failed")

    def v2_playbook_on_start(self, playbook):
        self.playbook = playbook
        self.human_log(None, "v2_playbook_on_start")

    def v2_playbook_on_notify(self, result, handler):
        self.human_log(result._result, "v2_playbook_on_notify")

    def v2_playbook_on_no_hosts_matched(self):
        pass

    def v2_playbook_on_no_hosts_remaining(self):
        pass

    def v2_playbook_on_task_start(self, task, is_conditional):
        self.task = task

    def v2_playbook_on_vars_prompt(self, varname, private=True, prompt=None,
                                   encrypt=None, confirm=False, salt_size=None,
                                   salt=None, default=None):
        pass

    def v2_playbook_on_setup(self):
        pass

    def v2_playbook_on_import_for_host(self, result, imported_file):
        self.human_log(result._result, "v2_playbook_on_import_for_host")

    def v2_playbook_on_not_import_for_host(self, result, missing_file):
        self.human_log(result._result, "v2_playbook_on_not_import_for_host")

    def v2_playbook_on_play_start(self, play):
        self.play = play

    def v2_playbook_on_stats(self, stats):
        pass

    def v2_on_file_diff(self, result):
        self.human_log(result._result, "v2_on_file_diff")

    def v2_playbook_on_item_ok(self, result):
        self.human_log(result._result, "v2_playbook_on_item_ok")

    def v2_playbook_on_item_failed(self, result):
        self.human_log(result._result, "v2_playbook_on_item_failed")

    def v2_playbook_on_item_skipped(self, result):
        self.human_log(result._result, "v2_playbook_on_item_skipped")

    def v2_playbook_on_include(self, included_file):
        pass

    def v2_playbook_item_on_ok(self, result):
        self.human_log(result._result, "v2_playbook_item_on_ok")

    def v2_playbook_item_on_failed(self, result):
        self.human_log(result._result, "v2_playbook_item_on_failed")

    def v2_playbook_item_on_skipped(self, result):
        self.human_log(result._result, "v2_playbook_item_on_skipped")
