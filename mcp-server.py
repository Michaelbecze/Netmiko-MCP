import os
from dotenv import load_dotenv
from fastmcp import FastMCP
from netmiko import ConnectHandler

load_dotenv()

DEVICE_USERNAME = os.environ["MCP_DEVICE_USERNAME"]
DEVICE_PASSWORD = os.environ["MCP_DEVICE_PASSWORD"]
DEVICE_SECRET = os.environ["MCP_DEVICE_SECRET"]

DEVICES = {
    "router1": {
        "device_type": "cisco_ios",
        "host": "192.168.0.30",
        "username": DEVICE_USERNAME,
        "password": DEVICE_PASSWORD,
        "secret": DEVICE_SECRET,
    },
    "router2": {
        "device_type": "cisco_ios",
        "host": "192.168.0.31",
        "username": DEVICE_USERNAME,
        "password": DEVICE_PASSWORD,
        "secret": DEVICE_SECRET,
    },
    "router3": {
        "device_type": "cisco_ios",
        "host": "192.168.0.32",
        "username": DEVICE_USERNAME,
        "password": DEVICE_PASSWORD,
        "secret": DEVICE_SECRET,
    },
}


mcp = FastMCP("Mr-MCP")

def connect(device):
    """
    Open a connection to my device with Netmiko
    """
    if device not in DEVICES:
        raise ValueError("Unknown Device")
    return ConnectHandler(**DEVICES[device])

@mcp.tool()
def list_devices():
    """
    List all the devices in the network topology
    """
    devices = []
    for device_name, device_info in DEVICES.items():
        device_dict = {
            "name": device_name,
            "host": device_info["host"],
            "type": device_info["device_type"]
        }
        devices.append(device_dict)
    return devices

@mcp.tool()
def run_show_command(device_name, command):
    """
    Run a show command against a device in the topology using Netmiko
    """
    conn = connect(device_name)
    result = conn.send_command(command)
    conn.disconnect()
    return result


@mcp.tool()
def run_show_command(device_name: str, command: str) -> str:
    """
    Run a show command against a device in the topology using Netmiko
    """
    conn = connect(device_name)
    commands = []
    lines = config.splitlines()
    for line in lines:
        if line != "":
            commands.append(line)
    result = conn.send_config_set(commands)
    conn.save_config()
    conn.disconnect()
    return result


if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)