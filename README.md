# Smart Gate Security System
Final Project for Embedded System Course Fasilkom UI 2020/2021

Smart Gate Security System (SGSS) adalah suatu sistem tertanam IoT berbasis arduino - raspberry pi yang berguna untuk mendeteksi jarak suatu objek ke gate (pintu), pergerakan objek, status pintu terbuka atau tidak, dan alarm jika terdapat objek atau seseorang masuk. Informasi-informasi tersebut dapat dimonitor dan dikontrol melalui web server yang dapat diakses oleh semua device yang berada pada jaringan tersebut.

## Installation:
Install Dependency and Paho MQTT:
```
bash install.sh
```
Install OpenCV :
```
cd ~
wget -O opencv.zip https://github.com/opencv/opencv/archive/4.1.0.zip
wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/4.1.0.zip
unzip opencv.zip
unzip opencv_contrib.zip
cd ~/opencv-4.1.0/
mkdir build
cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE \
  -D CMAKE_INSTALL_PREFIX=/usr/local \
  -D INSTALL_PYTHON_EXAMPLES=ON \
  -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib-4.1.0/modules \
  -D BUILD_EXAMPLES=ON ..
make -j4
sudo make install && sudo ldconfig
sudo reboot
```
## Running Program:
1. Write sgss.ino into your Arduino Mega and make sure all pin right base on top of comment program in sgss.ino
2. Change arduino port and username id in main.py
3. Run main.py in following command
```
python3 main.y
```
