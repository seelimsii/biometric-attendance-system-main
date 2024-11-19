#!/bin/sh

export build_type="local"
cd fastapi && sh scripts/docker.build.sh && cd - || exit
cd react && sh scripts/docker.build.sh && cd - || exit