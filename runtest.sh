
# 目前只适用于Mac本地环境的测试
# 构建最新的css、js文件
python3 tools/build.py

rm -rf testdata
python3 tools/run-test.py

# echo -e '\n\nrun test in python-2.7'
# python2 -m pytest tests --doctest-modules --cov handlers --cov xutils --cov core

# echo 'run test in python-3.4'
# /usr/local/bin/python3.4 -m pytest tests --doctest-modules --cov handlers --cov xutils --cov core

echo -e '\n\nrun test in python-3.7'
python3 tools/run-test.py

echo -e '\n\nrun test in python-3.8'
source py3.8/bin/activate
pip3 install -r config/requirements.txt
pip3 install -r config/requirements.test.txt
python3 tools/run-test.py
deactivate

# clean test dir
rm -rf testdata

# 生成html结果
python3 -m coverage html