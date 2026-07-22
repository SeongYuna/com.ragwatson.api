#!/usr/bin/env bash
set -euo pipefail
openssl genrsa -out jwt_private.pem 2048
openssl rsa -in jwt_private.pem -pubout -out jwt_public.pem
echo "jwt_private.pem → .env.auth 의 JWT_PRIVATE_KEY 로"
echo "jwt_public.pem  → .env.backend 의 JWT_PUBLIC_KEY 로"
echo
echo "base64 인코딩(멀티라인 env 주입용):"
echo "  JWT_PRIVATE_KEY: $(base64 -w0 jwt_private.pem 2>/dev/null || base64 jwt_private.pem)"
echo "  JWT_PUBLIC_KEY:  $(base64 -w0 jwt_public.pem 2>/dev/null || base64 jwt_public.pem)"
