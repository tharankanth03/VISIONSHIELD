# Deployment

## Render

The repository includes a `Dockerfile` and `render.yaml` for the local HTML dashboard and JSON API. The recommended deployment is:

1. Create a Render account and connect `tharankanth03/VISIONSHIELD`.
2. Create a Blueprint from `render.yaml`.
3. Confirm the `visionshield-ui` web service.
4. Wait for the build and open the generated HTTPS URL.
5. Verify `/api/health` returns `"status": "ok"`.

The service hosts the dashboard/API only. It does not have access to a user's local camera or MLX90640 sensor. Hardware inference must run on the edge device, where the camera and thermal bus are attached. If remote alerts are enabled, configure Telegram secrets through the hosting provider's secret manager, never in Git.

## Local equivalent

```bash
docker build -t visionshield-ui .
docker run --rm -p 8080:8080 visionshield-ui
```

Then open `http://127.0.0.1:8080`.

## Important limitation

This repository can prepare and verify the deployment configuration, but creating the external Render service requires an authorized Render account. No hosting credentials are stored in this repository.
