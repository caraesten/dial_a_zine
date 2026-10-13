## How to run

Use Python 3.13. From the root directory:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python dialazine/server.py
```

To access locally, run

`telnet localhost 8023`

(or equivalent with another telnet client)

The default issue is `example_issue`. Set `CONTENT_FOLDER` to another issue
directory (relative to the repository root, or absolute) and `PORT` to change
the listening port. The default port is now 8023 rather than 23, so a local
server does not need root privileges. `PORT=23` restores the previous port
where the operating system permits it.

## Docker

The image runs only the telnet server; the local install above also includes
the dependencies for the HTML generator.

```sh
docker build -t dial-a-zine .
docker run --rm --name dial-a-zine \
  --read-only --cap-drop ALL --security-opt no-new-privileges=true \
  --memory 128m --pids-limit 64 \
  -p 127.0.0.1:8023:8023 dial-a-zine
```

Connect with `telnet localhost 8023`. To retain host port 23, use
`-p 127.0.0.1:23:8023` instead; the container still listens on an unprivileged
port. Telnet is unencrypted: the examples publish only to localhost, not to
the public network.

To build another issue, make its directory available in the build context:

```sh
docker build --build-arg ISSUE_DIR=my_issue -t dial-a-zine .
```

The selected directory is copied to `/app/issue`, which is the container's
default `CONTENT_FOLDER`. The public example works without fetching the
optional `issue1` submodule. The image copies only runtime code and selected
content, runs as UID/GID 10001, and does not include pip or HTML-generation
dependencies. Runtime files stay root-owned. Read-only storage, capability
restrictions and resource limits require the `docker run` flags above.

The base digest, zlib version and Python dependency hashes are pinned; review
and update these together as patches become available. Pins improve control
over dependencies but do not replace ongoing vulnerability scans.

### Smoke tests

Build the default example image first. The tests run inside a network-isolated
container, connect through its loopback interface and publish no ports:

```sh
docker run -d --name dial-a-zine-test \
  --network none --read-only --cap-drop ALL \
  --security-opt no-new-privileges=true --memory 128m --pids-limit 64 \
  dial-a-zine
docker exec -i dial-a-zine-test python - < tests/session.py
docker exec -i dial-a-zine-test python - < tests/hardening.py
docker stop --timeout 3 dial-a-zine-test
docker rm dial-a-zine-test
```

The session test checks the example welcome, index, both pages of its first
story, return to the index and logout. The hardening test checks the effective
user, capabilities, privilege escalation setting, file permissions and
omission of build-only files. Run the session test once the server logs show
it is listening.

## Zine Structure

In the index.json, the "hello" message is the filepath within the issue folder for what is first displayed,

Then the contents is a list with each article, taking the "title" and "author" for the index, and the "directory" is the folder within the issue folder that contains the article pages - the pages must be called `1.txt`, `2.txt` etc. and will automatically display in that order
