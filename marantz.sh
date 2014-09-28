#!/usr/bin/env bash

declare -A inputMapping

inputMapping=( ["saga"]="MPLAY" ["xbox"]="GAME" )

function doPost {
    curl --data-urlencode "$1" http://marantz/MainZone/index.put.asp
}

function sendCommand {
    cmd="${1}"
    arg="${2}"
    doPost "cmd0=${cmd}/${arg}"
}

function increaseVolume {
    sendCommand "PutMasterVolumeBtn" ">"
}

function decreaseVolume {
    sendCommand "PutMasterVolumeBtn" "<"
}

function powerOn {
    sendCommand "PutZone_OnOff" "ON"
}

function powerOff {
    sendCommand "PutZone_OnOff" "OFF"
}

function setVolume {
    vol=$(printf %.1f "$1")
    sendCommand "PutMasterVolumeSet" "$vol"
}

function setInput {
    input=${inputMapping["$1"]}
    if [ -z "$input" ]; then
        echo "No such input: $1"
        return
    fi
    sendCommand "PutZone_InputFunction" "MPLAY"
}

function mute {
    sendCommand "PutVolumeMute" "$1"
}

while [ -n "$1" ] ; do
    arg="$1"
    shift
    case $arg in
        inc) increaseVolume ;;
        dec) decreaseVolume ;;
        on) powerOn ;;
        off) powerOff ;;
        vol) setVolume "$1"; shift ;;
        input) setInput "$1"; shift ;;
        mute) mute "$1"; shift ;;
        *) echo "Unknown option $arg" ;;
    esac
done
