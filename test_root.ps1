$r1 = Invoke-WebRequest -Uri 'https://govrag-v3-func.azurewebsites.net' -UseBasicParsing -TimeoutSec 15
Write-Host "Root Status:" $r1.StatusCode
$snippet = $r1.Content.Substring(0, 200)
Write-Host "Root Content:" $snippet

$r2 = Invoke-WebRequest -Uri 'https://govrag-v3-func.azurewebsites.net/home' -UseBasicParsing -TimeoutSec 15
Write-Host "/home Status:" $r2.StatusCode
$hasApp = $r2.Content.Contains("Alfalah")
Write-Host "/home HasAlfalah: $hasApp"
$hasForm = $r2.Content.Contains("resume-input")
Write-Host "/home HasForm: $hasForm"
