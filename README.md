# Traffic Data Collection Sensors

Code to run the sensors and publish/subscribe to AWS IoT message broker in [traffic data analysis project](https://github.com/wuihee/Traffic-Data-Collection/tree/main).

## Table of Contents

1. Installation
2. Usage
3. Repository Structure
4. Testing
5. AWS IoT Configuration

## Installation

### Prerequisites

### Dependencies

```bash
pip install -r requirements.txt
```

### Raspberry Pi Autostart on Boot with Systemd

Create a service in `/usr/lib/systemd/system`. E.g. `sensor.service`.

- Include the path to your script in ExecStart.
- Replace `YOUR_USER` with the output of command `whoami`.

```text
[Service]
ExecStart=/usr/bin/python3 /PATH_TO_YOUR_SCRIPT.py
User=YOUR_USER

[Install]
WantedBy=multi-user.target
```

Afterwards reload systemd.

```bash
sudo systemctl daemon-reload
```

Enable your service. Afterwards, your script should autostart on boot.

```bash
sudo systemctl enable SERVICE_NAME.service
```

To disable your service:

```bash
sudo systemctl disable SERVICE_NAME.service
```

To check the status of your service for degbugging:

```bash
sudo systemctl status SERVICE_NAME.service
```

### AWS IoT Setup

## Usage

### Sensors

### AWS IoT Message Broker

## Repository Structure

## Testing
