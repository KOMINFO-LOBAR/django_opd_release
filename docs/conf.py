import os,sys
sys.path.insert(0,os.path.abspath('..'))
project='WEBSITE OPD'
copyright='2024, APTIKA - DISKOMINFO LOBAR'
author='APTIKA - DISKOMINFO LOBAR'
release='1.0'
extensions=['sphinx.ext.autodoc']
templates_path=['_templates']
exclude_patterns=['_build','Thumbs.db','.DS_Store']
language='id'
html_theme='sphinxawesome_theme'
html_static_path=['_static']
html_permalinks_icon='<span>#</span>'