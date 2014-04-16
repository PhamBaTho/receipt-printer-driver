
Python source code of POS system, run on Raspberry Pi, receive requests from iPad app and control thermal printer via COM interface.

<h1>Install Additional Python Libraries:</h1>

<code>sudo apt-get install python-serial python-imaging python-unidecode</code>

<h1>Enable Software Access to Serial Port:</h1>

The serial port on the Raspberry Pi’s GPIO header is normally configured for console cable use. But now we want to use this port for the thermal printer instead, so we’ll need to disable this default behavior.

<code>sudo nano /boot/cmdline.txt</code>

Change:
<code>dwc_otg.lpm_enable=0 console=ttyAMA0,115200 kgdboc=ttyAMA0,115200 console=tty1 root=/dev/mmcblk0p2 rootfstype=ext4 elevator=deadline rootwait</code>
to:
<code>dwc_otg.lpm_enable=0 console=tty1 root=/dev/mmcblk0p2 rootfstype=ext4 elevator=deadline rootwait
(Basically, delete the references to ttyAMA0)</code>

And:

<code>sudo nano /etc/inittab</code>

Comment out or delete the last line. i.e. change this:
<code>T0:23:respawn:/sbin/getty -L ttyAMA0 115200 vt100</code>
to:
<code># T0:23:respawn:/sbin/getty -L ttyAMA0 115200 vt100</code>
Or simply delete that line.
