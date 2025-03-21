#!/usr/bin/env bash

wget --no-check-certificate 'https://www.dropbox.com/scl/fi/pml7zmyrgp2ellbyrm26o/emulators.tar.gz?rlkey=8gg4p20z3h87p2q7kxhk0x91f&st=nqjig9s5&dl=0' -O emulators.tar.gz
tar -xvf emulators.tar.gz
rm emulators.tar.gz
