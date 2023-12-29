# Have to use global peering

resource "azurerm_virtual_network_peering" "peer-eastus-to-centralus" {
  name                      = "peer-eastus-to-centralus"
  resource_group_name       = data.azurerm_resource_group.eastus-network-peering-rg.name
  virtual_network_name      = data.azurerm_virtual_network.eastus-vnet.name
  remote_virtual_network_id = azurerm_virtual_network.centralus-vnet.id

  allow_virtual_network_access = true
  allow_forwarded_traffic      = true

  # `allow_gateway_transit` must be set to false for vnet Global Peering
  allow_gateway_transit = false
}

resource "azurerm_virtual_network_peering" "peer-centralus-to-eastus" {
  name                      = "peer-centralus-to-eastus"
  resource_group_name       = azurerm_resource_group.centralus-network-peering-rg.name
  virtual_network_name      = azurerm_virtual_network.centralus-vnet.name
  remote_virtual_network_id = data.azurerm_virtual_network.eastus-vnet.id

  allow_virtual_network_access = true
  allow_forwarded_traffic      = true

  # `allow_gateway_transit` must be set to false for vnet Global Peering
  allow_gateway_transit = false
}