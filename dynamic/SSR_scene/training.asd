<?xml version="1.0" encoding="utf-8"?>
<asdf
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
 xsi:noNamespaceSchemaLocation="asdf.xsd"
 version="0.1">


<header>
 <name>Example for BRS rendering</name>
<description>
 This example is best replayed with the BRS renderer.
 </description>
</header>


<scene_setup>
<volume>-5 </volume>


<source name="Ref_N30_60" properties_file="/Users/aclab-recroom/Documents/GitHub/MUSHRA_2025/SSR_scene/BRIR/training/BRIR Ref_N30_60.wav" volume="-1.411621e+00" mute="true" id="ID_1">
      <file>/Users/aclab-recroom/Documents/GitHub/MUSHRA_2025/SSR_scene/dry_sigs/casta.wav</file>
      <position x="-2.00" y="1.00" fixed="true"/>
</source>


<source name="Ref_N30_30" properties_file="/Users/aclab-recroom/Documents/GitHub/MUSHRA_2025/SSR_scene/BRIR/training/BRIR Ref_N30_30.wav" volume="0" mute="true" id="ID_2">
      <file>/Users/aclab-recroom/Documents/GitHub/MUSHRA_2025/SSR_scene/dry_sigs/casta.wav</file>
      <position x="-1.00" y="1.00" fixed="true"/>
</source>


<source name="Ref_N3_60" properties_file="/Users/aclab-recroom/Documents/GitHub/MUSHRA_2025/SSR_scene/BRIR/training/BRIR Ref_N3_60.wav" volume="-3.609121e+00" mute="true" id="ID_3">
      <file>/Users/aclab-recroom/Documents/GitHub/MUSHRA_2025/SSR_scene/dry_sigs/casta.wav</file>
      <position x="0.00" y="1.00" fixed="true"/>
</source>


</scene_setup>
</asdf>
