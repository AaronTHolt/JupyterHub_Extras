
ml slurm/slurm
ml intel/15.0.2
ml impi/5.0.3.048
ml python/3.4.3
ml ipyparallel/4.1.0
ml nodejs/4.2.4
ml jupyterhub/0.4.0
ml slurmspawner/master
ml mpi4py/1.3.1

export HOME=/home/$USER
IPYTHONDIR=/home/$USER/.ipython.rc
export IPYTHONDIR
configDir=$CURC_JUPYTERHUB_ROOT/Ipython
export configDir

#Copy default config files if necessary
$CURC_JUPYTERHUB_ROOT/Ipython/copyIpythonDefaultConfig.sh

export JPY_COOKIE_SECRET=/srv/jupyterhub/jupyterhub_cookie_secret
export CONFIGPROXY_AUTH_TOKEN=/curc/tools/x86_64/rh6/software/python_packages/3.4.3/intel/15.0.2/slurmspawner/all/etc/jupyter.rc.int.colorado.edu.crt
PATH=$PATH:$CURC_JUPYTERHUB_ROOT/Ipython
export PATH

