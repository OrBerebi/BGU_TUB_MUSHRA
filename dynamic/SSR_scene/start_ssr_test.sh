#!/bin/sh

#xhost + 
sudo docker run \
  -e DISPLAY=$DISPLAY \
  -e QT_X11_NO_MITSHM=1 \
  -e XAUTHORITY=/tmp/.XAuthority \
  -e XAUTHORITY=/tmp/.XAuthority \
  --group-add $(ggetent group audio | cut -d: -f3) \
  --user=0 \
  --ipc=host \
  --net=host \
  -ti \
  -it \
  --rm \
  --privileged \
  christianscheer/ssr-0.3.4:latest \
  ssr --bpb --tracker=polhemus --master-volume-correction=-6 --fudi-server=1174 /Users/orberebi/Documents/SSR_mushra_2025/ListeningExperimentPy-THK_TUB_Chalmers_experiment/SSR_scene/test.asd --loop --ip-server=4711 \
  ssr-brs --fudi-server=1174 /Users/orberebi/Documents/SSR_mushra_2025/ListeningExperimentPy-THK_TUB_Chalmers_experiment/SSR_scene/test.asd --loop --ip-server=4711
