default: build

@release:
  echo 'tagged'
  echo 'pushed'
  echo 'updated sha'

@build:
   uv run resumetry --config src/resumetry/templates/main/main.yaml --template main

