default: build

@release:
  echo 'tagged'
  echo 'pushed'
  echo 'updated sha'

@build:
   uv run resumetry --config src/resumetry/templates/main/main.yaml --template main

@build-tp:
   uv run resumetry \
    --config src/resumetry/templates/main/main.yaml \
    --template-path src/resumetry/templates/main/main.tex \

@prod:
   resumetry --config src/resumetry/templates/main/main.yaml --template main

