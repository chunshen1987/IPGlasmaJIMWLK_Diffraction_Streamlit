#!/usr/bin/env bash

#curl -L -o emulators.tar.gz "https://www.dropbox.com/scl/fi/pml7zmyrgp2ellbyrm26o/emulators.tar.gz?rlkey=8gg4p20z3h87p2q7kxhk0x91f&st=nqjig9s5&dl=0"
#curl -L -o emulators.tar.gz "https://www.dropbox.com/scl/fi/o9je6zi63amck1kvsodyy/emulators.tar.gz?rlkey=sef2nrs9be2alvu2drcenkmt0&dl=0"

curl --output temp.tar.gz "https://zenodo.org/api/records/15880667/files/trained_emulators.tar.gz/content"

tar -xf temp.tar.gz
rm temp.tar.gz
mv trained_emulators emulators
