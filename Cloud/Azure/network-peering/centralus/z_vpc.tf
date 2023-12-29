# Virtual Network
resource "azurerm_virtual_network" "centralus-vnet" {
  name                = "centralus-vnet"
  address_space       = ["10.30.2.0/26"]
  location            = azurerm_resource_group.centralus-network-peering-rg.location
  resource_group_name = azurerm_resource_group.centralus-network-peering-rg.name
}

resource "azurerm_subnet" "centralus-vm-subnet" {
  name                 = "centralus-vm-subnet"
  resource_group_name  = azurerm_resource_group.centralus-network-peering-rg.name
  virtual_network_name = azurerm_virtual_network.centralus-vnet.name
  address_prefixes     = ["10.30.2.0/27"]
}