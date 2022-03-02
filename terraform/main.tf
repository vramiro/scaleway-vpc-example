terraform {
  required_providers {
    scaleway = {
      source = "scaleway/scaleway"
    }
  }
  required_version = ">= 0.13"
}

provider "scaleway" {
  alias   = "profile_provider"
  profile = "YOUR PROFILE HERE"
}

############################################################################################
# Private Network creation
resource "scaleway_vpc_private_network" "pn01" {
  provider = scaleway.profile_provider
  name     = "demo_private_network"
}
## DHCP
resource "scaleway_vpc_public_gateway_dhcp" "main" {
  provider           = scaleway.profile_provider
  subnet             = "192.168.1.0/24"
  push_default_route = true
}

# Public gateway creation
## Public IP
resource "scaleway_vpc_public_gateway_ip" "gw01" {
  provider = scaleway.profile_provider
}
resource "scaleway_vpc_public_gateway" "main" {
  provider = scaleway.profile_provider
  name     = "Public Gateway"
  type     = "VPC-GW-S"
  ip_id    = scaleway_vpc_public_gateway_ip.gw01.id
}

# Public gateway 
resource "scaleway_vpc_gateway_network" "main" {
  provider           = scaleway.profile_provider
  gateway_id         = scaleway_vpc_public_gateway.main.id
  private_network_id = scaleway_vpc_private_network.pn01.id
  dhcp_id            = scaleway_vpc_public_gateway_dhcp.main.id
  cleanup_dhcp       = true
  enable_masquerade  = true
  depends_on         = [scaleway_vpc_public_gateway.main, scaleway_vpc_public_gateway_ip.gw01, scaleway_vpc_private_network.pn01]
}

############################################################################################
# Instance creation
resource "scaleway_instance_server" "webserver" {
  provider = scaleway.profile_provider
  name     = "webserver"
  image    = "ubuntu_focal"
  type     = "DEV1-S"

  private_network {
    pn_id = scaleway_vpc_private_network.pn01.id
  }
}

resource "scaleway_instance_server" "database" {
  provider = scaleway.profile_provider
  name     = "database"
  image    = "ubuntu_focal"
  type     = "DEV1-S"

  private_network {
    pn_id = scaleway_vpc_private_network.pn01.id
  }
}

############################################################################################
# Forwarding rules
resource "scaleway_vpc_public_gateway_pat_rule" "webserver-http" {
  provider     = scaleway.profile_provider
  gateway_id   = scaleway_vpc_public_gateway.main.id
  private_ip   = scaleway_vpc_public_gateway_dhcp.main.address
  private_port = 8080
  public_port  = 80
  protocol     = "both"
  depends_on   = [scaleway_vpc_public_gateway.main, scaleway_vpc_gateway_network.main, scaleway_vpc_private_network.pn01]
}

resource "scaleway_vpc_public_gateway_pat_rule" "webserver-ssh" {
  provider     = scaleway.profile_provider
  gateway_id   = scaleway_vpc_public_gateway.main.id
  private_ip   = scaleway_vpc_public_gateway_dhcp.main.address
  private_port = 22
  public_port  = 2221
  protocol     = "both"
  depends_on   = [scaleway_vpc_public_gateway.main, scaleway_vpc_gateway_network.main, scaleway_vpc_private_network.pn01]
}

resource "scaleway_vpc_public_gateway_pat_rule" "database-ssh" {
  provider     = scaleway.profile_provider
  gateway_id   = scaleway_vpc_public_gateway.main.id
  private_ip   = scaleway_vpc_public_gateway_dhcp.main.address
  private_port = 22
  public_port  = 2222
  protocol     = "both"
  depends_on   = [scaleway_vpc_public_gateway.main, scaleway_vpc_gateway_network.main, scaleway_vpc_private_network.pn01]
}
