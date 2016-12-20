# InvWatermark
Create your own invisible watermark

## Install Website

	yarn install
	npm start

## Install Python OpenCV

```
sudo apt install -y build-essential cmake git pkg-config 
sudo apt install -y libjpeg8-dev libtiff4-dev libjasper-dev libpng12-dev

# For GUI
# sudo apt install -y libgtk2.0-dev

sudo apt install -y libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt install -y libatlas-base-dev gfortran

# install pip
sudo apt install python-pip
sudo apt install python2.7-dev

# !!!!!!!
# Download opencv, opencv_contrib
# !!!!!!!

cd ~/opencv/build

cmake 
	-D CMAKE_BUILD_TYPE=RELEASE \
	-D CMAKE_INSTALL_PREFIX=/usr/local \
	-D INSTALL_C_EXAMPLES=OFF \
	-D INSTALL_PYTHON_EXAMPLES=ON \
	-D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules \
	-D BUILD_EXAMPLES=ON ..

make -j4

sudo make install
sudo ldconfig
sudo pip install matplotlib
sudo apt install -y python-tk
```