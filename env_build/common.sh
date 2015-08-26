#!/bin/bash

sanity_check()
{
    if [ $EUID -ne 0 ]; then
        echo "You must be root."
        exit 1
    fi

    if [ ! -d $(dirname $BASH_SOURCE)/../src ]; then
        echo "you need to check out the whole branch to make this script work properly"
        #exit 1
    fi
}

install_python_module()
{
    pushd $PWD

    cd $(dirname $BASH_SOURCE)/tools
    tar zxf "$1.tar.gz" -C /tmp
    cd "/tmp/$1"
    /opt/bin/python setup.py install $2

    popd
}

install_python_module_lib()
{
    pushd $PWD

    cd $(dirname $BASH_SOURCE)/tools
    tar zxf "$1.tar.gz" -C /tmp
    cd "/tmp/$1"
    /opt/bin/python setup.py install_lib

    popd
}

setup_python()
{
    pushd $PWD

    cd $(dirname $BASH_SOURCE)/tools
    tar jxf Python-2.6.5.tar.bz2 -C /tmp
    cp -f Python_Modules_Setup /tmp/Python-2.6.5/Modules/Setup
    cd /tmp/Python-2.6.5
    ./configure --prefix=/opt
    make
    make install
    sed -i 's/^never\(.*\)]$/never\1, "_warnings"]/' Tools/freeze/makeconfig.py
    cp -r Tools/freeze /opt/bin/

    popd

    declare workspace=$(cd $(dirname $BASH_SOURCE)/..; pwd -P)
    echo ${workspace}/src > /opt/lib/python2.6/site-packages/tvie.pth
    echo ${workspace}/src/tviebackend/3rdparty >> /opt/lib/python2.6/site-packages/tvie.pth

    install_python_module setuptools-0.6c11 
    install_python_module cx_Freeze-4.2.3
    install_python_module MySQL-python-1.2.3 "--single-version-externally-managed --root=/"
    install_python_module libxml2-python-2.6.21
    install_python_module python2-chardet-2.0.1
    /opt/bin/easy_install sphinx
}

setup_python_2_7()
{
    pushd $PWD

    cd $(dirname $BASH_SOURCE)/tools
    tar jxf Python-2.7.3.tar.bz2 -C /tmp
    # comment ssl modules
    #cp -f Python_Modules_Setup_4_Centos_6_2 /tmp/Python-2.7.3/Modules/Setup
    cd /tmp/Python-2.7.3
    ./configure --prefix=/opt
    # comment test_datetime_capi
    #sed -i "1692s/^/\/\//;1279,1297s/^/\/\//" Modules/_testcapimodule.c 
    make -j8
    make install
    sed -i 's/^never\(.*\)]$/never\1, "_warnings"]/' Tools/freeze/makeconfig.py
    cp -r Tools/freeze /opt/bin/

    popd

    declare workspace=$(cd $(dirname $BASH_SOURCE)/..; pwd -P)
    echo ${workspace}/src > /opt/lib/python2.7/site-packages/tvie.pth
    echo ${workspace}/src/tviebackend/3rdparty >> /opt/lib/python2.7/site-packages/tvie.pth

    install_python_module setuptools-0.6c11 
    install_python_module_lib MySQL-python-1.2.3
    install_python_module libxml2-python-2.6.21
    install_python_module python2-chardet-2.0.1
#    /opt/bin/easy_install sphinx
}

setup_flex_jscompiler_yasm()
{
    pushd $PWD

    cd $(dirname $BASH_SOURCE)/tools
    tar zxf adobe_flex_sdk.tar.gz -C /opt
    tar zxf closure_compiler.tar.gz -C /opt

    # x264
    tar zxf yasm-1.0.0.tar.gz -C /tmp
    pushd /tmp/yasm-1.0.0
    ./configure --prefix=/usr
    make
    make install
    popd

    popd
}

setup_flex_jscompiler_yasm_for_6_2()
{
    pushd $PWD

    cd $(dirname $BASH_SOURCE)/tools
    tar zxf adobe_flex_sdk.tar.gz -C /opt
    tar zxf closure_compiler.tar.gz -C /opt

    tar zxf yasm-1.2.0.tar.gz -C /tmp
    pushd /tmp/yasm-1.2.0
    ./configure --prefix=/usr
    make -j8
    make install
    popd

    popd
}

install_from_src() #1, 2, 3, 3 is optional
{
    package_decomp_name=$1
    package_name=$2
    config=$3
    pushd $PWD

    tar -xf tools/${package_name} -C /tmp
    cd /tmp/${package_decomp_name} 
    ./configure ${config}; make install

    popd
}

ubuntu_apt_update()
{
    apt_file="/etc/apt/sources.list"
    cp $apt_file "${apt_file}.copy"
    pushd $PWD
    
    cd $(dirname $BASH_SOURCE)/tools
    cp sources.list $apt_file
    apt-get update

}
