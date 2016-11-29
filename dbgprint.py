
import sys
import os


class DebugStream:
    def __init__(self, stream, prefix=None):
        if prefix is None:
            prefix = ""
        self._prefix = prefix
        self._stream = stream
        self._last_data = None

    def flush(self):
        self._stream.flush()

    def write(self, data):
        from datetime import datetime
        dt = datetime.now()

        #pid = os.getpid()
        pref = '%s %02d:%02d:%03d : ' % (
            self._prefix,
            # str(pid),
            dt.minute,
            dt.second,
            int(dt.microsecond / 1000)
        )
        add_newline = False
        if data.endswith("\n"):
            data = data[:-1]
            add_newline = True

        data = data.replace(
            "\n",
            "\n{}".format(pref)
        )
        if add_newline:
            data += "\n"

        if self._last_data is None or self._last_data.endswith("\n"):
            data = pref + data

        if False:
        #if True:
            with open("/tmp/mydbgoutput_235234.txt", "a") as myfile:
                myfile.write(data)
                myfile.flush()

        self._stream.write(data)
        try:
            self._stream.flush()
        except:
            pass
        self._last_data = data

_sys_stdout_original = sys.stdout
_sys_stderr_original = sys.stderr
_sys_stdin_original = sys.stdin

_enabled = False


def enable_print_dbg(pref=None):
    sys.stdout = DebugStream(
        stream=_sys_stdout_original,
        prefix=pref,
    )
    sys.stderr = DebugStream(
        stream=_sys_stderr_original,
        prefix=pref,
    )
