# Import data from centralus

data "azurerm_resource_group" "centralus-network-peering-rg" {
  name = "centralus-network-peering-rg"
}

data "azurerm_virtual_network" "centralus-vnet" {
  name                = "centralus-vnet"
  resource_group_name = data.azurerm_resource_group.centralus-network-peering-rg.name
}

data "azurerm_subnet" "centralus-vm-subnet" {
  name                 = "centralus-vm-subnet"
  resource_group_name  = data.azurerm_resource_group.centralus-network-peering-rg.name
  virtual_network_name = data.azurerm_virtual_network.centralus-vnet.name
}