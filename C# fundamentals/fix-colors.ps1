# Fix mermaid diagram colors across all C# fundamental files
$baseDir = 'c:\Users\Nguyen\github\ai-home-lab-docker-compose\C# fundamentals'
$files = @(
    'day04-linq-patterns.md',
    'day05-generics.md', 
    'day06-exceptions.md',
    'day07-collections.md',
    'day08-async-await.md',
    'day09-multithreading.md',
    'day10-reflection-attributes.md',
    'day11-modern-csharp.md',
    'day12-design-patterns.md',
    'day13-performance.md',
    'day14-interview-prep.md'
)

foreach ($file in $files) {
    $path = Join-Path $baseDir $file
    if (Test-Path $path) {
        Write-Host "Processing $file..."
        $content = Get-Content $path -Raw -Encoding UTF8
        
        # Replace bright colors with softer colors
        $content = $content -replace 'fill:#90EE90', 'fill:#c8e6c9,stroke:#333,stroke-width:2px'
        $content = $content -replace 'fill:#87CEEB', 'fill:#bbdefb,stroke:#333,stroke-width:2px'
        $content = $content -replace 'fill:#FFB6C1', 'fill:#ffccbc,stroke:#333,stroke-width:2px'
        $content = $content -replace 'fill:#FF6347', 'fill:#ef9a9a,stroke:#333,stroke-width:2px'
        $content = $content -replace 'fill:#FFD700', 'fill:#fff9c4,stroke:#333,stroke-width:2px'
        $content = $content -replace 'fill:#DDA0DD', 'fill:#e1bee7,stroke:#333,stroke-width:2px'
        
        # Simplify complex characters for GitHub rendering
        $content = $content -replace '&lt;', ''
        $content = $content -replace '&gt;', ''
        
        Set-Content $path $content -NoNewline -Encoding UTF8
        Write-Host "  Fixed $file"
    } else {
        Write-Host "  File not found: $path"
    }
}

Write-Host "`nDone! All files processed."
