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


<source name="Ref_median_L" properties_file="/Users/orberebi/Documents/GitHub/TUB-BGU-colab/MUSHRA_2025/SSR_scene/BRIR/tub_25/Ref_L.wav" volume="0" mute="true" id="ID_1.1">
      <file>/Users/orberebi/Documents/GitHub/TUB-BGU-colab/MUSHRA_2025/SSR_scene/dry_sigs/tub25_v2/Ref_median_L.wav</file>
      <position x="-2.00" y="1.00" fixed="true"/>
</source>

<source name="Ref_median_R" properties_file="/Users/orberebi/Documents/GitHub/TUB-BGU-colab/MUSHRA_2025/SSR_scene/BRIR/tub_25/Ref_R.wav" volume="0" mute="true" id="ID_1.2">
      <file>/Users/orberebi/Documents/GitHub/TUB-BGU-colab/MUSHRA_2025/SSR_scene/dry_sigs/tub25_v2/Ref_median_R.wav</file>
      <position x="-2.00" y="2.00" fixed="true"/>
</source>


<source name="MagLS_median_L" properties_file="/Users/orberebi/Documents/GitHub/TUB-BGU-colab/MUSHRA_2025/SSR_scene/BRIR/tub_25/MagLS_L.wav" volume="0" mute="true" id="ID_2.1">
      <file>/Users/orberebi/Documents/GitHub/TUB-BGU-colab/MUSHRA_2025/SSR_scene/dry_sigs/tub25_v2/MagLS_median_L.wav</file>
      <position x="-1.00" y="1.00" fixed="true"/>
</source>

<source name="MagLS_median_R" properties_file="/Users/orberebi/Documents/GitHub/TUB-BGU-colab/MUSHRA_2025/SSR_scene/BRIR/tub_25/MagLS_R.wav" volume="0" mute="true" id="ID_2.2">
      <file>/Users/orberebi/Documents/GitHub/TUB-BGU-colab/MUSHRA_2025/SSR_scene/dry_sigs/tub25_v2/MagLS_median_R.wav</file>
      <position x="-1.00" y="2.00" fixed="true"/>
</source>


<source name="Phiona_median_L" properties_file="/Users/orberebi/Documents/GitHub/TUB-BGU-colab/MUSHRA_2025/SSR_scene/BRIR/tub_25/Phiona_L.wav" volume="0" mute="true" id="ID_3.1">
      <file>/Users/orberebi/Documents/GitHub/TUB-BGU-colab/MUSHRA_2025/SSR_scene/dry_sigs/tub25_v2/Phiona_median_L.wav</file>
      <position x="0.00" y="1.00" fixed="true"/>
</source>

<source name="Phiona_median_R" properties_file="/Users/orberebi/Documents/GitHub/TUB-BGU-colab/MUSHRA_2025/SSR_scene/BRIR/tub_25/Phiona_R.wav" volume="0" mute="true" id="ID_3.2">
      <file>/Users/orberebi/Documents/GitHub/TUB-BGU-colab/MUSHRA_2025/SSR_scene/dry_sigs/tub25_v2/Phiona_median_R.wav</file>
      <position x="0.00" y="2.00" fixed="true"/>
</source>

<source name="Ref_horizontal_L" properties_file="/Users/orberebi/Documents/GitHub/TUB-BGU-colab/MUSHRA_2025/SSR_scene/BRIR/tub_25/Ref_L.wav" volume="0" mute="true" id="ID_4.1">
      <file>/Users/orberebi/Documents/GitHub/TUB-BGU-colab/MUSHRA_2025/SSR_scene/dry_sigs/tub25_v2/Ref_horizontal_L.wav</file>
      <position x="1.00" y="1.00" fixed="true"/>
</source>

<source name="Ref_horizontal_R" properties_file="/Users/orberebi/Documents/GitHub/TUB-BGU-colab/MUSHRA_2025/SSR_scene/BRIR/tub_25/Ref_R.wav" volume="0" mute="true" id="ID_4.2">
      <file>/Users/orberebi/Documents/GitHub/TUB-BGU-colab/MUSHRA_2025/SSR_scene/dry_sigs/tub25_v2/Ref_horizontal_R.wav</file>
      <position x="1.00" y="2.00" fixed="true"/>
</source>


<source name="MagLS_horizontal_L" properties_file="/Users/orberebi/Documents/GitHub/TUB-BGU-colab/MUSHRA_2025/SSR_scene/BRIR/tub_25/MagLS_L.wav" volume="0" mute="true" id="ID_5.1">
      <file>/Users/orberebi/Documents/GitHub/TUB-BGU-colab/MUSHRA_2025/SSR_scene/dry_sigs/tub25_v2/MagLS_horizontal_L.wav</file>
      <position x="2.00" y="1.00" fixed="true"/>
</source>

<source name="MagLS_horizontal_R" properties_file="/Users/orberebi/Documents/GitHub/TUB-BGU-colab/MUSHRA_2025/SSR_scene/BRIR/tub_25/MagLS_R.wav" volume="0" mute="true" id="ID_5.2">
      <file>/Users/orberebi/Documents/GitHub/TUB-BGU-colab/MUSHRA_2025/SSR_scene/dry_sigs/tub25_v2/MagLS_horizontal_R.wav</file>
      <position x="2.00" y="2.00" fixed="true"/>
</source>


<source name="Phiona_horizontal_L" properties_file="/Users/orberebi/Documents/GitHub/TUB-BGU-colab/MUSHRA_2025/SSR_scene/BRIR/tub_25/Phiona_L.wav" volume="0" mute="true" id="ID_6.1">
      <file>/Users/orberebi/Documents/GitHub/TUB-BGU-colab/MUSHRA_2025/SSR_scene/dry_sigs/tub25_v2/Phiona_horizontal_L.wav</file>
      <position x="3.00" y="1.00" fixed="true"/>
</source>

<source name="Phiona_horizontal_R" properties_file="/Users/orberebi/Documents/GitHub/TUB-BGU-colab/MUSHRA_2025/SSR_scene/BRIR/tub_25/Phiona_R.wav" volume="0" mute="true" id="ID_6.2">
      <file>/Users/orberebi/Documents/GitHub/TUB-BGU-colab/MUSHRA_2025/SSR_scene/dry_sigs/tub25_v2/Phiona_horizontal_R.wav</file>
      <position x="3.00" y="2.00" fixed="true"/>
</source>


</scene_setup>
</asdf>
