$ProgressPreference = "SilentlyContinue"
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12 -bor [Net.SecurityProtocolType]::Tls11 -bor [Net.SecurityProtocolType]::Tls
[System.Net.ServicePointManager]::Expect100Continue = $false
[System.Net.ServicePointManager]::DefaultConnectionLimit = 10
[System.Net.WebRequest]::DefaultWebProxy = $null
[System.Net.ServicePointManager]::ServerCertificateValidationCallback = { $true }
[System.Net.HttpWebRequest]::DefaultMaximumErrorResponseLength = 1048576
function Get-Json($url) {
    try {
        $req = [System.Net.HttpWebRequest]::Create($url)
        $req.Timeout = 60000
        $req.UserAgent = "Mozilla/5.0"
        $rs = $req.GetResponse().GetResponseStream()
        $sr = New-Object System.IO.StreamReader($rs)
        $j = $sr.ReadToEnd(); $sr.Close(); $rs.Close()
        return $j | ConvertFrom-Json
    } catch { Write-Host "FETCHERR: $($_.Exception.Message)"; return $null }
}
$enc=[System.Uri]::EscapeDataString('Cymodocea rotundata')
$url="https://api.inaturalist.org/v1/observations?taxon_name=$enc&photos=true&per_page=30&page=1"
$r = Get-Json $url
if($r){ "OK results=$($r.results.Count)" } else { "NULL" }
