# Install the AIY Projects software

This page describes how to install all software for an AIY Vision Bonnet or Voice Bonnet.

If you're updating an existing AIY kit or starting from scratch, we recommend you [install our
pre-built image](#install-our-pre-build-aiy-projects-image). But if you have your own Raspbian
system that you'd like to use with an AIY kit, then you can
[install our software on your existing Raspbian system](#install-aiy-software-on-an-existing-raspbian-system).

## Install our pre-build AIY Projects image

To flash our latest pre-built system image onto an SD card, follow these steps:

1. Download the latest `.img.xz` file from our [releases page on GitHub][github-releases].
   (For release details, see the [Change log][changelog].)
1. Plug-in your MicroSD card to your computer with an adapter.
1. Use a program such as [balenaEtcher](https://www.balena.io/etcher/) to flash the `.img.xy` file
   onto your MicroSD card. (balenaEtcher is free and works on Windows, Mac, and Linux.)

When flashing is done, put the MicroSD card back in your kit and you're good to go!


## Install AIY software on an existing Raspbian system

Follow these steps to install the AIY drivers and software onto an existing Raspbian system.

**Note:** This process is compatible with Raspbian Buster (2019-06-20) or later only.
Before you start, be sure you have the latest version of [Raspbian][raspbian].

### 1. Add the AIY Debian packages repo

Add AIY package repo:

```bash
echo "deb https://packages.cloud.google.com/apt aiyprojects-stable main" | sudo tee /etc/apt/sources.list.d/aiyprojects.list
```

Add Google package keys:

```bash
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
```

Update and install the latest system updates (including kernel):

```bash
sudo apt-get update
sudo apt-get upgrade
```

Reboot after update:

```bash
sudo reboot
```

### 2. Install optional packages

#### RGB Button Driver

This package is needed only if you're using the light-up RGB button that's included with
the Vision/Voice Bonnet:

```bash
sudo apt-get install -y leds-ktd202x-dkms
```

Run `sudo modprobe leds_ktd202x` to load the driver and `sudo modprobe -r leds_ktd202x` to
unload it. Vision/Voice Bonnet does this automatically via built-in device tree overlay
saved in the board's EEPROM.

#### Piezo Buzzer Driver

This package is needed only if you're using the piezo buzzer included with the Vision Bonnet:

```bash
sudo apt-get install -y pwm-soft-dkms
```

#### Pi Zero Ethernet-over-USB

This package is needed only if you're using Ethernet-over-USB on Pi Zero:
```bash
sudo apt-get install -y aiy-usb-gadget
```
Default Pi IP address is `192.168.11.2`, host IP address will be assigned automatically.

#### Support for AIY Projects app

In order to make the Pi work with the [AIY Projects][aiy-app] app:

```bash
sudo apt-get install -y aiy-bt-prov-server
```

### 3. Install required packages

Use the following commands to install packages for either the
[Vision Bonnet](#install-vision-bonnet-packages) or the
[Voice Bonnet/HAT](#install-voice-bonnethat-packages).

#### Install Vision Bonnet packages

Install the bonnet drivers:

```bash
sudo apt-get install -y aiy-vision-dkms
```

Install the [example vision models][aiy-models]:

```bash
sudo apt-get install -y aiy-models
```

Enable camera module:
```bash
echo "start_x=1" | sudo tee -a /boot/config.txt
```

Set GPU memory to 128MB:
```bash
echo "gpu_mem=128" | sudo tee -a /boot/config.txt
```

Make sure to *not* use GPIO6 for SPI0 (required since 5.4 kernel):
```bash
echo "dtoverlay=spi0-1cs,cs0_pin=7" | sudo tee -a /boot/config.txt
```

Reboot:

```bash
sudo reboot
```

Then verify that `dmesg` output contains `Myriad ready` message:

```bash
dmesg | grep -i "Myriad ready"
```

You can also verify that camera is working fine by watching video on the
connected monitor:
```bash
raspivid -t 0
```

Or use `ffplay` to get video output on the host machine:
```bash
ssh pi@raspberrypi.local "raspivid --nopreview --timeout 0 -o -" | ffplay -loglevel panic -
```

#### Install Voice Bonnet/HAT packages

Voice HAT does not require any driver installation. You only need to load
device tree overlay on boot:
```bash
echo "dtoverlay=googlevoicehat-soundcard" | sudo tee -a /boot/config.txt
```

Voice Bonnet requires driver installation:
```bash
sudo apt-get install -y aiy-voicebonnet-soundcard-dkms
```

Disable built-in audio:

```bash
sudo sed -i -e "s/^dtparam=audio=on/#\0/" /boot/config.txt
```

Install PulseAudio:

```bash
sudo apt-get install -y pulseaudio
sudo mkdir -p /etc/pulse/daemon.conf.d/
echo "default-sample-rate = 48000" | sudo tee /etc/pulse/daemon.conf.d/aiy.conf
```

You may also need to disable `module-suspend-on-idle` PulseAudio module for the
Voice HAT:
```bash
sudo sed -i -e "s/^load-module module-suspend-on-idle/#load-module module-suspend-on-idle/" /etc/pulse/default.pa
```

Reboot:

```bash
sudo reboot
```

Then verify that you can record audio:

```bash
arecord -f cd test.wav
```

...and play a sound:

```bash
aplay test.wav
```

Additionally, the Voice Bonnet/HAT requires access to Google Cloud APIs.
To complete this setup, follow the [Voice Kit setup instructions][aiy-voice-setup].


### 4. Install the AIY Projects Python library

Finally, you need to install the [AIY Projects Python library](
https://aiyprojects.readthedocs.io/en/latest/index.html).

First make sure you have `git` installed:

```bash
sudo apt-get install -y git
```

Then clone this `aiyprojects-raspbian` repo from GitHub:

```bash
git clone https://github.com/google/aiyprojects-raspbian.git AIY-projects-python
```

And now install the Python library in editable mode:

```bash
sudo pip3 install -e AIY-projects-python
```

## Appendix: List of all AIY Debian packages

The following is just a reference of all packages that are installed when you
follow the above steps.

### Vision and Voice Bonnets

* `aiy-dkms` contains MCU drivers:

  * `aiy-io-i2c` &mdash; firmware update support
  * `pwm-aiy-io` &mdash; [PWM][kernel-pwm] sysfs interface
  * `gpio-aiy-io` &mdash; [GPIO][kernel-gpio] sysfs interface
  * `aiy-adc`  &mdash; [Industrial I/O][kernel-iio] ADC interface

* `aiy-io-mcu-firmware` contains MCU firmware update service
* `leds-ktd202x-dkms` contains `leds-ktd202x` LED driver
* `pwm-soft-dkms` contains `pwm-soft` software PWM driver

### Vision Bonnet

* `aiy-vision-dkms` contains `aiy-vision` Myriad driver
* `aiy-vision-firmware` contains Myriad firmware
* `aiy-models` contains [models][aiy-models] for on-device inference:

  * Face Detection
  * Object Detection
  * Image Classification
  * Dish Detection
  * Dish Classification
  * iNaturalist Classification (plants, insects, birds)

### Voice Bonnet

* `aiy-voicebonnet-soundcard-dkms` contains sound drivers:

  * `rl6231`
  * `rt5645`
  * `snd_aiy_voicebonnet`

## Appendix: Hacking AIY Voice Kit v1 (Voice Hat) for autodetection

By default, Voice Hat needs dtoverlay added in the /boot/config.txt file. This is because the dtb is not flashed in the eeprom of Voice Hat by Google. If autodetection is desired, perform the following steps to flash patched eeprom image to your hat.

### 1. Clone and compile the Raspberry PI EEPROM utils

```bash
git clone https://github.com/raspberrypi/hats
cd hats/eepromutils
make
```

### 2. Download the patched eeprom

```bash
wget https://raw.githubusercontent.com/viraniac/aiyprojects-raspbian/aiyprojects/eeprom/voicekit_v1.eep
```

### 3. Backup existing eeprom file

```bash
sudo dtoverlay i2c-gpio i2c_gpio_sda=0 i2c_gpio_scl=1 bus=9
sudo ./eepflash.sh -r -t=24c32 -f=stock.eep
```

### 4. Disable the write protection for the I2C eeprom chip on Voice Hat

This can be done either by bridging the jumper at JP5 located on top of the hat or by grounding the TP5 testpad located below the hat.

### 5. Flash the patched eeprom file to the Voice Hat

While keeping the write protection disabled, run the following command to flash the patched eep file

```bash
sudo ./eepflash.sh -w -t=24c32 -f=voicekit_v1.eep
```

The Voice Hat will now get autodetected after reboot and will have its drivers automatically loaded as they are built into the official Raspbian kernel. Source code for the Voice Hat drivers can be found [here][voice-hat-source].

[changelog]: CHANGES.md
[raspbian]: https://www.raspberrypi.org/downloads/raspbian/
[image-flash]: https://www.raspberrypi.org/documentation/installation/installing-images/
[aiy-models]: https://aiyprojects.withgoogle.com/models/
[github-releases]: https://github.com/google/aiyprojects-raspbian/releases
[kernel-pwm]: https://www.kernel.org/doc/Documentation/pwm.txt
[kernel-gpio]: https://www.kernel.org/doc/Documentation/gpio/sysfs.txt
[kernel-iio]: https://www.kernel.org/doc/Documentation/driver-api/iio/core.rst
[aiy-app]: https://play.google.com/store/apps/details?id=com.google.android.apps.aiy
[voice-hat-source]: https://github.com/raspberrypi/linux/blob/rpi-6.1.y/sound/soc/bcm/rpi-simple-soundcard.c
