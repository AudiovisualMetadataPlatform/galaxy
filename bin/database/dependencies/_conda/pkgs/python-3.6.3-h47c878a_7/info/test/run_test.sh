

set -ex



python -V
python3 -V
2to3 -h
pydoc -h
python3-config --help
python -c "import sysconfig; print(sysconfig.get_config_var('CC'))"
conda inspect linkages -p $PREFIX python
conda inspect objects -p $PREFIX python
exit 0
