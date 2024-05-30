#!/bin/bash
if [ $# -lt 2 ]; then
    echo "Usage error for $0. Required arguments not provided." >&2
    echo "Usage: $0 <product_type> <communication_mode> [serial_port] [server_ip] [server_port]" >&2
    echo "Example 1 (serial): $0 LD06 serial /dev/ttyUSB0" >&2
    echo "Example 2 (network): $0 LD19 network 192.168.1.200 2000" >&2
    exit 1
fi

PRODUCT_TYPE=$1
COMM_MODE=$2
PORT_PATH=$3  # For serial
SERVER_IP_ADDR=$4 # For network
SERVER_PORT_ADDR=$5 # For network

# Start the node based on the communication mode
if [ "$COMM_MODE" == "network" ]; then
    if [ -z "$SERVER_IP_ADDR" ] || [ -z "$SERVER_PORT_ADDR" ]; then
        echo "ERROR: Server IP and port must be specified for network mode." >&2
        exit 1
    fi
    echo "Starting node in network mode..."
    ./build/ldlidar_stl_node "$PRODUCT_TYPE" networkcom_tcpclient "$SERVER_IP_ADDR" "$SERVER_PORT_ADDR"
elif [ "$COMM_MODE" == "serial" ]; then
    if [ -z "$PORT_PATH" ]; then
        echo "ERROR: Serial port must be specified for serial mode." >&2
        exit 1
    fi
    # Secure the serial port with more restrictive permissions
    sudo chmod 660 "$PORT_PATH"
    sudo chown $(whoami) "$PORT_PATH"  # Change owner to the current user
    echo "Starting node in serial mode..."
    ./build/ldlidar_stl_node "$PRODUCT_TYPE" serialcom "$PORT_PATH"
else
    echo "ERROR: Invalid communication mode specified." >&2
    exit 1
fi

echo "Node started successfully. Outputting to stdout. Ready for piping or monitoring."
