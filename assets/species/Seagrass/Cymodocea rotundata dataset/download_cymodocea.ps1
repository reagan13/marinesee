# Cymodocea rotundata image dataset downloader (curl-based, reliable)
# Sources: iNaturalist (CC-BY-NC) and GBIF occurrence media
# Run with: powershell -ExecutionPolicy Bypass -File download_cymodocea.ps1

$base = "$env:USERPROFILE\Desktop\Cymodocea rotundata dataset"
$taxon = "Cymodocea rotundata"
$enc = [System.Uri]::EscapeDataString($taxon)

$inDir = Join-Path $base "inaturalist"
$gbDir = Join-Path $base "gbif"
$tmp  = Join-Path $base "tmp"
New-Item -ItemType Directory -Force -Path $inDir, $gbDir, $tmp | Out-Null

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

# ---------- iNaturalist ----------
Write-Host "== Fetching iNaturalist observations ==" -ForegroundColor Cyan
$page = 1
$total = 0
while ($page -le 15) {
    $url = "https://api.inaturalist.org/v1/observations?taxon_name=$enc&photos=true&per_page=30&page=$page"
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
                    source = "inaturalist"; observation = $obsId; photo_index = $pi
                    license = $p.license; file = Split-Path $dest -Leaf; url = $imgUrl
                }
            }
        }
    }
    Write-Host "  page $page done, total so far: $total"
    $page++
}
Write-Host "iNaturalist images downloaded: $total" -ForegroundColor Green

# ---------- GBIF ----------
Write-Host "== Fetching GBIF occurrence media ==" -ForegroundColor Cyan
$gurl = "https://api.gbif.org/v1/occurrence/search?speciesKey=179116397&mediaType=StillImage&limit=300"
$gjsonPath = Join-Path $tmp "gbif.json"
$gresp = Get-JsonViaCurl $gurl $gjsonPath
$gcount = 0
if ($gresp -and $gresp.results) {
    foreach ($occ in $gresp.results) {
        $occId = $occ.key
        if ($occ.media) {
            $mi = 0
            foreach ($m in $occ.media) {
                $mi++
                if ($m.identifier) {
                    $dest = Save-ImageViaCurl $m.identifier $gbDir ("$occId" + "_$mi") "gbif"
                    if ($dest) {
                        $gcount++
                        $metadata += [PSCustomObject]@{
                            source = "gbif"; observation = $occId; photo_index = $mi
                            license = $m.license; file = Split-Path $dest -Leaf; url = $m.identifier
                        }
                    }
                }
            }
        }
    }
}
Write-Host "GBIF images downloaded: $gcount" -ForegroundColor Green

# ---------- Metadata ----------
$metaPath = Join-Path $base "metadata.csv"
$metadata | Export-Csv -Path $metaPath -NoTypeInformation
Remove-Item $tmp -Recurse -Force -ErrorAction SilentlyContinue
Write-Host "Saved metadata to $metaPath" -ForegroundColor Green
Write-Host "DONE. Total images: $($metadata.Count)" -ForegroundColor Yellow
