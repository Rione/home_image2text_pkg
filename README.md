# home_image2text_pkg

+ required package
```
sudo apt install ros-noetic-usb-cam
```

+ setup
```
cd ~/catkin_ws/src/ && git clone https://github.com/Rione/home_image2text_pkg.git
pip install git+https://github.com/rionehome/image2text
cd ~/catkin_ws/ && catkin_make
source devel/setup.bash
```

```
roslaunch home_image2text_pkg image2text.launch 
```

出力されるテキストは
```
/i2t_text
```
のメッセージから取得できます。