# Deploy

The app runs on **kimlab**, a private machine reachable only over Tailscale.
Two environments live side by side on it:

| Environment | Trigger | Port |
|---|---|---|
| staging | automatic, after every merge to `main` | 8101 |
| production | manual button in the pipeline | 8100 |

## How a deploy job works

1. The job runs on a GitLab shared runner and installs Tailscale.
2. It joins the tailnet with `TS_AUTHKEY`. That key carries `tag:ci`, and the
   tailnet policy lets `tag:ci` reach only the SSH port of kimlab.
3. It SSHes in with `DEPLOY_SSH_KEY_B64`. On kimlab that key is forced to run a
   single script, so the job can only say `<environment> <image tag>`.
4. The script pulls `registry.gitlab.com/.../demo-devsecops:<tag>`, restarts the
   stack, waits for the health checks and runs a smoke test. If any of that
   fails, the job fails.

The compose file and the script are kept on kimlab, not in this repository.
Whoever can push here decides *which image* runs, but not *how* it is run.

## CI/CD variables (Settings > CI/CD > Variables)

| Variable | What it is |
|---|---|
| `TS_AUTHKEY` | Tailscale auth key: ephemeral, reusable, tagged `tag:ci` |
| `DEPLOY_SSH_KEY_B64` | base64 of the restricted SSH private key |
| `KIMLAB_KNOWN_HOSTS` | pinned SSH host key of kimlab |
| `KIMLAB_IP` | Tailscale IP of kimlab |

## Roll back

Open **Operate > Environments**, pick the environment, and press **Re-deploy**
on an older deployment. The old image is still in the Container Registry under
its commit tag.
