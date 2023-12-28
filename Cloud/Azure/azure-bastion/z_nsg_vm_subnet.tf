resource "azurerm_network_security_group" "vm-subnet-nsg" {
  name = "vm-subnet-nsg"
  location = azurerm_resource_group.azure-bastion-rg.location
  resource_group_name = azurerm_resource_group.azure-bastion-rg.name

    # Allow inbound traffic from AzureBastionSubnet to vm-subnet
    # 22 --> ssh, 3389 --> rdp, both uses tcp
  security_rule {
    name                       = "AllowRdpSshInbound"
    priority                   = 500
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_ranges    = ["3389","22"]
    source_address_prefix      = azurerm_subnet.AzureBastionSubnet.address_prefixes[0]
    destination_address_prefix = azurerm_subnet.vm-subnet.address_prefixes[0]
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
    destination_address_prefix = azurerm_subnet.vm-subnet.address_prefixes[0]
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
    source_address_prefix      = azurerm_subnet.vm-subnet.address_prefixes[0]
    destination_address_prefix = azurerm_subnet.vm-subnet.address_prefixes[0]
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
    source_address_prefix      = azurerm_subnet.vm-subnet.address_prefixes[0]
    destination_address_prefix = "*"
  }

}

# Associate nsg with vm-vnet
resource "azurerm_subnet_network_security_group_association" "nsg-vm-subnet-association" {
  network_security_group_id = azurerm_network_security_group.vm-subnet-nsg.id
  subnet_id = azurerm_subnet.vm-subnet.id
}