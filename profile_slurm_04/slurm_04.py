import uuid
import math
from IPython.parallel.apps import launcher
from IPython.utils import traitlets
from IPython.utils.traitlets import (List, Unicode, CRegExp)

class SLURMLauncher(launcher.BatchSystemLauncher):
    """A BatchSystemLauncher subclass for SLURM
    """
    submit_command = List(['sbatch'], config=True,
                          help="The SLURM submit command ['sbatch']")
    # Send SIGKILL instead of term, otherwise the job is "CANCELLED", not
    # "FINISHED"
    delete_command = List(['scancel', '--signal=KILL'], config=True,
                          help="The SLURM delete command ['scancel']")
    job_id_regexp = CRegExp(r'\d+', config=True,
                            help="A regular expression used to get the job id from the output of 'sbatch'")

    batch_file = Unicode(u'', config=True,
                         help="The string that is the batch script template itself.")

    queue_regexp = CRegExp('#SBATCH\W+-p\W+\w')
    queue_template = Unicode('#SBATCH -p {queue}')

class SLURMEngineSetLauncher(SLURMLauncher, launcher.BatchClusterAppMixin):
    """Custom launcher handling heterogeneous clusters on SLURM
    Launches with 4 tasks per node
    """
    batch_file_name = Unicode("SLURM_engine" + str(uuid.uuid4()))
    mem = traitlets.Unicode("", config=True)
    timelimit = traitlets.Unicode("", config=True)
    resources = traitlets.Unicode("", config=True)
    default_template = traitlets.Unicode("""#!/bin/sh
#SBATCH --partition=janus
#SBATCH --output=/dev/null
#SBATCH -N {n}
#SBATCH --ntasks-per-node=4
#SBATCH --time=24:00:00
#SBATCH --export=ALL
#SBATCH --qos=janus

cd {profile_dir}
mpirun -n {n*4} ipengine --profile-dir={profile_dir}
""")

    def start(self, n):
        self.context["timelimit"] = self.timelimit
        self.context["resources"] = "\n".join(["#SBATCH --%s" % r.strip()
                                               for r in str(self.resources).split(";")
                                               if r.strip()])
        #math.ceil(n/4) requests the appropriate number of nodes for 4-tasks-per-node
        #Ex: 4 total tasks = 1 node. 5 total tasks = 2 nodes etc.
        return super(SLURMEngineSetLauncher, self).start(math.ceil(n/4))
