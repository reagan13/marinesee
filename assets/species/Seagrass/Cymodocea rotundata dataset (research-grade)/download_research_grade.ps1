# Cymodocea rotundata image dataset downloader - RESEARCH-GRADE only
# Only community-validated (quality_grade=research) iNaturalist observations.
# Run with: powershell -ExecutionPolicy Bypass -File download_research_grade.ps1

$base = "$env:USERPROFILE\Desktop\Cymodocea rotundata dataset (research-grade)"
$taxon = "Cymodocea rotundata"
$enc = [System.Uri]::EscapeDataString($taxon)

$inDir = Join-Path $base "inaturalist"
$tmp  = Join-Path $base "tmp"
New-Item -ItemType Directory -Force -Path $inDir, $tmp | Out-Null

$metadata = @()

function Get-JsonViaCurl($url, $outJson) {
    & curl.exe -s --max-time 60 -A "Mozilla/5.0" $url -o $outJson
    if ((Test-Path $outJson) -and (Get-Item $outJson).Length -gt 50) {
        return (Get-Content $outJson -Raw | ConvertFrom-Json)
    }
    return $null
}

function Save-ImageViaCurl($url, $dest, $id, $source) {
    $ext = "jpg"
    if ($url -match "\.(jpe?g|png|gif|bmp)(?:$|&)") { $ext = $matches[1] }
    $out = Join-Path $dest ("$id" + "_$source.$ext")
    & curl.exe -s --max-time 40 -L -A "Mozilla/5.0" $url -o $out
    if (-not (Test-Path $out) -or (Get-Item $out).Length -lt 1000) {
        if (Test-Path $out) { Remove-Item $out -Force }
        return $null
    }
    return $out
}

Write-Host "== Fetching RESEARCH-GRADE iNaturalist observations ==" -ForegroundColor Cyan
$page = 1
$total = 0
while ($page -le 30) {
    $url = "https://api.inaturalist.org/v1/observations?taxon_name=$enc&photos=true&quality_grade=research&per_page=30&page=$page"
    $jsonPath = Join-Path $tmp "inat_page_$page.json"
    $resp = Get-JsonViaCurl $url $jsonPath
    if (-not $resp -or -not $resp.results -or $resp.results.Count -eq 0) { break }

    foreach ($o in $resp.results) {
        $obsId = $o.id
        $pi = 0
        foreach ($p in $o.photos) {
            $pi++
            $imgUrl = $p.url.Replace("square", "large")
            $dest = Save-ImageViaCurl $imgUrl $inDir ("$obsId" + "_$pi") "inat"
            if ($dest) {
                $total++
                $metadata += [PSCustomObject]@{
                    source         = "inaturalist"
                    observation    = $obsId
                    photo_index    = $pi
                    license        = $p.license
                    quality_grade  = $o.quality_grade
                    file           = Split-Path $dest -Leaf
                    url            = $imgUrl
                }
            }
        }
    }
    Write-Host "  page $page done, total so far: $total"
    $page++
}
Write-Host "Research-grade images downloaded: $total" -ForegroundColor Green

$metaPath = Join-Path $base "metadata.csv"
$metadata | Export-Csv -Path $metaPath -NoTypeInformation
Remove-Item $tmp -Recurse -Force -ErrorAction SilentlyContinue
Write-Host "Saved metadata to $metaPath" -ForegroundColor Green
Write-Host "DONE. Total images: $($metadata.Count)" -ForegroundColor Yellow
