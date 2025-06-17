from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.plugins.callback import CallbackBase
import os
import sys

class CallbackModule(CallbackBase):
    """
    This callback plugin logs when a playbook starts and ends, using a user-provided name.
    """

    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'notification'
    CALLBACK_NAME = 'notify_user'

    def __init__(self):
        super(CallbackModule, self).__init__()
        self.user_name = os.environ.get('ANSIBLE_USER_NAME')
        self.playbook_name = "UNKNOWN"

        # Only ask for name if not set in env (interactive mode)
        if not self.user_name:
            try:
                # Print to stderr so it doesn't interfere with stdout_callback behavior
                sys.stderr.write("Enter your name: ")
                sys.stderr.flush()
                self.user_name = sys.stdin.readline().strip()
                if not self.user_name:
                    self.user_name = "Unknown"
                os.environ['ANSIBLE_USER_NAME'] = self.user_name
            except Exception:
                self.user_name = "Unknown"

    def v2_playbook_on_start(self, playbook):
        try:
            self.playbook_name = os.path.basename(getattr(playbook, '_file_name', 'UNKNOWN'))
        except Exception:
            self.playbook_name = "UNKNOWN"

        msg = f"{self.user_name} is executing the Playbook {self.playbook_name}"
        self._display.banner(msg)

    def v2_playbook_on_stats(self, stats):
        msg = f"{self.user_name} has finished executing the Playbook {self.playbook_name}"
        self._display.banner(msg)