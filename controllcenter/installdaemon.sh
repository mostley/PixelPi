echo "**** Installing the WebIDE as a service ****"
echo "**** (to uninstall service, execute: 'sudo update-rc.d -f adafruit-webide.sh remove') ****"
cp "/home/pi/pixelpi/controllcenter/controllcenter.sh" "/etc/init.d"
cd /etc/init.d
chmod 755 adafruit-webide.sh
update-rc.d controllcenter.sh defaults