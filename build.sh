#!/bin/bash
app="crypto-oracle"
docker build -t ${app}:$(git describe --always --tags --dirty --abbrev=7) .
