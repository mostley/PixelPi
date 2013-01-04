echo "**** Installing the Controll Center as a service ****"
echo "**** (to uninstall service, execute: 'sudo update-rc.d -f controllcenter.sh remove') ****"
cp "/home/pi/pixelpi/controllcenter/controllcenter.sh" "/etc/init.d"
cd /etc/init.d
chmod 755 adafruit-webide.sh
update-rc.d controllcenter.sh defaults