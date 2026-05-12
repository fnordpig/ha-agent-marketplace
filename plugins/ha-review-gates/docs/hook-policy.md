# Hook Policy

The pre-tool hook warns on commands and tool payloads containing sensitive terms:

- delete
- remove
- `rm -rf`
- restart
- reboot
- hassio
- `ha core restart`
- `docker compose down`
- `.storage`
- `secrets.yaml`
- `known_devices.yaml`
- direct writes to `automations.yaml`

The post-turn hook emits a short reporting reminder.

