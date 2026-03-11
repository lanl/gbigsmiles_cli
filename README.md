# GBIGSMILES_CLI

This project provides a CLI for interfacing with [Generative BigSMILES](https://doi.org/10.1039/D3DD00147D) and other polymer info formats.

# Installation

Install with pipx via
```bash
pipx install . 
```
or from PyPi via

```bash
pipx install gbigcli
```

Check that installation was successful by running 

```bash
gbigcli check
```

# Usage

The core CLI functionality of `gbigcli` is the ability to stochastically generate polymer examples from the command line. The syntax is

```bash
gbigsmiles get "<GenBigSMILES>" n_samples (optional) file_output (optional)
```

A number of helper library functions for interfacing with polymer inputs are also provided.

# Testing
Run 

```bash
pytest tests
```

# Copyright
This is GPLv3-LICENSED (see LICENSE.txt). This project has been approved for open-source release under O#: O5059. 
 © 2026. Triad National Security, LLC. All rights reserved.

This program was produced under U.S. Government contract 89233218CNA000001 for Los Alamos National Laboratory (LANL), which is operated by Triad National Security, LLC for the U.S. Department of Energy/National Nuclear Security Administration. All rights in the program are reserved by Triad National Security, LLC, and the U.S. Department of Energy/National Nuclear Security Administration. The Government is granted for itself and others acting on its behalf a nonexclusive, paid-up, irrevocable worldwide license in this material to reproduce, prepare. derivative works, distribute copies to the public, perform publicly and display publicly, and to permit others to do so.\