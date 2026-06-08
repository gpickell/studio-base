# ![](https://apps.vertigisstudio.com/favicon.ico) VertiGIS Studio Base

Container image for running VertiGIS Studio with Docker.

See [docs](https://gpickell.github.io/studio-base/?tag=v1.1.1002.321611-r23931814084).

## Image

```text
ghcr.io/vertigis/studio/base:v1.1.1002.321611-r23931814084
```

## GitHub Actions tag sync

This repository includes a workflow that mirrors the latest `ghcr.io/vertigis/studio/base:v*` tags to matching git tags.

- Trigger it manually with **Actions > Tag from GHCR image > Run workflow** to sync the latest five version tags.
- It also listens for `registry_package` publish/update events, resolves the latest five image tags that start with `v`, and refreshes each matching git tag.
- Each tag contains a generated `docs/index.md` snapshot without updating `master`.
- Rerunning the workflow force-updates those git tags and republishes `gh-pages` from the newest resolved tag.
- The same run publishes `index.html`, `README.md`, and `docs/index.md` to GitHub Pages with the same layout as the newest tagged content.
- If the workflow token can read the package metadata, the snapshot links each tag to its exact GitHub Packages version page; otherwise it falls back to the package page filtered by `?tag=...`.

## Registry login

```sh
gh auth login -w -s read:packages
gh auth token | docker login ghcr.io -u x-access-token --password-stdin
```

## Quick start

```sh
docker run -d --name studio-base \
  -p 8080:8080 \
  -e ARCGIS_APP_ID=app_id \
  -e ARCGIS_PORTAL_URL=https://portal.example.com/portal \
  -e VERTIGIS_ACCOUNT_ID=account_id \
  -e FRONTEND_URL=https://studio.example.com/studio \
  -v studio-data:/data \
  -v studio-logs:/var/log \
  -v studio-temp:/stmp \
  ghcr.io/vertigis/studio/base:v1.1.1002.321611-r23931814084
```

## Compose example

```yaml
services:
  studio-base:
    image: ghcr.io/vertigis/studio/base:v1.1.1002.321611-r23931814084
    restart: unless-stopped
    ports:
      # Expose Studio Base on the host.
      - "8080:8080"
    environment:
      # ArcGIS OAuth application ID from your ArcGIS Portal app registration.
      ARCGIS_APP_ID: app_id
      # Base URL of your ArcGIS Portal.
      ARCGIS_PORTAL_URL: https://portal.example.com/portal
      # VertiGIS account ID provided by VertiGIS support.
      VERTIGIS_ACCOUNT_ID: account_id
      # Public URL users will browse to.
      FRONTEND_URL: https://studio.example.com/studio
      # Optional runtime settings.
      VERTIGIS_PURGE: "1"
      VERTIGIS_WORKERS: "8"
    volumes:
      # Persist application data, logs, and temp files.
      - studio-data:/data
      - studio-logs:/var/log
      - studio-temp:/stmp

volumes:
  studio-data:
  studio-logs:
  studio-temp:
```

## Required environment variables

| Variable | Description |
| --- | --- |
| `ARCGIS_APP_ID` | ArcGIS application ID from your ArcGIS Portal app registration |
| `ARCGIS_PORTAL_URL` | ArcGIS Portal URL |
| `VERTIGIS_ACCOUNT_ID` | VertiGIS account ID provided by VertiGIS support |
| `FRONTEND_URL` | Public Studio Base URL |

## Finding the IDs

- `ARCGIS_APP_ID`: create or open the app registration in ArcGIS Portal and copy the application ID.
- `VERTIGIS_ACCOUNT_ID`: request this value from VertiGIS support.

## Data

Persist these paths if you want data and logs to survive container replacement:

- `/data`
- `/var/log`
- `/stmp`
