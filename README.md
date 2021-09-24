# SignalWarn
SignalWarn is an application dedicated to monitoring radio signals, it uses an SDR to receive the signal at a set frequency and calculate the power, if a signal is detected it can also demodulate it to get the audio loudness

It can be used for example to detect if a wireless microphone gets muted accidentally or even looses power

## FAQ
> With what sdr is SignalWarn compatible

Right now, it only support the RTL-SDR with the use of the pyrtlsdr library, howeever it shouldn't be complicated to switch to SoapySDR to expand the deivce list
> What type of demodulation is supported

Right now, only mono FM demodulation is supported but AM shouldn't be too hard to implement

# License
SignalWarn is under the GPLv3 license (See LICENSE.md)
