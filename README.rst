=========
Slurm TUI
=========


.. image:: https://img.shields.io/pypi/v/slurm_tui.svg
        :target: https://pypi.python.org/pypi/slurm_tui

Slurm Text User Interface using the Slurm REST API in Python.


* Free software: MIT license
* Documentation: https://github.com/bihealth/slurm-tui

-------------
Usage Example
-------------

::

    # slurm-tui --server=http://hpc-slurmrestd scancel
    [I 220401 14:43:28] args = {
        "verbose": false,
        "force_jwt_token": false,
        "api_version": "v0.0.37",
        "server": "http://hpc-slurmrestd",
        "command": "scancel"
        }
    [I 220401 14:43:30] Which job to kill? Enter to select, Ctrl-C to cancel
      1317509 -- bash
      1317802 -- bash
      1320066 -- bash
      1320250 -- bash
      1320256 -- snakejob.ngs_mapping_bwa_run.86.sh
      1370797 -- foo
    > 1370958 -- foo [Enter]
    [I 220401 14:43:32] Deleted job 1370958
    [I 220401 14:43:32] All done, have a nice day!
