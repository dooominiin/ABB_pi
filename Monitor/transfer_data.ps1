$source = "mister@192.168.43.203:/home/mister/Desktop/ABB_Projekt/log.txt"
$destination = "Monitor"

while ($true) {
    Start-Sleep -Seconds 5  # Warte 5 Sekunden

    try {
        $process = Start-Process -NoNewWindow -PassThru -Wait -FilePath "scp" -ArgumentList $source, $destination
        $exitCode = $process.ExitCode

        if ($exitCode -eq 0) {
            Write-Host "SCP operation completed successfully."
        } else {
            Write-Host "SCP operation failed with exit code: $exitCode"
        }
    } catch {
        Write-Host "An error occurred: $_"
    }
}
