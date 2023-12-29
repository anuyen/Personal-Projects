# Establish tunnelling

$vmId = terraform -chdir=".\eastus" output -raw vm-id

az network bastion tunnel `
    --name "bastion-host" `
    --resource-group "eastus-network-peering-rg" `
    --target-resource-id $vmId `
    --resource-port "22" --port "6969"