# Traefik Manager for Unraid

<img src="https://raw.githubusercontent.com/chr0nzz/unraid-templates/main/icon.png" alt="Traefik Manager" width="96" align="right">

[Traefik Manager](https://github.com/chr0nzz/traefik-manager) is a web UI for managing Traefik routes, services, middlewares and certificates. It edits your Traefik dynamic config directly, so routes you create in the UI are ordinary YAML you can read, back up and revert.

Both apps are in Unraid Community Applications. Open the **Apps** tab, search for **Traefik Manager** and click **Install**.

| App | Community Applications |
|---|---|
| Traefik Manager | [traefik-manager](https://ca.unraid.net/apps/traefik-manager-07006dq0obycuq) |
| Traefik Manager agent | [traefik-manager-agent](https://ca.unraid.net/apps/traefik-manager-agent-0hwaq5u1sy2tzy) |

## Which one do I want?

**Traefik Manager** is the app itself, with the web UI. Install this if Traefik runs on this Unraid server and you want to manage it here.

**Traefik Manager agent** has no UI. Install it when Traefik runs on this server but you manage it from a Traefik Manager on another machine. Add the server in that Traefik Manager under **Settings - Agents** to generate an API key, then paste the key into the template.

## Features

- **Routes** - HTTP, TCP and UDP routes with multiple domains and backends, sticky sessions, health checks, certificate resolvers and TLS options
- **Services** - load balancer, weighted, mirroring and failover services
- **Middlewares** - 30 guided wizards for auth, rate limiting, headers, CORS, redirects and more, plus a raw YAML editor
- **Dashboard and Route Map** - your apps with icons and health, and a topology map from entry point to backend
- **Certificates** - every certificate in `acme.json` with expiry, unused certificates and orphaned resolvers
- **Monitoring** - live router and service health from the Traefik API, provider tabs and CVE advisories for your Traefik version
- **Logs and CrowdSec** - access log analytics, CrowdSec attacks, bans and decisions
- **Notifications** - Discord, Slack, ntfy, Gotify, Pushover, Pushbullet, Telegram, UnifiedPush and webhooks, with background checks when the UI is closed
- **Static config editor** - edit `traefik.yml` and restart Traefik from the UI
- **Plugins** - install Traefik plugins and see which middlewares use them
- **Backups** - a local backup before every change, plus git push with history, diffs and restore
- **Multi-server** - manage Traefik on other hosts through the agent, no VPN or SSH
- **Security** - two-factor login, OIDC single sign-on, per-device API keys and secrets encrypted at rest
- **Mobile** - a native [Android app](https://play.google.com/store/apps/details?id=dev.chr0nzz.traefikmanager), and the web app installs as a PWA

## Configuration

Every template field maps to an environment variable. The [Unraid guide](https://traefik-manager.xyzlab.dev/unraid.html) covers what to set, which paths to mount for the optional tabs, and how to reach the Traefik API. The [environment variable reference](https://traefik-manager.xyzlab.dev/env-vars.html) lists them all with defaults.

The full documentation is at [traefik-manager.xyzlab.dev](https://traefik-manager.xyzlab.dev/).

## Help and issues

- **Bugs and feature requests** - open an issue on the [Traefik Manager tracker](https://github.com/chr0nzz/traefik-manager/issues)
- **Questions** - check the [documentation](https://traefik-manager.xyzlab.dev/) first, then ask on the [tracker](https://github.com/chr0nzz/traefik-manager/issues)
- **Template problems** - a missing field, wrong default or broken icon in the Unraid template also goes on the [tracker](https://github.com/chr0nzz/traefik-manager/issues), mention Unraid in the title
- **Chat** - questions and release news on the [Discord](https://discord.gg/a6NKyJsfc)

When reporting a bug, include your Traefik Manager version, your Traefik version, and the container log from the Unraid **Docker** tab.

## Links

- [Traefik Manager source](https://github.com/chr0nzz/traefik-manager)
- [Documentation](https://traefik-manager.xyzlab.dev/)
- [Discord](https://discord.gg/a6NKyJsfc)
- [Container image](https://github.com/chr0nzz/traefik-manager/pkgs/container/traefik-manager)
- [Agent image](https://github.com/chr0nzz/traefik-manager/pkgs/container/traefik-manager-agent)

## License

GPL-3.0, see [LICENSE](LICENSE).
