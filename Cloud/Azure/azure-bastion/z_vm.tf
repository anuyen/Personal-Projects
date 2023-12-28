# Create an SSH key
resource "azurerm_ssh_public_key" "my-ssh-key" {
  name                = "my-ssh-key"
  resource_group_name = azurerm_resource_group.azure-bastion-rg.name
  location            = azurerm_resource_group.azure-bastion-rg.location
  public_key          = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDtgla48VfFedbWi0RD29yKeE34SoxuT1r9q+EaCzFVYf4RtXejbDiQ2SUqX8ZpFq0MyGY9sxIbemHZjhDHo0hyAdH5t792QL5VGfy0oXvkiV8r/XE5tkJMn+a63BzsA9WB56WchQBxnpAga0Q+yExt/t3aux/sferxS8FucMaB3NCOwdgMRcowupNkvl1FFOY33TikrHWu/zD70wIT9DwbZqTGk19G3NeWPZaZzWAqFXy++JY+9WnAjdQnXwansX3oNwrO2CQqUoA2BTB8tUIzdm6Fym2Ut3lgFUFqThK9r7Fh9fekcJFJzr1OsOME5KriO+FZaCu7Z3KjqWzBAabJBFXfL3/kAZkSYaRudY7lHgE0J91wqO5hK4gEcSkFsWIfOZe7rMPsKn4KS96CHqLNZ+YV6zrDkIFHpo7G+D25/Rh5CBaHvnj2pnxTHGXJrvqXhXDgRUbdzuOfFFGX+CRYuGZYsa5Kiw+ymAXLn9JrNJMZJEzghkw9PVRo9pvjMC0= anguyen@BO-PC"
}

resource "azurerm_network_interface" "vm1-nic" {
  name = "vm1-nic"
  location = azurerm_resource_group.azure-bastion-rg.location
  resource_group_name = azurerm_resource_group.azure-bastion-rg.name

  ip_configuration {
    name = "vm1-nic1-conf"
    subnet_id = azurerm_subnet.vm-subnet.id
    private_ip_address_allocation = "Dynamic"
  }
}

resource "azurerm_linux_virtual_machine" "vm1" {
  name = "vm1"
  resource_group_name = azurerm_resource_group.azure-bastion-rg.name
  location = azurerm_resource_group.azure-bastion-rg.location
  size = "Standard_B1s"
  admin_username = "anguyen"
  admin_password = "ExtremelyHardToGuessPassword11999!*(@)"
  disable_password_authentication = false

  network_interface_ids = [
    azurerm_network_interface.vm1-nic.id
  ]

  os_disk {
    caching = "None"
    storage_account_type = "Standard_LRS"
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-jammy"
    sku       = "22_04-lts"
    version   = "latest"
  }
}