#!/bin/bash

# Check if the script is run as root.
if [ "$EUID" -ne 0 ]
then
    echo "Please run the script as root."
    exit
fi

# Prompt for the path to the Python script.
read -p "Enter path to Python script: " script_path

# Prompt to enter the name of the service.
read -p "Enter the name of the service: " service_name

# Verify that the provided script path exists.
if [ ! -f "$script_path" ]
then
    echo "The provided path doesn't exist."
    exit
fi

# Create the systemd service file content.
service_content="[Service]
ExecStart=/usr/bin/python3 $script_path
User=$SUDO_USER

[Install]
WantedBy=multi-user.target"

# Define the service file path.
service_file_path="/usr/lib/systemd/system/$service_name.service"

# Write the content to the service file.
echo "$service_content" > "$service_file_path"

# Reload systemd to recognize new service.
systemctl daemon-reload

# Enable the service.
systemctl enable $service_name.service

echo "Service '$service_name' created and enabled successfully!"
