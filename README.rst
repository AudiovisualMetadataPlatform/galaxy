# AMP galaxy

The AMP galaxy repository is forked from the [original Galaxy repository](https://github.com/galaxyproject/galaxy), with various AMP extensions and customizations.

The major changes to the original galaxy code base include but are not limited to:
- extensions to data types related various media formats, as well as workflow outputs in AMP specific JSON formats.
- extensions to JobRunner, mainly for the purpose of running LWLW (light-weight-long-waiting) jobs, such as Human MGMs and various clound-based MGMs.
- extension to workflow search criteria
- bug fixes

Note that some of the above changes are general enough that they have been or could be contributed back to the original Galaxy project; yet some are pretty AMP specific and might not be applicable to other applications using Galaxy.

AMP Galaxy can be run as a standalone application but its UI is advised to be only accessible to AMP Admin and not available to end users. Galaxy APIs are also wrapped by AMP backend and are hiden from external clients for security reasons. AMP Galaxy instance is a required dependency of AMP backend. Detailed information about this component in relationship to other AMP components is described in [AMP System Architecture](https://uisapp2.iu.edu/confluence-prd/display/AMP/System+Architecture?src=contextnavpagetreemode).

To install, config, run AMP Galaxy, as well as contribute to the AMP project, please refer to the instructions on [AMP Bootstrap](https://github.com/AudiovisualMetadataPlatform/amp_bootstrap)
