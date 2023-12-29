resource "azurerm_network_security_group" "centralus-vm-subnet-nsg" {
  name                = "centralus-vm-subnet-nsg"
  location            = azurerm_resource_group.centralus-network-peering-rg.location
  resource_group_name = azurerm_resource_group.centralus-network-peering-rg.name

  # Allow ssh inbound from eastus
  security_rule {
    name                       = "AllowSshInbound"
    priority                   = 500
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_ranges    = ["22"]
    source_address_prefix      = data.azurerm_subnet.eastus-vm-subnet.address_prefixes[0]
    destination_address_prefix = azurerm_subnet.centralus-vm-subnet.address_prefixes[0]
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
    destination_address_prefix = azurerm_subnet.centralus-vm-subnet.address_prefixes[0]
  }

  # Allow ssh outbound to eastus (ssh is a two way communication)
  security_rule {
    name                       = "AllowSshOutbound"
    priority                   = 500
    direction                  = "Outbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_ranges    = ["22"]
    source_address_prefix      = azurerm_subnet.centralus-vm-subnet.address_prefixes[0]
    destination_address_prefix = data.azurerm_subnet.eastus-vm-subnet.address_prefixes[0]
  }

  # Allow any outbound from subnet to subnet
  security_rule {
    name                       = "AllowSubnetOutbound"
    priority                   = 550
    direction                  = "Outbound"
    access                     = "Allow"
    protocol                   = "*"
    source_port_range          = "*"
    destination_port_range     = "*"
    source_address_prefix      = azurerm_subnet.centralus-vm-subnet.address_prefixes[0]
    destination_address_prefix = azurerm_subnet.centralus-vm-subnet.address_prefixes[0]
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
    source_address_prefix      = azurerm_subnet.centralus-vm-subnet.address_prefixes[0]
    destination_address_prefix = "*"
  }
}

# Associate nsg with vm-vnet
resource "azurerm_subnet_network_security_group_association" "nsg-vm-subnet-association" {
  network_security_group_id = azurerm_network_security_group.centralus-vm-subnet-nsg.id
  subnet_id                 = azurerm_subnet.centralus-vm-subnet.id
}