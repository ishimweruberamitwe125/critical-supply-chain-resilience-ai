# Install git hooks that remove Cursor co-author lines from commits.
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$HooksDir = Join-Path $Root ".git\hooks"
$SourceDir = Join-Path $Root "scripts\git-hooks"

Copy-Item (Join-Path $SourceDir "prepare-commit-msg") (Join-Path $HooksDir "prepare-commit-msg") -Force
Copy-Item (Join-Path $SourceDir "commit-msg") (Join-Path $HooksDir "commit-msg") -Force

Write-Host "Installed git hooks: prepare-commit-msg, commit-msg"
Write-Host "Cursor Co-authored-by and Made-with lines will be stripped from commit messages."
