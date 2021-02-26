#!/bin/bash

download_link=https://github.com/ArjunSahlot/knight_visualizer/archive/main.zip
temporary_dir=$(mktemp -d) \
&& curl -LO $download_link \
&& unzip -d $temporary_dir main.zip \
&& rm -rf main.zip \
&& mv $temporary_dir/knight_visualizer-main $1/knight_visualizer \
&& rm -rf $temporary_dir
echo -e "[0;32mSuccessfully downloaded to $1/knight_visualizer[0m"
