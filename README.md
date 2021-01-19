# Smart Gate Security System
Final Project for Embedded System Course Fasilkom UI 2020/2021

Smart Gate Security System (SGSS) adalah suatu sistem tertanam IoT dan AI berbasis arduino - raspberry pi yang berguna untuk mendeteksi jarak suatu objek ke gate (pintu), pergerakan objek, human detection camera untuk unusual activity, status pintu terbuka atau tidak, dan alarm jika terdapat unauthenticated objek atau seseorang masuk. Untuk authentication menggunakan RFID yang teregister pada arduino. Informasi-informasi tersebut dapat dimonitor melalui web server Thinsboard yang dapat diakses internet.

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

## Arduino Setup:
1. Install library lcd and rfid in arduinoLibrary folder and FreeRTOS
2. Make sure all pin right base on top of comment program in sgss.ino / sgssRTOS.ino
3. Change RFID id and name in sgss.ino / sgssRTOS.ino into your RFID id and name
4. Write sgss.ino / sgssRTOS.ino into your arduino mega and run it

## Raspberry Pi Setup:
1. Change arduino port and username id in main.py
2. Change in main.py directory path to your absolute path of objectDetectionData folder
3. Run main.py in following command
```
python3 main.y
```
