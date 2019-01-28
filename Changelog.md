## %"FusionDirectory 1.3" - 2019-01-28

### Added

#### fusiondirectory
- fusiondirectory#5676 New file include/class_Language.inc
- fusiondirectory#5686 Package supann-ext
- fusiondirectory#5698 Package supann-ext
- fusiondirectory#5699 package the sinaps plugin for 1.3
- fusiondirectory#5700 Update audit plugin for selecting range of date
- fusiondirectory#5703 to use the backport of LDAP size limit refactor from 1.4 we need to add the include/class_ldapSizeLimit.inc

### Changed

#### fusiondirectory
- fusiondirectory#5665 Plugins folder should be reorganized to ease packaging
- fusiondirectory#5670 Install the new files for OPSI dashboard in RPM build
- fusiondirectory#5677 New file in sudo plugin
- fusiondirectory#5687 select to install vith scl 7.x a version for centos 6 and 7
- fusiondirectory#5697 Renaming of supann sources
- fusiondirectory#5702 Make FD work with official php-Smarty
- fusiondirectory#5704 Update fusiondirectory-plugins spec file so that it match fusiondirectory.spec
- fusiondirectory#5705 It looks like directory does not work on /fusiondirectory in fusiondirectory-apache.conf
- fusiondirectory#5706 Force php-Smarty to 3.1.32 from remi's repo

### Removed

#### fusiondirectory
- fusiondirectory#5667 Remove files no longer in the developer plugin

## %"FusionDirectory 1.2.3" - 2018-11-18

### Added

#### fusiondirectory
- fusiondirectory#5694 Add the pdf with the oid of fusiondirectory in the contrib dir of the core


## %"FusionDirectory 1.2.2" - 2018-09-01

### Changed

#### fusiondirectory
- fusiondirectory#5690 AUTHORS as been Remamed AUTHORS.md
- fusiondirectory#5692 Change the partage icon to be the new one

### Security

#### fusiondirectory
- fusiondirectory#5691 The file include/class_CSRFProtection.inc needs to be packaged


## %"FusionDirectory 1.2.1" - 2018-06-11

### Added

#### fusiondirectory
- fusiondirectory#5678 Add include/class_Combinations.inc

### Changed

#### fusiondirectory
- fusiondirectory#5666 Change file COPYING into LICENCE
- fusiondirectory#5672 Adapt packages to the removal of the contrib/docs directory
- fusiondirectory#5673 Adapt packages for stuff that are moved to dev-tools

### Fixed

#### fusiondirectory
- fusiondirectory#5671 Scriptaculous is used in plugins but not loaded into browser
- fusiondirectory#5675 Error when checking LDAP when we install FD

