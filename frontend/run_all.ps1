$frontends = @(
    @{ name = "slp"; path = "H:\frontend\slp"; port = 5173 },
    @{ name = "plm"; path = "H:\frontend\plm"; port = 5174 },
    @{ name = "slp9"; path = "H:\frontend\slp9"; port = 5175 }
    @{ name = "krt"; path = "H:\frontend\krt"; port = 5176 },
    @{ name = "krt3"; path = "H:\frontend\krt3"; port = 5177 },
    @{ name = "sm1"; path = "H:\frontend\sm1"; port = 5178 },
    @{ name = "sm13"; path = "H:\frontend\sm13"; port = 5179 },
    @{ name = "mry"; path = "H:\frontend\mry"; port = 5180 },
    @{ name = "kdy"; path = "H:\frontend\kdy"; port = 5181 },
    @{ name = "ckg"; path = "H:\frontend\ckg"; port = 5182 },
    @{ name = "tga"; path = "H:\frontend\tga"; port = 5183 },
    @{ name = "kpk"; path = "H:\frontend\kpk"; port = 5184 },
    @{ name = "ksb"; path = "H:\frontend\ksb"; port = 5185 },
    @{ name = "jia"; path = "H:\frontend\jia"; port = 5186 }
)

foreach ($fe in $frontends) {
    Write-Host "Menjalankan frontend $($fe.name) di port $($fe.port)..."
    Start-Process powershell -ArgumentList "cd `"$($fe.path)`"; npm run dev -- --host --port=$($fe.port)"
}