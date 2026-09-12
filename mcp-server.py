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


def connect(device: str) -> ConnectHandler:
    """
    Open a connection to a device with Netmiko
    """
    if device not in DEVICES:
        raise ValueError(f"Unknown device: {device}")
    return ConnectHandler(**DEVICES[device])


@mcp.tool()
def list_devices() -> list[dict]:
    """
    List all the devices in the network topology
    """
    return [
        {"name": name, "host": info["host"], "type": info["device_type"]}
        for name, info in DEVICES.items()
    ]


@mcp.tool()
def run_show_command(device_name: str, command: str) -> str:
    """
    Run a show command against a device in the topology using Netmiko
    """
    conn = connect(device_name)
    try:
        return conn.send_command(command)
    finally:
        conn.disconnect()


@mcp.tool()
def run_config_commands(device_name: str, config: str) -> str:
    """
    Push configuration lines to a device in the topology using Netmiko.
    `config` is a newline-separated block of IOS configuration commands.
    """
    conn = connect(device_name)
    try:
        commands = [line for line in config.splitlines() if line.strip()]
        conn.enable()
        result = conn.send_config_set(commands)
        conn.save_config()
        return result
    finally:
        conn.disconnect()


if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)