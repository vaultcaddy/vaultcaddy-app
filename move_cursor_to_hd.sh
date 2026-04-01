#!/bin/bash

# 請將下面的路徑替換成你實際的外接硬碟路徑
# 例如：HD_PATH="/Volumes/1hd"
HD_PATH="/Volumes/你的外接硬碟名稱"

if [ ! -d "$HD_PATH" ]; then
    echo "錯誤：找不到外接硬碟 $HD_PATH，請確認硬碟已連接並修改腳本中的路徑。"
    exit 1
fi

echo "開始將 Cursor 資料轉移到 $HD_PATH..."

# 1. 建立外接硬碟上的目標資料夾
mkdir -p "$HD_PATH/CursorData"

# 2. 轉移 ~/.cursor
if [ -d "$HOME/.cursor" ] && [ ! -L "$HOME/.cursor" ]; then
    echo "正在移動 ~/.cursor..."
    mv "$HOME/.cursor" "$HD_PATH/CursorData/.cursor"
    ln -s "$HD_PATH/CursorData/.cursor" "$HOME/.cursor"
    echo "~/.cursor 轉移完成！"
else
    echo "~/.cursor 已經是軟連結或不存在，跳過。"
fi

# 3. 轉移 ~/Library/Application Support/Cursor
if [ -d "$HOME/Library/Application Support/Cursor" ] && [ ! -L "$HOME/Library/Application Support/Cursor" ]; then
    echo "正在移動 Application Support/Cursor..."
    mv "$HOME/Library/Application Support/Cursor" "$HD_PATH/CursorData/Cursor"
    ln -s "$HD_PATH/CursorData/Cursor" "$HOME/Library/Application Support/Cursor"
    echo "Application Support/Cursor 轉移完成！"
else
    echo "Application Support/Cursor 已經是軟連結或不存在，跳過。"
fi

echo "所有操作完成！你可以重新打開 Cursor 了。"
