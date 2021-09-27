# SignalWarn
SignalWarn is an application dedicated to monitoring radio signals, it uses an SDR to receive the signal at a set frequency and calculate the power, if a signal is detected it can also demodulate it to get the audio loudness

It can be used for example to detect if a wireless microphone gets muted accidentally or even looses power

## FAQ
> With what sdr is SignalWarn compatible

Right now, it only support the RTL-SDR with the use of the pyrtlsdr library, howeever it shouldn't be complicated to switch to SoapySDR to expand the deivce list
> What type of demodulation is supported

Right now, only mono FM demodulation is supported but AM shouldn't be too hard to implement

## Screenshots


### Dashboard
![python_2021-09-27_22-27-32](https://user-images.githubusercontent.com/17061996/134980957-34deda6e-83ae-48a8-aaf6-f627e239b503.png)
### Dashboard with muted signal
![python_2021-09-27_22-28-34](https://user-images.githubusercontent.com/17061996/134980965-606e0b35-7a2e-427f-817a-c3b6909ffa5e.png)
### Add signal manually
![python_2021-09-27_22-27-42](https://user-images.githubusercontent.com/17061996/134980977-e1442faf-61f1-4f27-bb95-b0db032d0f1f.png)
### Add signal with a preset
![python_2021-09-27_22-27-56](https://user-images.githubusercontent.com/17061996/134980980-55314784-5602-4dd5-a44d-3cb5ef07272d.png)
### Config
![python_2021-09-27_22-28-04](https://user-images.githubusercontent.com/17061996/134981003-29e4c5df-1878-4bf1-845a-78c310848e74.png)


# License
SignalWarn is under the GPLv3 license (See LICENSE.md)
