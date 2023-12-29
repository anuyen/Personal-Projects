# Due to dependencies, resources have to be deployed in this order

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

# Create Resource Groups in parallel
$job3 = Start-Job -ScriptBlock { 
    param($path) terraform -chdir="$path\eastus" apply -target azurerm_resource_group.eastus-network-peering-rg --auto-approve -compact-warnings
} -ArgumentList $currentPath
$job4 = Start-Job -ScriptBlock { 
    param($path) terraform -chdir="$path\centralus" apply -target azurerm_resource_group.centralus-network-peering-rg --auto-approve -compact-warnings
} -ArgumentList $currentPath

# Wait for both jobs to complete
Wait-Job $job3, $job4
do {
    $result3 = Receive-Job $job3; $result4 = Receive-Job $job4
    # Process result if needed
}
while (($job3.HasMoreData) -or ($job4.HasMoreData))

$result3; $result4
Remove-Job $job3, $job4

# Create Virtual Networks and their VM Subnets
$job5 = Start-Job -ScriptBlock {
    param($path) 
    terraform -chdir="$path\eastus" apply -target azurerm_virtual_network.eastus-vnet --auto-approve -compact-warnings
    terraform -chdir="$path\eastus" apply -target azurerm_subnet.eastus-vm-subnet --auto-approve -compact-warnings
} -ArgumentList $currentPath

$job6 = Start-Job -ScriptBlock {
    param($path) 
    terraform -chdir="$path\centralus" apply -target azurerm_virtual_network.centralus-vnet --auto-approve -compact-warnings
    terraform -chdir="$path\centralus" apply -target azurerm_subnet.centralus-vm-subnet --auto-approve -compact-warnings
} -ArgumentList $currentPath

# Wait for both jobs to complete
Wait-Job $job5, $job6
do {
    $result5 = Receive-Job $job5; $result6 = Receive-Job $job6
    # Process result if needed
}
while (($job5.HasMoreData) -or ($job6.HasMoreData))

$result5; $result6
Remove-Job $job5, $job6

# Apply remaining configuration in parallel
$job7 = Start-Job -ScriptBlock { 
    param($path) terraform -chdir="$path\eastus" apply --auto-approve
} -ArgumentList $currentPath
$job8 = Start-Job -ScriptBlock { 
    param($path) terraform -chdir="$path\centralus" apply --auto-approve
} -ArgumentList $currentPath

# Wait
Wait-Job $job7, $job8
do {
    $result7 = Receive-Job $job7; $result8 = Receive-Job $job8
    # Process result if needed
}
while (($job7.HasMoreData) -or ($job8.HasMoreData))

# print results
$result7; $result8
Remove-Job $job7, $job8