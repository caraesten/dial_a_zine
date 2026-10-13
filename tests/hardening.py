"""Verify the Docker runtime when launched with the documented hardening flags."""
import errno
import importlib.util
import os
from pathlib import Path

assert os.geteuid() == 10001
assert os.getegid() == 10001
print("PASS: effective UID/GID is 10001")

status = dict(line.split(":", 1) for line in Path("/proc/self/status").read_text().splitlines() if ":" in line)
assert int(status["CapEff"].strip(), 16) == 0
assert status["NoNewPrivs"].strip() == "1"
print("PASS: no effective capabilities; no-new-privileges enabled")

assert Path("/app/dialazine/server.py").stat().st_uid == 0
try:
    with open("/app/runtime-write-test", "w") as handle:
        handle.write("unexpected write access")
except OSError as exc:
    assert exc.errno in (errno.EROFS, errno.EACCES)
    print("PASS: writing to the application directory is blocked")
else:
    raise AssertionError("Application directory was writable")

try:
    with open("/etc/shadow", "rb") as handle:
        handle.read(1)
except PermissionError:
    print("PASS: runtime user cannot read /etc/shadow")
else:
    raise AssertionError("Sensitive file was readable")

for path in ("/app/.git", "/app/default_templates", "/app/dialazine/tools", "/app/dialazine/generate_html.py"):
    assert not Path(path).exists(), path
for package in ("pip", "chevron"):
    assert importlib.util.find_spec(package) is None, package
print("PASS: source-control data, generator and install-only dependencies are absent")
