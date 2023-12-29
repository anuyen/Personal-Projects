# Import data from eastus

data "azurerm_resource_group" "eastus-network-peering-rg" {
  name = "eastus-network-peering-rg"
}

data "azurerm_virtual_network" "eastus-vnet" {
  name                = "eastus-vnet"
  resource_group_name = data.azurerm_resource_group.eastus-network-peering-rg.name
}

data "azurerm_subnet" "eastus-vm-subnet" {
  name                 = "eastus-vm-subnet"
  resource_group_name  = data.azurerm_resource_group.eastus-network-peering-rg.name
  virtual_network_name = data.azurerm_virtual_network.eastus-vnet.name
}