# Virtual Network
resource "azurerm_virtual_network" "vnet2" {
  name = "vnet2"
  address_space = ["10.40.2.0/24"]
  location = azurerm_resource_group.azure-bastion-rg.location
  resource_group_name = azurerm_resource_group.azure-bastion-rg.name
}

# Subnets
resource "azurerm_subnet" "AzureBastionSubnet" {
  name = "AzureBastionSubnet"
  resource_group_name = azurerm_resource_group.azure-bastion-rg.name
  virtual_network_name = azurerm_virtual_network.vnet2.name
  address_prefixes = ["10.40.2.0/25"]
}

resource "azurerm_subnet" "vm-subnet" {
  name = "vm-subnet"
  resource_group_name = azurerm_resource_group.azure-bastion-rg.name
  virtual_network_name = azurerm_virtual_network.vnet2.name
  address_prefixes     = ["10.40.2.128/25"]
}