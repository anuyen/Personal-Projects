resource "azurerm_network_interface" "eastus-vm-nic" {
  name                = "eastus-vm-nic"
  location            = azurerm_resource_group.eastus-network-peering-rg.location
  resource_group_name = azurerm_resource_group.eastus-network-peering-rg.name

  ip_configuration {
    name                          = "eastus-vm-nic1-conf"
    subnet_id                     = azurerm_subnet.eastus-vm-subnet.id
    private_ip_address_allocation = "Dynamic"
  }
}

resource "azurerm_linux_virtual_machine" "eastus-vm" {
  name                            = "eastus-vm"
  resource_group_name             = azurerm_resource_group.eastus-network-peering-rg.name
  location                        = azurerm_resource_group.eastus-network-peering-rg.location
  size                            = "Standard_B1s"
  admin_username                  = "anguyen"
  admin_password                  = "ExtremelyHardToGuessPassword11999!*(@)"
  disable_password_authentication = false

  network_interface_ids = [
    azurerm_network_interface.eastus-vm-nic.id
  ]

  os_disk {
    caching              = "None"
    storage_account_type = "Standard_LRS"
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-jammy"
    sku       = "22_04-lts"
    version   = "latest"
  }
}

output "vm-id" {
  value = azurerm_linux_virtual_machine.eastus-vm.id
}