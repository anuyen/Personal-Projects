# Azure Virtual Network Peering with Terraform

## What is VNet Peering?

Virtual network peering enables you to connect two or more Virtual Networks in Azure.

Read more: https://learn.microsoft.com/en-us/azure/virtual-network/virtual-network-peering-overview

## Project Goal

In this project, I will set up a VM in Central US that is only accessible via ssh connection, though peering, from a VM in East US. The VM is East US is accessible for ssh over the internet via Bastion Tunneling.

## Project Components

I will set up the following (similar to diagram below) with Terraform:

    _Region: East US
        Virtual Network
            Azure Bastion Subnet
                Azure Bastion Host
            VM Subnet
                east-us-VM
    
    _Region: Central US
        Virtual Network
            VM Subnet
                central-us-VM

![project-diagram](https://learn.microsoft.com/en-us/azure/virtual-network/media/tutorial-connect-virtual-networks-portal/resources-diagram.png)

### Azure Bastion

Used exact code from an earlier project

https://github.com/antnguyen72/Personal-Projects/tree/main/Cloud/Azure/azure-bastion

### Peering Configuration

Since I am using Virtual Networks in different regions, the "allow_gateway_transit" option is set to false for Global peering. I honestly am confused about this option, even after reading multiple documents. I think it's better to keep it in mind and re-explore it later when I have more knowledge about networking.

Since SSH is a 2-way connection, peering also has to be 2-way.

Read more: https://learn.microsoft.com/en-us/azure/vpn-gateway/vpn-gateway-peering-gateway-transit

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

### Network Security Group Configuration

For subnet network security groups, where my VM resides, I allowed both outbound and inbound TCP connections at port 22. (SSH is a two-way connection)

    # Allow ssh inbound
    security_rule {
        name                       = "AllowSshInbound"
        priority                   = 500
        direction                  = "Inbound"
        access                     = "Allow"
        protocol                   = "Tcp"
        source_port_range          = "*"
        destination_port_ranges    = ["22"]
        source_address_prefix      = data.azurerm_subnet.eastus-vm-subnet.address_prefixes[0]
        destination_address_prefix = azurerm_subnet.centralus-vm-subnet.address_prefixes[0]
    }

    # Allow ssh outbound (ssh is a 2-way communication)
    security_rule {
        name                       = "AllowSshOutbound"
        priority                   = 500
        direction                  = "Outbound"
        access                     = "Allow"
        protocol                   = "Tcp"
        source_port_range          = "*"
        destination_port_ranges    = ["22"]
        source_address_prefix      = azurerm_subnet.centralus-vm-subnet.address_prefixes[0]
        destination_address_prefix = data.azurerm_subnet.eastus-vm-subnet.address_prefixes[0]
    }

### Deployment orchestration with PowerShell

I used PowerShell because:

* Resource Group is to be created first. Maybe it's the way I wrote my code, but I saw that resource groups must be created before other resources.
* Certain resources depend on data modules. When these resources are deployed, they check in with the data module, and, in turn, the resource pointed at by the data module is checked. If I run apply on all, resources mentioned by data modules might not have been created yet.

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
    These resources are imported for peering configuration above.

To solve this problem, I used PowerShell to deploy in the following order:

1.  Init
2.  Deploy Resource Groups
3.  Deploy Virtual Networks and Subnets
4.  Deploy all (Virtual Machines, Bastion Host, Network Security Group)

Using a code structure like below, I applied each corresponding resource on each region in parallel to speed up deployment.

        $currentPath = Get-Location

        # Init both directories in parallel
        $job1 = Start-Job -ScriptBlock { 
            param($path) terraform -chdir="$path\eastus" init 
        } -ArgumentList $currentPath
        $job2 = Start-Job -ScriptBlock { 
            param($path) terraform -chdir="$path\centralus" init 
        } -ArgumentList $currentPath

        # Wait
        Wait-Job $job1, $job2
        do {
            $result1 = Receive-Job $job1; $result2 = Receive-Job $job2
            # Process result if needed
        }
        while (($job1.HasMoreData) -or ($job2.HasMoreData))

        # print results
        $result1; $result2
        Remove-Job $job1, $job2

## Steps:

1. With PowerShell Terminal, run apply.ps1 deploy resources (Maybe take up to 15 minutes, Bastion takes a while to set up):
    
        .\apply.ps1

    ![resources](./pics/resources.png)

2. Wait for Resource to deploy, then run tunnel.ps1 to establish Bastion tunneling. This allows for ssh connection to East US VM from your computer:

        .\tunnel.ps1
    
    ![peering](./pics/peering.png)

3. On a new Terminal Window, test ssh connection to East US VM (Use your preferrred method of authentication, I used password):

        ssh anguyen@127.0.0.1 -p 6969

        # Note: 127.0.0.1 is Azure's IP. Literally SSH to this.
    
    ![east-us-vm-ssh-success](./pics/eastus%20ssh.png)

4. Test ssh connection from East US VM to Central US VM:

        ssh anguyen@<Central-US-VM-IP>
    
    ![central-us-vm-ssh-sucess](./pics/centralus%20ssh.png)

5. Clean up your cloud resources:

        .\destroy.ps1
    
    

# Done!