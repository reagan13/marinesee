$ProgressPreference = "SilentlyContinue"
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
[System.Net.WebRequest]::DefaultWebProxy = $null
function Get-Json($url) {
    try {
        $req = [System.Net.HttpWebRequest]::Create($url)
        $req.Timeout = 60000
        $req.UserAgent = "Mozilla/5.0"
        $rs = $req.GetResponse().GetResponseStream()
        $sr = New-Object System.IO.StreamReader($rs)
        $j = $sr.ReadToEnd(); $sr.Close(); $rs.Close()
        return $j | ConvertFrom-Json
    } catch { Write-Host "FETCHERR: $($_.Exception.GetType().Name) : $($_.Exception.Message)"; return $null }
}
$enc=[System.Uri]::EscapeDataString('Cymodocea rotundata')
$url="https://api.inaturalist.org/v1/observations?taxon_name=$enc&photos=true&per_page=30&page=1"
$r = Get-Json $url
if($r){ "OK results=$($r.results.Count)" } else { "NULL returned" }
