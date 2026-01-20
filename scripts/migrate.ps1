param(
    [string]$Message = "update"
)

$ErrorActionPreference = "Stop"

Write-Host "Creating migration: $Message"
alembic revision --autogenerate -m $Message

Write-Host "Applying migrations"
alembic upgrade head
