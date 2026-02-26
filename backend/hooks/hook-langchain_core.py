from PyInstaller.utils.hooks import collect_submodules, collect_data_files

hiddenimports = collect_submodules("langchain_core")
datas = collect_data_files("langchain_core")
