#!/usr/bin/env bash
# Upload an xlsx to Google Drive as a native Google Sheet in My Drive root (where Casey's other Aurit SEO sheets live).
# Usage: upload_to_drive.sh file.xlsx "Drive file name"   -> prints JSON {id,name,webViewLink}
set -euo pipefail
FILE="$1"; NAME="$2"
T=$(gcloud auth print-access-token)
META=$(python3 -c "import json,sys; print(json.dumps({'name': sys.argv[1], 'mimeType': 'application/vnd.google-apps.spreadsheet'}))" "$NAME")
curl -s -X POST "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart&supportsAllDrives=true&fields=id,name,webViewLink,parents" \
  -H "Authorization: Bearer $T" \
  -F "metadata=$META;type=application/json;charset=UTF-8" \
  -F "file=@$FILE;type=application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
