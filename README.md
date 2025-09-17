# resumetry
template driven document generation

### prerequisites
```
brew install basictex
sudo tlmgr install enumitem
sudo tlmgr install preprint
sudo tlmgr install marvosym
```

### installation
```
brew tap ajilk/tools
```

## usage
```
python main.py \
  -c templates/sample/sample.yaml \
  [-t main] or [--template-path templates/main/main.tex] \
  -o templates/sample/sample.pdf
```
