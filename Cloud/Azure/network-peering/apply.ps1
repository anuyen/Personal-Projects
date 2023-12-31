# Due to dependencies, resources have to be deployed in this order

# Start the timer
$startTime = Get-Date

function Invoke-Async-Commands {
    param(
        [string[]]$paths,
        [string[]]$commands
    )

    $jobs = @()
    foreach ($path in $paths){
        # When Invoke-Expression is used, multiple commands sequentially can be
        # invoked if they have separed by ; in that string
        $final_commands = ""
        foreach ($command in $commands){
            $final_commands += "terraform -chdir=`"$path`" $command;"
        }
        $jobs += Start-Job -ScriptBlock {
            param($final_commands)
                Write-Host "-----------------------------------------------------------------" -ForegroundColor Cyan
                Write-Host "For command:" -ForegroundColor Cyan
                Write-Host $final_commands -ForegroundColor Cyan
                Invoke-Expression $final_commands
        } -ArgumentList $final_commands
    }

    # Wait
    Wait-Job $jobs > $null
    do {
        foreach ($job in $jobs) {
            if ($job.State -eq 'Failed') {
                Write-Output "Job $($job.Id) failed with error: $($job.JobStateInfo.Reason.Message)"
            } else {
                $result = Receive-Job $job
                Write-Output $result  # Print the result to the terminal
                # Process result if needed
            }
        }
    }
    while (($jobs | Where-Object HasMoreData).Count -gt 0)

    $jobs | Remove-Job
}

$path1 = Join-Path (Get-Location) "eastus"
$path2 = Join-Path (Get-Location) "centralus"
$paths = @($path1, $path2)

# Init both directories
Invoke-Async-Commands `
    -commands "init" `
    -paths $paths

# Create Resource Groups
Invoke-Async-Commands `
    -commands "apply -target azurerm_resource_group.rg --auto-approve -compact-warnings" `
    -paths $paths

# Create Virtual Network and their VM Subnets
Invoke-Async-Commands `
    -commands "apply -target azurerm_virtual_network.vnet --auto-approve -compact-warnings", `
    "apply -target azurerm_subnet.vm-subnet --auto-approve -compact-warnings" `
    -paths $paths

# Apply remaining configuration
Invoke-Async-Commands `
    -commands "apply --auto-approve" `
    -paths $paths

# Calculate the time difference
$endTime = Get-Date
$timeTaken = $endTime - $startTime

# Output the time taken
$minutes = [math]::Floor($timeTaken.TotalMinutes)
$seconds = [math]::Round($timeTaken.TotalSeconds - $minutes * 60)
Write-Output "`nTotal time taken: $minutes minute(s) and $seconds second(s)"