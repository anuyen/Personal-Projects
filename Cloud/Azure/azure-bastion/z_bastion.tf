resource "azurerm_public_ip" "bastion-public-ip" {
  name = "bastion-public-ip"
  location = azurerm_resource_group.azure-bastion-rg.location
  resource_group_name = azurerm_resource_group.azure-bastion-rg.name
  sku = "Standard"
  allocation_method = "Static"
}

resource "azurerm_bastion_host" "bastion-host" {
  name = "bastion-host"
  location = azurerm_resource_group.azure-bastion-rg.location
  resource_group_name = azurerm_resource_group.azure-bastion-rg.name
  sku = "Standard"
  
  copy_paste_enabled = true
  file_copy_enabled = true
  shareable_link_enabled = true
  tunneling_enabled = true

  ip_configuration {
    name = "bastion-ip-conf"
    subnet_id = azurerm_subnet.AzureBastionSubnet.id
    public_ip_address_id = azurerm_public_ip.bastion-public-ip.id
  }
}