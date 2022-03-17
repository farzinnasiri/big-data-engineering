#!/bin/bash

cat /proc/cpuinfo | grep "core id" | sort | uniq | wc -l
