# Vogon IoT Collector

Simple MQTT-based IoT measurement collector which stores data to a TimescaleDB and display them using a Grafana
dashboard.

**Work in progress**

## MQTT

| MQTT Topics                                         | Example                                             | Description                |
|-----------------------------------------------------|-----------------------------------------------------|----------------------------|
| {service}/{node-mac-address}/raw                    | vogonair/42:d1:03:6c:dd:a0/raw                      | Raw collector without sink |
| {service}/{sink-mac-address}/{node-mac-address}/raw | vogonveggie/40:4c:ca:44:0e:ec/42:d1:03:6c:dd:a0/raw | Raw collector with sink    |

## OS Configuration & Installation

In this project we use a RaspberryPi 3B as a "server" which provides MQTT broker, TimescaleDB database, Grafana and
WiFi Access Point for a sink nodes which sends data from WSN. By the way: we use ArchLinux.

**TODO: Add nice deployment diagrams**

### Initial

```shell
pacman-key --init
pacman-key --populate archlinuxarm

# Update repositories
pacman -Syy

# System upgrade
pacman -Syu
```

### Docker

```shell
pacman -S docker
systemctl enable docker.service
systemctl start docker.service

usermod -aG docker alarm
```

### Access point

```shell
pacman -S hostapd kea
```

**/etc/systemd/network/wlan0.network**

```ini
[Match]
Name=wlan0

[Network]
Address=192.168.40.1/24
DNS=8.8.8.8
```

**/etc/kea/kea-dhcp4.conf**

```json
{
	"Dhcp4": {
		"interfaces-config": {
			"interfaces": [ "eth0/192.168.0.1" ],
			"dhcp-socket-type": "raw"
		},

		"subnet4": [
			{
				"id": 1,
				"subnet": "192.168.0.0/24",
				"pools": [ { "pool": "192.168.0.30 - 192.168.0.250" } ],
				"option-data": [
					{
						"name": "routers",
						"data": "192.168.0.1"
					},
					{
						"name": "domain-name-servers",
						"data": "8.8.8.8"
					}
				]
			}
		]
	}
}
```

```shell
kea-dhcp4 -t /etc/kea/kea-dhcp4.conf
systemctl enable kea-dhcp4 --now
systemctl enable hostapd --now
```
