$currentPath = Get-Location

# Init both directories in parallel
$job1 = Start-Job -ScriptBlock { 
    param($path) terraform -chdir="$path\eastus" destroy --auto-approve 
} -ArgumentList $currentPath
$job2 = Start-Job -ScriptBlock { 
    param($path) terraform -chdir="$path\centralus" destroy --auto-approve
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