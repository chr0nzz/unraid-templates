# Unraid templates

Unraid container templates for [Traefik Manager](https://github.com/chr0nzz/traefik-manager), a web UI for managing Traefik routes, services, middlewares and certificates.

| Template | App |
|---|---|
| [`templates/traefik-manager.xml`](templates/traefik-manager.xml) | Traefik Manager |
| [`templates/traefik-manager-agent.xml`](templates/traefik-manager-agent.xml) | Traefik Manager agent, to manage this server from a Traefik Manager running elsewhere |

## Install

Run this on your Unraid server:

```bash
wget -O /boot/config/plugins/dockerMan/templates-user/my-traefik-manager.xml \
  https://raw.githubusercontent.com/chr0nzz/unraid-templates/main/templates/traefik-manager.xml
```

For the agent instead:

```bash
wget -O /boot/config/plugins/dockerMan/templates-user/my-traefik-manager-agent.xml \
  https://raw.githubusercontent.com/chr0nzz/unraid-templates/main/templates/traefik-manager-agent.xml
```

Then open the **Docker** tab, click **Add Container**, and pick the template from the **Template** dropdown under *User templates*.

Run the same command again to pick up new fields added to a template.

## Which one do I want?

**Traefik Manager** is the app itself, with the web UI. Install this if Traefik runs on this Unraid server and you want to manage it here.

**Traefik Manager agent** has no UI. Install it when Traefik runs on this server but you manage it from a Traefik Manager on another machine. Add the server in that Traefik Manager under **Settings - Agents** to generate an API key, then paste the key into the template.

## Configuration

Every field maps to an environment variable. The [Unraid guide](https://traefik-manager.xyzlab.dev/unraid.html) covers what to set, which paths to mount for the optional tabs, and how to reach the Traefik API. The [environment variable reference](https://traefik-manager.xyzlab.dev/env-vars.html) lists them all with defaults.

## Support

Issues and questions belong on the [Traefik Manager tracker](https://github.com/chr0nzz/traefik-manager/issues).

## License

GPL-3.0, see [LICENSE](LICENSE).
