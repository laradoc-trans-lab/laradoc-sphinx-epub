#!/bin/bash

set -e

# 檢查是否有輸入版本參數
if [ -z "$1" ]; then
  echo "Please input first argument as version (e.g., 10.x, 11.x)."
  exit 1
fi
version=$1

# 檢查版本格式
if [[ "$version" =~ ^[0-9]+\.(x|[0-9]+)$ ]]; then
    echo "Building version: $version"
else
    echo "Invalid version format. Use format like '12.x' or '5.8'."
    exit 1
fi

# 檢查版本目錄是否存在
if [ ! -d "workspace/source/.git" ]; then
    echo "Version directory 'workspace/source' is not a git repo."
    exit 1
fi


# -- 清除舊的建置檔案
echo ">>> Cleaning previous builds..."
rm -Rf workspace/preprocess/$version
rm -Rf workspace/build/$version

# -- 建立 preprocess/$version 目錄與檔案
mkdir -p workspace/preprocess/$version/_static
mkdir -p workspace/preprocess/$version/docs
mkdir -p workspace/preprocess/$version/tocs
# 複製靜態檔案
# cp -f workspace/common/_static/* workspace/preprocess/$version/_static/




# -- 預處理原始文件至 workspace/preprocess 目錄
cd workspace/source
git checkout $version
cd ../..
echo ">>> Pre processing source files..."
python3 bin/preprocess_docs.py workspace/source workspace/preprocess/$version/docs

# -- 生成目錄
python3 bin/gen_index.py $version

cd workspace



# -- 轉換成 EPUB 格式

echo ">>> Building EPUB (color version) with Sphinx..."
SPHINX_BUILD_VERSION="$version,color" sphinx-build -E -a -b epub \
    --conf-dir . preprocess/$version build/$version/color

echo ">>> Building EPUB (grayscale version) with Sphinx..."
cp -f common/_static/custom-grayscale.css preprocess/$version/_static/
SPHINX_BUILD_VERSION="$version,grayscale" sphinx-build -E -a -b epub \
    --conf-dir . preprocess/$version build/$version/grayscale

echo ">>> Build complete! Check the 'workspace/build/$version' directory."
