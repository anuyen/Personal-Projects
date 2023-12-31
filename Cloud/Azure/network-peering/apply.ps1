# Due to dependencies, resources have to be deployed in this order

# Start the timer
$startTime = Get-Date

function Invoke-Async-Commands {
    <#
    Description:
        This function takes in paths and commands.
        If more than one paths is given, the series of commands are ran asynchronously in each folder.
        The series of commands themselves are ran sequentially.

        The function will wait for jobs to finish and write out output before removing the job and exiting the function
    Variable:
        paths: input - an array of paths
        commands: input - an array of commands
    Use:
        With async function call, the duration of the function will as long as the longest single-command duration
    #>
    param(
        [string[]]$paths,
        [string[]]$commands
    )

    $jobs = @()
    foreach ($path in $paths){
        # When Invoke-Expression is used, multiple commands can be
        # sequentially invoked if they have separated by "";"" in that string

        # This variable will collect commands in the following manner
        # "cmd1,cmd2,..."
        $final_commands = ""
        foreach ($command in $commands){
            $final_commands += "terraform -chdir=`"$path`" $command;"
        }

        # Start job
        $jobs += Start-Job -ScriptBlock {
            param($final_commands)
                Write-Host "-----------------------------------------------------------------" -ForegroundColor Cyan
                Write-Host "For command:" -ForegroundColor Cyan
                Write-Host $final_commands -ForegroundColor Cyan
                Invoke-Expression $final_commands
        } -ArgumentList $final_commands
    } #This block will iteratively start each job, but does not wait for the last job to finish
    #Before starting another job --> they are essentially started at the same time

    # Wait for jobs to be done
    Wait-Job $jobs > $null
    do {
        foreach ($job in $jobs) {
            if ($job.State -eq 'Failed') {
                Write-Output "Job $($job.Id) failed with error: $($job.JobStateInfo.Reason.Message)"
            } else {
                $result = Receive-Job $job
                Write-Output $result  # Print the result to the terminal
            }
        }
    } # Waiting for job to be done is not enough, I found that completed jobs are not really completed
    while (($jobs | Where-Object HasMoreData).Count -gt 0) # checks if they still got outputs

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