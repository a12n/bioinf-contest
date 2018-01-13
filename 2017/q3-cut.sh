#!/bin/sh

n=$1
k=$2

start=$((k * (n + 1) + 1))

exec sed "${start},+${n}p;d"
