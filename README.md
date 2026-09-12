# Unraid templates

Unraid container templates for [Traefik Manager](https://github.com/chr0nzz/traefik-manager), a web UI for managing Traefik routes, services, middlewares and certificates.

| Template | App |
|---|---|
| [`templates/traefik-manager.xml`](templates/traefik-manager.xml) | Traefik Manager |

## Install

Run this on your Unraid server:

```bash
wget -O /boot/config/plugins/dockerMan/templates-user/my-traefik-manager.xml \
  https://raw.githubusercontent.com/chr0nzz/unraid-templates/main/templates/traefik-manager.xml
```

Then open the **Docker** tab, click **Add Container**, and pick **traefik-manager** from the **Template** dropdown under *User templates*.

Run the same command again to pick up new fields added to the template.

## Configuration

Every field maps to an environment variable. The [Unraid guide](https://traefik-manager.xyzlab.dev/unraid.html) covers what to set, which paths to mount for the optional tabs, and how to reach the Traefik API. The [environment variable reference](https://traefik-manager.xyzlab.dev/env-vars.html) lists them all with defaults.

## Support

Issues and questions belong on the [Traefik Manager tracker](https://github.com/chr0nzz/traefik-manager/issues).

## License

GPL-3.0, see [LICENSE](LICENSE).
