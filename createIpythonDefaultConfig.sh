#!/bin/bash

# Aaron Holt
# A script for Jupyter 2 that copies default ipython parallel configuration files and directories
# to a default location.

ipythonDir="/home/$USER/.ipython.rc"
configDir="/curc/tools/x86_64/rh6/software/python_packages/3.4.3/intel/15.0.2/jupyterhub/0.2.0/Ipython"

#check if dir exists
if [ -d $ipythonDir ]; then
    #check for symlink/file
    if [ -L $ipythonDir ]; then
        echo "Error, symlink at ipythonDir"
    elif [ -f $ipythonDir ]; then
        echo "Error, file at ipythonDir"
    else
        echo "Directory already exists"
    fi
else
    #directory doesn't exist, create it, copy config
    if mkdir $ipythonDir; then
        echo "Directory successfully created"
        #Copy ipython config files
        if cp -rn $configDir/* $ipythonDir/; then
            echo "Files successfully copied"
        else 
            echo "File copy failed" 
        fi
    else 
        echo "Directory creation failed" 
    fi
fi