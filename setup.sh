#!/bin/bash
# github author@sudoskys
# project:TelechaBot
initVar() {
  echoType='echo -e'
}
initVar
echox() {
  case $1 in
  # 红色
  "red")
    # shellcheck disable=SC2154
    ${echoType} "\033[31m$2\033[0m"
    ;;
    # 绿色
  "green")
    ${echoType} "\033[32m$2\033[0m"
    ;;
    # 黄色
  "yellow")
    ${echoType} "\033[33m$2\033[0m"
    ;;
    # 蓝色
  "blue")
    ${echoType} "\033[34m$2\033[0m"
    ;;
    # 紫色
  "purple")
    ${echoType} "\033[35m$2\033[0m"
    ;;
    # 天蓝色
  "skyBlue")
    ${echoType} "\033[36m$2\033[0m"
    ;;
    # 白色
  "white")
    ${echoType} "\033[37m$2\033[0m"
    ;;
  esac
}
Gitpull() {
  git clone https://github.com/TelechaBot/TelechaBot.git || (
    echox yellow "Git failed,try pull from mirror"
    git clone https://gitclone.com/github.com/TelechaBot/TelechaBot.git
  )
}

dependenceInit() {
  cd TelechaBot || (
    echo "Cant find !?"
    exit 1
  )
  pip3 install --upgrade pip
  pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
  # while read -r requirement; do pip3 install "${requirement}" -i https://pypi.tuna.tsinghua.edu.cn/simple; done <requirements.txt || echox yellow "===pip install failed,please check it====="
  echox yellow "========Down=========="
}
dataBack="$(pwd)/tmp"
dir="$(pwd)/TelechaBot"
data="$(pwd)/TelechaBot/Data"
config="$(pwd)/TelechaBot/Config"
echo "=============Setup============"

run() {
  #  if [ -f "${dir}/project.info" ]; then
  #    Data=$(cat "${dir}/project.info")
  #    declare "$Data"
  #    # shellcheck disable=SC2154
  #    echox green "当前版本 ${version}"
  #    now=$version
  #    (curl -s https://raw.fastgit.org/sudoskys/TelechaBot/main/project.info) && declare<(curl -s https://raw.fastgit.org/sudoskys/TelechaBot/main/project.info)
  #    new=$version
  #    if [[ $new ]]; then
  #       if [[ $((new)) -gt $((now)) ]]; then
  #          echox yellow "仓库最新版本为${new}"
  #       fi
  #    else
  #       echox red "远程仓库出现错误或未连接"
  #    fi
  #  fi
  if [ ! -d "$dir" ]; then
    echox skyBlue "初始化:No found ${dir}，init, setup..."
    Gitpull
    dependenceInit
  else
    # 初始化备份文件夹
    if [ ! -d "$dataBack" ]; then
      echox skyBlue "初始化备份文件夹：init ${dataBack}...."
      mkdir "$dataBack"
    fi


    # 备份配置文件
    if [ -f "${dir}/Captcha.toml" ]; then
      echox skyBlue "移动配置文件：backup ${dir}/Captcha.toml to ${dataBack} ...."
      cp -f "${dir}/Captcha.toml" "$config"
    fi
    # 备份配置文件
    if [ -f "${dir}/config.json" ]; then
      echox skyBlue "移动配置文件：backup ${dir}/config.json to ${dataBack} ...."
      cp -f "${dir}/config.json" "$config"


    # 备份配置文件
    if [ -f "${dir}/taskRedis.json" ]; then
      echox skyBlue "移动配置文件：backup ${dir}/taskRedis.json to ${dataBack} ...."
      cp -f "${dir}/taskRedis.json" "$dataBack"
    fi
    fi
    # 备份运行数据
    if [ -d "$data" ]; then
      echox skyBlue "备份运行数据：Copy run data to ${dataBack}...."
      cp -rf "$data" "$dataBack" #文件夹目录 文件夹上级
    fi
    # 备份配置数据
    if [ -d "$config" ]; then
      echox skyBlue "备份运行数据：Copy Config to ${dataBack}...."
      cp -rf "$config" "$dataBack" #文件夹目录 文件夹上级
    fi
    read -r -p "请问，是否使用可能存在的备份配置？Do you want to update your app with probably exist old data？${dir} y/n?[default=y]" input
    if [ -z "${input}" ]; then
      input=y
    fi
    case $input in
    [nN][oO] | [nN])
      echox red "We will reinstall a pure app...."
      rm -rf "${dir}"
      Gitpull
      dependenceInit
      ;;
    [yY][eE][sS] | [yY])
      rm -rf "${dir}"
      Gitpull
      # if [ -f "${dataBack}/Captcha.toml" ]; then
      #  echox green "恢复配置文件：Reuse the Captcha.toml from ${dataBack}...."
      #  cp -f "${dataBack}/Captcha.toml" "$dir" #文件夹目录 文件夹上级
      # fi
      if [ -f "${dataBack}/taskRedis.json" ]; then
      echox green "恢复配置文件：Reuse the taskRedis.json from ${dataBack}...."
      cp -f "${dataBack}/taskRedis.json" "$dir" #文件夹目录 文件夹上级
      fi
      if [ -d "${dataBack}/Config" ]; then
        echox green "恢复配置库：Reuse the Config from ${dataBack}...."
        cp -rf "${dataBack}/Config" "$dir" #文件夹目录 文件夹上级
      fi
      if [ -d "${dataBack}/Data" ]; then
        echox green "恢复数据库：Reuse the run data from ${dataBack}...."
        cp -rf "${dataBack}/Data" "$dir" #文件夹目录 文件夹上级
      fi
      dependenceInit || exit 1
      ;;
    *)
      echox skyBlue "Invalid input"
      ;;
    esac
  fi
}

run

cd "$(pwd)" && rm setup.sh
