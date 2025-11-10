#!/bin/sh
open -a XQuartz
xhost +
sudo docker run \
  -e DISPLAY=$DISPLAY \
  -e QT_X11_NO_MITSHM=1 \
  -e XAUTHORITY=/tmp/.XAuthority \
  -e XAUTHORITY=/tmp/.XAuthority \
  --device /dev/snd \
  --device /dev/shm \
  --device /dev/ttyUSB0 \
  --volume $XAUTHORITY:/tmp/.XAuthority \
  --volume /tmp/.X11-unix:/tmp/.X11-unix \
  --volume $XAUTHORITY:/tmp/.XAuthority \
  --volume=/dev/snd:/dev/snd:rw \
  --volume=/dev/shm:/dev/shm:rw \
  --volume=/home/chef/:/home/chef:rw \
  --volume=/dev/ttyUSB0:/dev/ttyUSB0:rw \
  --group-add $(ggetent group audio | cut -d: -f3) \
  --user=0 \
  --ipc=host \
  --net=host \
  -ti \
  -it \
  --rm \
  --privileged \
  christianscheer/ssr-0.3.4:latest \
  ssr --bpb --tracker=polhemus --master-volume-correction=-6 --tracker-port=/dev/ttyUSB0 /home/chef/Documents/cscheer/Code/Python/ListeningExperimentPy/SSR_scene/bpb.asd
