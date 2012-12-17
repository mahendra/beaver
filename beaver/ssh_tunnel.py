import os
import signal
import subprocess


class BeaverSubprocess:

    def __init__(self, beaver_config):
        # Child classes should build a subprocess via the following method:
        #
        #   self._subprocess = subprocess.Popen(cmd, stdout=subprocess.PIPE, preexec_fn=os.setsid)
        #
        # This will allow us to attach a session id to the spawned child, allowing
        # us to send a SIGTERM to the process on close
        self._subprocess = None

    def poll(self):
        if self._subprocess is not None:
            self._subprocess.poll()

    def close(self):
        if self._subprocess is not None:
            os.killpg(self._subprocess.pid, signal.SIGTERM)
            self._subprocess = None


class BeaverSshTunnel(BeaverSubprocess):

    def __init__(self, beaver_config):
        key_file = beaver_config.get('ssh_key_file')
        tunnel = beaver_config.get('ssh_tunnel')
        tunnel_port = beaver_config.get('ssh_tunnel_port')
        remote_host = beaver_config.get('ssh_remote_host')
        remote_port = beaver_config.get('ssh_remote_port')

        self._subprocess = subprocess.Popen(["ssh", "-i", key_file, "-f", tunnel, "-L",
            "{0}:{1}:{2}".format(tunnel_port, remote_host, remote_port),
            "sleep 5"], stdout=subprocess.PIPE, preexec_fn=os.setsid)
        self.poll()
