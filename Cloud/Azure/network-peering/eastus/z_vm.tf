resource "azurerm_network_interface" "vm1-nic" {
  name                = "eastus-vm1-nic"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  ip_configuration {
    name                          = "vm1-nic1-conf"
    subnet_id                     = azurerm_subnet.vm-subnet.id
    private_ip_address_allocation = "Dynamic"
  }
}

resource "azurerm_linux_virtual_machine" "vm1" {
  name                            = "eastus-vm1"
  resource_group_name             = azurerm_resource_group.rg.name
  location                        = azurerm_resource_group.rg.location
  size                            = "Standard_B1s"
  admin_username                  = "anguyen"
  admin_password                  = "ExtremelyHardToGuessPassword11999!*(@)"
  disable_password_authentication = false

  network_interface_ids = [
    azurerm_network_interface.vm1-nic.id
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
  value = azurerm_linux_virtual_machine.vm1.id
}