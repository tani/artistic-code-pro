#!/usr/bin/env bash
set -euo pipefail

rm -rf build
mkdir build

fontforge -script script/merge.py \
    --target_name="./build/ArtisticCodePro-Light.ttf" \
    --source_name="./FiraCode/distr/ttf/FiraCode-Light.ttf" \
    --cjk_name="./mgenplus/mgenplus-1mn-light.ttf" 
fontforge -script script/merge.py \
    --target_name="./build/ArtisticCodePro-Regular.ttf" \
    --source_name="./FiraCode/distr/ttf/FiraCode-Regular.ttf" \
    --cjk_name="./mgenplus/mgenplus-1mn-regular.ttf"
fontforge -script script/merge.py \
    --target_name="./build/ArtisticCodePro-Medium.ttf" \
    --source_name="./FiraCode/distr/ttf/FiraCode-Medium.ttf" \
    --cjk_name="./mgenplus/mgenplus-1mn-medium.ttf"
fontforge -script script/merge.py \
    --target_name="./build/ArtisticCodePro-SemiBold.ttf" \
    --source_name="./FiraCode/distr/ttf/FiraCode-SemiBold.ttf" \
    --cjk_name="./mgenplus/mgenplus-1mn-bold.ttf"
fontforge -script script/merge.py \
    --target_name="./build/ArtisticCodePro-Bold.ttf" \
    --source_name="./FiraCode/distr/ttf/FiraCode-Bold.ttf" \
    --cjk_name="./mgenplus/mgenplus-1mn-bold.ttf"

parallel -i \
    fontforge -script ./nerd-fonts/font-patcher \
        --adjust-line-height \
        --fontawesome \
        --fontawesomeextension \
        --fontlogos \
        --octicons \
        --powersymbols \
        --powerline \
        --powerlineextra \
        --materialdesignicons \
        --weathericons \
        --quiet \
        --outputdir build \
        build/ArtisticCodePro-{}.ttf \
    -- Light Regular Medium SemiBold Bold

parallel -i \
    mv "build/Fira Code {} Nerd Font Plus Font Awesome Plus Font Awesome Extension Plus Octicons Plus Power Symbols Plus Font Logos (Font Linux) Plus Material Design Icons Plus Weather Icons.ttf" "build/ArtisticCodePro-{}.ttf" \
    -- Light Regular Medium SemiBold Bold

parallel -i \
    python3 script/metadata.py \
        --version=0.002 \
        --weight={} \
        --font_path=build/ArtisticCodePro-{}.ttf \
    -- Light Regular Medium SemiBold Bold

otf2otc -o build/ArtisticCodePro.ttc build/ArtisticCodePro*.ttf
