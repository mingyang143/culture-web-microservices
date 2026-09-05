# microservices
contains the microservices for culture web

## Face-detection image compatibility

Face detection uses NumPy 1.24.3 with OpenCV headless 4.5.2.54. The
`constraints.txt` file is applied to every pip invocation in its Docker image.
Keep `--no-deps` on the final OpenCV reinstall: an unconstrained reinstall
previously replaced NumPy with 2.0.2 and prevented `cv2` from importing.
RetinaFace declares `opencv-python` as a dependency; the image deliberately
replaces that distribution with the headless variant that provides `cv2`.
Consequently pip can report the missing `opencv-python` distribution even when
the runtime imports work. Do not install a second OpenCV distribution to silence
that warning.

The Dockerfile runs `verify_image.py` before completing the build. This checks
the NumPy version, OpenCV image encoding, application import and the Flask
missing-image response. It does not check model inference or model downloads;
test an actual image through the deployed application after rollout.

Build from this repository after committing the changes, using the existing
**Build Image CI** workflow with a new version tag (do not reuse `v2.1.0`).
Its face-detection build runs the checks before pushing the image. The workflow
also builds the other services, but they do not need to be redeployed for this fix.
Update only the face-detection image reference in the deployment Compose file,
then run from the deployment directory:

```bash
docker compose pull face-detection
docker compose up -d --no-deps face-detection
docker compose ps -a face-detection
docker compose logs --tail=100 face-detection
```

Keep the previous image reference for rollback. Local source edits do not change
already-published images or the deployed VM. The local requirements also contain
earlier TensorFlow 2.17 / tf-keras changes; the rebuilt image must be verified on
the target VM even though the NumPy-only test passed on the older image.
