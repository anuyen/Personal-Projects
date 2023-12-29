resource "azurerm_network_security_group" "eastus-vm-subnet-nsg" {
  name                = "eastus-vm-subnet-nsg"
  location            = azurerm_resource_group.eastus-network-peering-rg.location
  resource_group_name = azurerm_resource_group.eastus-network-peering-rg.name

  # Allow inbound traffic from AzureBastionSubnet to eastus-vm-subnet
  # 22 --> ssh, 3389 --> rdp, both uses tcp
  security_rule {
    name                       = "AllowBastionRdpSshInbound"
    priority                   = 500
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_ranges    = ["3389", "22"]
    source_address_prefix      = azurerm_subnet.AzureBastionSubnet.address_prefixes[0]
    destination_address_prefix = azurerm_subnet.eastus-vm-subnet.address_prefixes[0]
  }

  security_rule {
    name                       = "AllowVmSshInbound"
    priority                   = 510
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_ranges    = ["22"]
    source_address_prefix      = data.azurerm_subnet.centralus-vm-subnet.address_prefixes[0]
    destination_address_prefix = azurerm_subnet.eastus-vm-subnet.address_prefixes[0]
  }

  # Deny any other inbounds
  security_rule {
    name                       = "DenyAllInbound"
    priority                   = 1000
    direction                  = "Inbound"
    access                     = "Deny"
    protocol                   = "*"
    source_port_range          = "*"
    destination_port_range     = "*"
    source_address_prefix      = "*"
    destination_address_prefix = azurerm_subnet.eastus-vm-subnet.address_prefixes[0]
  }

  security_rule {
    name                       = "AllowSshOutbound"
    priority                   = 400
    direction                  = "Outbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_ranges    = ["22"]
    source_address_prefix      = azurerm_subnet.eastus-vm-subnet.address_prefixes[0]
    destination_address_prefix = data.azurerm_subnet.centralus-vm-subnet.address_prefixes[0]
  }

  # Allow any outbound from subnet to subnet
  security_rule {
    name                       = "AllowSubnetOutbound"
    priority                   = 500
    direction                  = "Outbound"
    access                     = "Allow"
    protocol                   = "*"
    source_port_range          = "*"
    destination_port_range     = "*"
    source_address_prefix      = azurerm_subnet.eastus-vm-subnet.address_prefixes[0]
    destination_address_prefix = azurerm_subnet.eastus-vm-subnet.address_prefixes[0]
  }

  # Deny any outbound from subnet
  security_rule {
    name                       = "DenyAllOutbound"
    priority                   = 1000
    direction                  = "Outbound"
    access                     = "Deny"
    protocol                   = "*"
    source_port_range          = "*"
    destination_port_range     = "*"
    source_address_prefix      = azurerm_subnet.eastus-vm-subnet.address_prefixes[0]
    destination_address_prefix = "*"
  }

}

# Associate nsg with vm-vnet
resource "azurerm_subnet_network_security_group_association" "nsg-eastus-vm-subnet-association" {
  network_security_group_id = azurerm_network_security_group.eastus-vm-subnet-nsg.id
  subnet_id                 = azurerm_subnet.eastus-vm-subnet.id
}