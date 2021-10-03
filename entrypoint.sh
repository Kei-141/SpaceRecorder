# Cleanup to be "stateless" on startup, otherwise pulseaudio daemon can't start
rm -rf /var/run/pulse /var/lib/pulse /root/.config/pulse

# Start pulseaudio as system wide daemon; for debugging it helps to start in non-daemon mode
pulseaudio -D --verbose --exit-idle-time=-1 --system --disallow-exit

# Create a virtual audio source; fixed by adding source master and format
echo "Creating virtual audio source: ";
pactl load-module module-virtual-sink sink_name=v1
pactl set-default-sink v1

# Set VirtualMic as default input source;
echo "Setting default source: ";
pactl set-default-source v1.monitor

#bash
python3 /opt/bin/SpaceRecorder.py