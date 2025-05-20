#!/bin/bash
ENTRYPOINT="python3 /app/app.py"
IMG_NAME=tee-dcgan-generator
IMG_FROM=raorla/dcgan-generator:1.0.0
IMG_TO=raorla/${IMG_NAME}:1.0.0-debug

docker run -it \
    -v /var/run/docker.sock:/var/run/docker.sock \
    registry.scontain.com/scone-production/iexec-sconify-image:5.9.1-v15 \
    sconify_iexec \
    --name=${IMG_NAME} \
    --from=${IMG_FROM} \
    --to=${IMG_TO} \
    --base=ubuntu:20.04 \
    --binary-fs \
    --fs-dir=/app \
    --fs-dir=/opt/venv \
    --host-path=/tmp \
    --host-path=/etc/hosts \
    --host-path=/etc/resolv.conf \
    --binary=/opt/venv/bin/python3 \
    --heap=1G \
    --dlopen=1 \
    --no-color \
    --verbose \
    --env HOME=/app \
    --env PATH=/opt/venv/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin \
    --command="${ENTRYPOINT}" \
    && echo -e "\n------------------\n" \
    && echo "successfully built TEE docker image => ${IMG_TO}" \
    && echo "application mrenclave.fingerprint is $(docker run --rm -e SCONE_HASH=1 ${IMG_TO})"