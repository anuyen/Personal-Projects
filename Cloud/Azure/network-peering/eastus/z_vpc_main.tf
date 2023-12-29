# Virtual Network
resource "azurerm_virtual_network" "eastus-vnet" {
  name                = "eastus-vnet"
  address_space       = ["10.40.2.0/24"]
  location            = azurerm_resource_group.eastus-network-peering-rg.location
  resource_group_name = azurerm_resource_group.eastus-network-peering-rg.name
}

# Subnets
resource "azurerm_subnet" "AzureBastionSubnet" {
  name                 = "AzureBastionSubnet"
  resource_group_name  = azurerm_resource_group.eastus-network-peering-rg.name
  virtual_network_name = azurerm_virtual_network.eastus-vnet.name
  address_prefixes     = ["10.40.2.0/25"]
}

resource "azurerm_subnet" "eastus-vm-subnet" {
  name                 = "eastus-vm-subnet"
  resource_group_name  = azurerm_resource_group.eastus-network-peering-rg.name
  virtual_network_name = azurerm_virtual_network.eastus-vnet.name
  address_prefixes     = ["10.40.2.128/25"]
}