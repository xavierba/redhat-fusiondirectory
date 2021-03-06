# This is the header.spec file
Name:       fusiondirectory
Version:    _VERSION_
Release:    _RELEASE_
Summary:    Web Based LDAP Administration Program

Group:      Applications/System
License:    GPLv2
URL:        http://www.%{name}.org

Buildarch:  noarch
Source0:    %{name}-%{version}.tar.gz
Source1:    %{name}.te
Source2:    %{name}.fc

Patch0:     %{name}-fix_install-location-apache.patch
Patch1:     %{name}-fix_install-location.patch
Patch2:     %{name}-breezy-headers.patch
Patch3:     %{name}-fix_openldap-schema-location.patch
Patch4:     %{name}-fix_pear-location.patch
Patch5:     %{name}-fix_smarty3-location.patch
Patch6:     %{name}-fix_install-location-apache-old-version.patch


Requires:   php >= 7, php-ldap >= 7, php-imap >= 7, php-mbstring >= 7, php-gd >= 7, php-pecl-imagick

Requires:   perl-Path-Class, perl-Digest-SHA, perl-File-Copy-Recursive, perl-Archive-Extract, perl-XML-Twig
Requires:   perl-Crypt-CBC, perl-LDAP, perl, perl-Crypt-Rijndael

Requires:   httpd, gettext, perl-ExtUtils-MakeMaker, prototype, prototype-httpd, scriptaculous, scriptaculous-httpd

Requires:   php-Smarty >= 3.1.32, php-Smarty3-gettext, php-pear-CAS

%description
FusionDirectory is a combination of system-administrator and end-user web
interface, designed to handle LDAP based setups.
Provided is access to posix, shadow, samba, proxy, fax, and Kerberos
accounts. It is able to manage the Postfix/Cyrus server combination
and can write user adapted sieve scripts.


# This is the package.spec file
%package schema
Group:      Applications/System
Summary:    Schema Definitions for the %{name} package
Requires:   openldap-clients, schema2ldif

%description schema
Contains the Schema definition files for the %{name} admin package.


############################
# SELINUX PACKAGE
############################

%package selinux
Group:      Applications/System
Summary:    SELinux policy for Fusiondirectory
Requires:   selinux-policy >= %{selinux_policyver}
Requires:   %{name} = %{version}-%{release}
BuildRequires:    checkpolicy, selinux-policy-devel, /usr/share/selinux/devel/policyhelp

%description selinux
This package contains the binary modules and sources files of the
SEPolicy needed for Fusiondirectory.

############################

%global webconfdir        %{_sysconfdir}/httpd/conf.d/
%global docdir            %{_datadir}/doc/
%global selinux_policyver %(%{__sed} -e 's,.*selinux-policy-\\([^/]*\\)/.*,\\1,' /usr/share/selinux/devel/policyhelp || echo 0.0.0)

# SELinux policy variants
%global selinux_variants mls strict targeted

############################

# This is the prep.spec file
%prep

# Create build directory
%setup -c -q -n %{name}-%{version}

# Source FD-core
# Extract Source
%setup -T -D -b 0

# Apply all the patches
%if %{?rhel} >= 7
%patch0 -p1
%else
%patch6 -p1
%endif

%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

############################
# SELINUX PREP
############################

# SELinux build environment setup
mkdir SELinux
cp -p %{SOURCE1} %{SOURCE2} SELinux

# Change version of fusiondirectory.te
sed -i 's/_SELINUX-VERSION_/%{version}/g' SELinux/%{name}.te

############################
# SELINUX BUILD
############################

%build
# Build SELinux binary policy module
cd SELinux
for selinuxvariant in %{selinux_variants}
do
  make NAME=${selinuxvariant} -f /usr/share/selinux/devel/Makefile
  mv %{name}.pp %{name}.pp.${selinuxvariant}
  make NAME=${selinuxvariant} -f /usr/share/selinux/devel/Makefile clean
done
cd -

############################

# This is the install.spec file
%install
rm -Rf %{buildroot}

# Installation of FD-core
# Create /usr/share/fusiondirectory/
mkdir -p %{buildroot}%{_datadir}/%{name}

DIRS="ihtml plugins html include locale setup"
for i in $DIRS ; do
  cp -ua $i %{buildroot}%{_datadir}/%{name}
done

# Create spool and cache directories
install -d -m 0770 %{buildroot}/var/spool/%{name}/
install -d -m 0770 %{buildroot}/var/cache/%{name}/{tmp,fai}/

# Create other directories
mkdir -p %{buildroot}%{_datadir}/man/man1/
mkdir -p %{buildroot}%{_datadir}/man/man5/
mkdir -p %{buildroot}%{_sysconfdir}/%{name}/
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_sysconfdir}/openldap/schema/%{name}/
mkdir -p %{buildroot}%{_datadir}/php/Smarty/plugins/
mkdir -p %{buildroot}%{_datadir}/fusiondirectory/html/javascript/

# Set the rights
chmod 750 contrib/bin/*

# Prepare the man pages
gzip contrib/man/%{name}.conf.5
gzip contrib/man/%{name}-setup.1
gzip contrib/man/%{name}-insert-schema.1

# Move man files
cp contrib/man/%{name}-setup.1.gz %{buildroot}%{_datadir}/man/man1
cp contrib/man/%{name}-insert-schema.1.gz %{buildroot}%{_datadir}/man/man1
cp contrib/man/%{name}.conf.5.gz %{buildroot}%{_datadir}/man/man5

# Copy docs
mkdir -p %{buildroot}%{_datadir}/doc/{%{name},%{name}-schema}
mkdir -p %{buildroot}%{_datadir}/doc/%{name}/examples/
cp ./AUTHORS.md ./Changelog ./LICENSE %{buildroot}%{_datadir}/doc/%{name}/
cp ./AUTHORS.md ./Changelog ./LICENSE %{buildroot}%{_datadir}/doc/%{name}-schema/
cp contrib/%{name}.conf %{buildroot}%{_datadir}/doc/%{name}/
cp -a contrib/docs/ %{buildroot}%{_datadir}/doc/%{name}/
cp -a contrib/images/ %{buildroot}%{_datadir}/doc/%{name}/
cp -a contrib/apache/* %{buildroot}%{_datadir}/doc/%{name}/examples/
cp -a contrib/lighttpd/* %{buildroot}%{_datadir}/doc/%{name}/examples/

# Move smarty functions and create php lib directory if it exist
cp contrib/smarty/plugins/function.msgPool.php %{buildroot}%{_datadir}/php/Smarty/plugins/function.msgPool.php
cp contrib/smarty/plugins/function.filePath.php %{buildroot}%{_datadir}/php/Smarty/plugins/function.filePath.php
cp contrib/smarty/plugins/block.render.php %{buildroot}%{_datadir}/php/Smarty/plugins/block.render.php

# Move the schemas
cp -a contrib/openldap/* %{buildroot}%{_sysconfdir}/openldap/schema/%{name}/
mkdir -p %{buildroot}%{_datadir}/doc/%{name}/

# Move executables
cp contrib/bin/* %{buildroot}%{_sbindir}

# Move apache configuration
cp contrib/apache/%{name}-apache.conf %{buildroot}%{_sysconfdir}/%{name}/

############################
# SELINUX INSTALL
############################

# Install SELinux Policy Module
for selinuxvariant in %{selinux_variants}
do
  install -d %{buildroot}%{_datadir}/selinux/${selinuxvariant}
  install -p -m 644 SELinux/%{name}.pp.${selinuxvariant} \
    %{buildroot}%{_datadir}/selinux/${selinuxvariant}/%{name}.pp
done

############################


%clean
rm -Rf %{buildroot}


############################
# POST / POSTUN SELINUX
############################

%post selinux
# SELinux post and postun scriptlets
for selinuxvariant in %{selinux_variants}
do
  /usr/sbin/semodule -s ${selinuxvariant} -i \
    %{_datadir}/selinux/${selinuxvariant}/%{name}.pp &> /dev/null || :
done

# Apply context for spool and cache directroy considering the fusiondirectory policy
/sbin/restorecon -R /var/spool/%{name}
/sbin/restorecon -R /var/cache/%{name}

%postun selinux
if [ $1 = 0 ] ; then
  for selinuxvariant in %{selinux_variants}
  do
    /usr/sbin/semodule -s ${selinuxvariant} -r %{name} &> /dev/null || :
  done

  # Apply context for spool and cache directroy without the fusiondirectory policy
  /sbin/restorecon -R /var/spool/%{name}
  /sbin/restorecon -R /var/cache/%{name}
fi

%postun
if [ $1 = 0 ] ; then
  if [ -d /etc/httpd/conf.d ]; then
    # Remove FusionDirectory include
    [ -L /etc/httpd/conf.d/fusiondirectory.conf ] && rm -f /etc/httpd/conf.d/fusiondirectory.conf

    # Restart servers
    if [ -x /usr/sbin/httpd ]; then
      service httpd restart
    fi
  fi

  if [ -d /var/cache/fusiondirectory ]; then
    # Remove cache directory
    rm -Rf /var/cache/fusiondirectory

    # Remove spool directory
    rm -Rf /var/spool/fusiondirectory
  fi

  # Delete javascript libraries symlinks
  [ -L /usr/share/fusiondirectory/html/javascript/prototype ] && rm -f /usr/share/fusiondirectory/html/javascript/prototype
  [ -L /usr/share/fusiondirectory/html/javascript/scriptaculous ] && rm -f /usr/share/fusiondirectory/html/javascript/scriptaculous
fi

%post
# Remove cache and spool
rm -Rf /var/cache/fusiondirectory/
rm -Rf /var/spool/fusiondirectory/

# Create all cache and directories we need after install
%{_sbindir}/%{name}-setup -y --check-directories --update-cache --update-locales

if [ -d /etc/httpd/conf.d ]; then

  # Copy FusionDirectory configuration to conf.d directories
  if [ ! -L /etc/httpd/conf.d/fusiondirectory.conf ]; then

    # Remove old instances of this file
    if [ -f /etc/httpd/conf.d/fusiondirectory.conf ]; then
      echo "Found old fusiondirectory apache configuration in /etc/httpd/conf.d - moving it to fusiondirectory.conf.orig..."
      echo "Please check for changes in /etc/fusiondirectory/fusiondirectory-apache.conf if you modified this file!"
      mv /etc/httpd/conf.d/fusiondirectory.conf /etc/httpd/conf.d/fusiondirectory.conf.orig
    fi

    echo "Making /fusiondirectory available in /etc/httpd/conf.d"

    # Add FusionDirectory include file
    ln -s /etc/fusiondirectory/fusiondirectory-apache.conf /etc/httpd/conf.d/fusiondirectory.conf
  fi

  service httpd reload
fi

# Link fusiondirectory.conf to cache/template directory
ln -s /usr/share/doc/fusiondirectory/fusiondirectory.conf  /var/cache/fusiondirectory/template/fusiondirectory.conf

# Link javascript profotype if not exist
if ! [[ -d /usr/share/fusiondirectory/html/javascript/prototype ]] ; then
  ln -s /usr/share/prototype /usr/share/fusiondirectory/html/javascript/prototype
fi

# Link javascript scriptaculous if not exist
if ! [[ -d /usr/share/fusiondirectory/html/javascript/scriptaculous ]] ; then
  ln -s /usr/share/scriptaculous /usr/share/fusiondirectory/html/javascript/scriptaculous
fi

%files
%defattr(-,root,root,-)
%{_mandir}/man1/%{name}-setup.1.gz
%{_mandir}/man5/%{name}.conf.5.gz

%{_sbindir}/%{name}-setup
%{_datadir}/%{name}/html/images
%{_datadir}/%{name}/html/plugins
%{_datadir}/%{name}/html/themes
%{_datadir}/%{name}/html/*.php
%{_datadir}/%{name}/html/*.inc
%{_datadir}/%{name}/html/*.ico
%{_datadir}/%{name}/html/*.txt
%{_datadir}/%{name}/html/include/datepicker.js
%{_datadir}/%{name}/html/include/%{name}.js
%{_datadir}/%{name}/html/include/pulldown.js
%{_datadir}/%{name}/html/include/pwdStrength.js
%{_datadir}/%{name}/html/include/tsorter.js
%{_datadir}/%{name}/html/javascript/
%{_datadir}/%{name}/ihtml
%{_datadir}/%{name}/include/exporter
%{_datadir}/%{name}/include/password-methods
%{_datadir}/%{name}/include/simpleplugin
%{_datadir}/%{name}/include/select
%{_datadir}/%{name}/include/accept-to-gettext.inc
%{_datadir}/%{name}/include/class_acl.inc
%{_datadir}/%{name}/include/class_baseSelector.inc
%{_datadir}/%{name}/include/class_config.inc
%{_datadir}/%{name}/include/class_CopyPasteHandler.inc
%{_datadir}/%{name}/include/class_departmentSortIterator.inc
%{_datadir}/%{name}/include/class_divSelectBox.inc
%{_datadir}/%{name}/include/class_filter.inc
%{_datadir}/%{name}/include/class_filterLDAP.inc
%{_datadir}/%{name}/include/class_IconTheme.inc
%{_datadir}/%{name}/include/class_ldap.inc
%{_datadir}/%{name}/include/class_ldapFilter.inc
%{_datadir}/%{name}/include/class_ldapMultiplexer.inc
%{_datadir}/%{name}/include/class_listing.inc
%{_datadir}/%{name}/include/class_listingSortIterator.inc
%{_datadir}/%{name}/include/class_logging.inc
%{_datadir}/%{name}/include/class_msg_dialog.inc
%{_datadir}/%{name}/include/class_msgPool.inc
%{_datadir}/%{name}/include/class_objects.inc
%{_datadir}/%{name}/include/class_pluglist.inc
%{_datadir}/%{name}/include/class_session.inc
%{_datadir}/%{name}/include/class_SnapshotHandler.inc
%{_datadir}/%{name}/include/class_tests.inc
%{_datadir}/%{name}/include/class_timezone.inc
%{_datadir}/%{name}/include/class_userinfo.inc
%{_datadir}/%{name}/include/class_xml.inc
%{_datadir}/%{name}/include/class_ldapGeneralizedTime.inc
%{_datadir}/%{name}/include/functions_debug.inc
%{_datadir}/%{name}/include/functions.inc
%{_datadir}/%{name}/include/php_setup.inc
%{_datadir}/%{name}/include/variables_common.inc
%{_datadir}/%{name}/include/variables.inc
%{_datadir}/%{name}/include/class_template.inc
%{_datadir}/%{name}/include/class_SnapshotDialogs.inc
%{_datadir}/%{name}/include/class_exceptions.inc
%{_datadir}/%{name}/include/class_templateHandling.inc
%{_datadir}/%{name}/include/class_Combinations.inc
%{_datadir}/%{name}/include/class_Language.inc
%{_datadir}/%{name}/include/class_CSRFProtection.inc
%{_datadir}/%{name}/include/class_ldapSizeLimit.inc
%{_datadir}/%{name}/locale
%{_datadir}/%{name}/plugins
%{_datadir}/%{name}/setup
%config %{_sysconfdir}/%{name}/%{name}-apache.conf
%{_datadir}/doc/%{name}/
%{_datadir}/php/Smarty/plugins/block.render.php
%{_datadir}/php/Smarty/plugins/function.msgPool.php
%{_datadir}/php/Smarty/plugins/function.filePath.php

%files schema
%defattr(-,root,root,-)
%{_mandir}/man1/%{name}-insert-schema.1.gz

%{_datadir}/doc/%{name}-schema/AUTHORS.md
%{_datadir}/doc/%{name}-schema/LICENSE
%{_datadir}/doc/%{name}-schema/Changelog

%{_sysconfdir}/openldap/schema/%{name}/core-fd.schema
%{_sysconfdir}/openldap/schema/%{name}/ldapns.schema
%{_sysconfdir}/openldap/schema/%{name}/core-fd-conf.schema
%{_sysconfdir}/openldap/schema/%{name}/rfc2307bis.schema
%{_sysconfdir}/openldap/schema/fusiondirectory/template-fd.schema
%{_sbindir}/%{name}-insert-schema


############################
# FILES SELINUX
############################

%files selinux
%defattr(-,root,root,0755)
%doc SELinux/%{name}.te
%doc SELinux/%{name}.fc
%{_datadir}/selinux/*/%{name}.pp

%changelog
* Mon Jan 28 2019 Jonathan SWAELENS <jonathan@opensides.be> - 1.3-1
- [Added] fusiondirectory#5676 New file include/class_Language.inc
- [Added] fusiondirectory#5703 to use the backport of LDAP size limit refactor from 1.4 we need to add the include/class_ldapSizeLimit.inc
- [Changed] fusiondirectory#5687 select to install vith scl 7.x a version for centos 6 and 7
- [Changed] fusiondirectory#5702 Make FD work with official php-Smarty
- [Changed] fusiondirectory#5705 It looks like directory does not work on /fusiondirectory in fusiondirectory-apache.conf
- [Changed] fusiondirectory#5706 Force php-Smarty to 3.1.32 from remi's repo

* Sun Nov 18 2018 Jonathan SWAELENS <jonathan@opensides.be> - 1.2.3-1
- [Added] fusiondirectory#5694 Add the pdf with the oid of fusiondirectory in the contrib dir of the core

* Sat Sep 01 2018 Jonathan SWAELENS <jonathan@opensides.be> - 1.2.2-1
- [Changed] fusiondirectory#5690 AUTHORS as been Renamed AUTHORS.md
- [Security] fusiondirectory#5691 The file include/class_CSRFProtection.inc needs to be packaged

* Mon Jun 11 2018 Jonathan SWAELENS <jonathan@opensides.be> - 1.2.1-1
- [Added] fusiondirectory#5678 Add include/class_Combinations.inc
- [Changed] fusiondirectory#5666 Change file COPYING into LICENCE
- [Changed] fusiondirectory#5672 Adapt packages to the removal of the contrib/docs directory
- [Fixed] fusiondirectory#5671 Scriptaculous is used in plugins but not loaded into browser
- [Fixed] fusiondirectory#5675 Error when checking LDAP when we install FD

* Fri Jun 16 2017 Jonathan SWAELENS <jonathan@opensides.be> - 1.2-1
- Fixes #5618 Correct the date error in changelog
- Fixes #5621 Correct specfile with rpmlint help
- Fixes #5435 Set an if condition for linking javascript libs

* Tue Jun 06 2017 Jonathan SWAELENS <jonathan@opensides.be> - 1.1.1-1
- New upstream release

* Wed May 17 2017 Jonathan SWAELENS <jonathan@opensides.be> - 1.1-2
- Add php-Smarty3-gettext as dependance

* Fri Apr 28 2017 Jonathan SWAELENS <jonathan@opensides.be> - 1.1-1
- Fixes #5108 Package class_exceptions.inc
- Fixes #5319 Remove class_plugin.inc
- Fixes #5325 Remove class_management.inc
- Fixes #5142 Add class_templateHandling.inc

* Mon Apr 03 2017 Jonathan SWAELENS <jonathan@opensides.be> - 1.0.20-1
- New upstream release

* Fri Jan 20 2017 Jonathan SWAELENS <jonathan@opensides.be> - 1.0.19-1
- New upstream release

* Mon Jan 16 2017 Jonathan SWAELENS <jonathan@opensides.be> - 1.0.18-1
- Fixes #5108 Add class_exceptions in packaging

* Mon Nov 14 2016 Jonathan SWAELENS <jonathan@opensides.be> - 1.0.17-1
- New upstream release

* Tue Oct 04 2016 Jonathan SWAELENS <jonathan@opensides.be> - 1.0.16-1
- New upstream release

* Tue Aug 23 2016 Jonathan SWAELENS <jonathan@opensides.be> - 1.0.15-1
- New upstream release

* Sun Jul 10 2016 Jonathan SWAELENS <jonathan@opensides.be> - 1.0.14-1
- Fixes #4986 Add the contrib files
- Fixes #4940 Rename and add patches

* Fri Jun 03 2016 Jonathan SWAELENS <jonathan@opensides.be> - 1.0.13-1
- Fixes add class_ldapGeneralizedTime.inc
- Fixes #4837 Add class_logging.inc

* Fri May 13 2016 Jonathan SWAELENS <jonathan@opensides.be> - 1.0.12-3
- Fixes #4786 Split specfile rhel6 and rhel7 to modify the php dependence of rhel6

* Tue May 10 2016 Jonathan SWAELENS <jonathan@opensides.be> - 1.0.12-2
- Fixes #4770 Fix prototype path in headers.tpl

* Tue May 03 2016 Jonathan SWAELENS <jonathan@opensides.be> - 1.0.12-1
- Fixes #4683 Modify the path for scriptaculous and prototype loading

* Thu Apr 07 2016 Jonathan SWAELENS <jonathan@opensides.be> - 1.0.11-1
- Fixes #4649 Replace php54-mcrypt with php54-openssl
- Fixes #4642 Update requirement for php to 5.4

* Thu Mar 17 2016 Jonathan SWAELENS <jonathan@opensides.be> - 1.0.10-1
- New upstream release

* Thu Jan 28 2016 Jonathan SWAELENS <jonathan@opensides.be> - 1.0.9.3-1
- Fixes #4384 Add the missing html directory to remove javascript links

* Tue Jan 05 2016 Jonathan SWAELENS <jonathan@opensides.be> - 1.0.9.2-1
- Fixes #4210 Add dependance at fusiondirectory-schema to schema2ldif
- Fixes #4232 Set fusiondirectory-apache as config file
- Fixes #4248 Remove class_SnapShotDialog.inc
- Fixes #4248 Include class_SnapshotDialogs.inc in specfile
- Fixes #4257 Add php54-mcrypt in the dependence
- Fixes #4256 Add perl-Crypt-Rijndael in the dependence
- Fixes #4326 Add php cas library
- Fixes #4269 Make symlink for javascript libraries
- Fixes #4400 Delete databaseManagement class
- Fixes #4400 Must only not create the connector docs directory

* Thu Oct 08 2015 Jonathan SWAELENS <jonathan@opensides.be> - 1.0.9.1-1.el6
- Fixes #4159 Modify syntax for postun
- Fixes #4136 Remove class_smbHash.inc
- Fixes #4136 Remove samba.schema from fusiondirectory-schema

* Thu Sep 24 2015 Jonathan SWAELENS <jonathan@opensides.be> - 1.0.9-1.el6
- Remove password and associate patch
- Fixes #4071 Fixes postun only when we uninstall a package
- Fixes #4071 Fixes postun selinux only when we uninstall the package
- Fixes #4116 Remove slapd.conf example

* Thu Jul 30 2015 Jonathan SWAELENS <jonathan@opensides.be> - 1.0.8.9-1.el6
- php54-gd as mandatory package
- replace perl-Crypt-PasswdMD5 by perl-Digest-SHA

* Tue Jun 30 2015 Jonathan SWAELENS <jonathan@opensides.be> - 1.0.8.8-1.el6
- Add rhel if to build RHEL6 and RHEL7

* Fri Jun 05 2015 Jonathan SWAELENS <jonathan@opensides.be> - 1.0.8.7-1.el6
- New upstream release

* Mon Jun 01 2015 Jonathan SWAELENS <jonathan@opensides.be> - 1.0.8.6-1.el6
- Add again rfc2307bis schema

* Wed May 06 2015 Jonathan SWAELENS <jonathan@opensides.be> - 1.0.8.5-2.el6
- Remove schema rfc2307bis
- Correct the post script
- Correct postun scriptlet of fusiondirectory and fusiondirectory-selinux

* Sat Dec 13 2014 Jonathan SWAELENS <jonathan@opensides.be> - 1.0.8.3-1.el6
- Correct the errors for the post scripts

* Sun Jun 09 2013 Olivier BONHOMME <obonhomme@nerim.net> - 1.0.6-2.el6
- Reorganize include directory files declaration in order to avoid multiple
  declaration in serveral RPMS (Closes #2504)
- Move the config/systems directory from sympa plugin to systems plugin (Closes #2423)
- Move the class_mailPluginConfig.inc file from core RPM to mail plugin (Closed #2485)
- Backport bugfix #2424 : Try to use PHP hash function if mhash is not available.
- Backport bugfix #2449 : Allow users with SAMBA attributes to be deleted properly.

* Sun May 12 2013 Olivier BONHOMME <obonhomme@nerim.net> - 1.0.6-1.el6
- Upgrade to 1.0.6 Version
- Schema are now only provided in .schema format
- Plugins reorganisation and simplification
- Gofax plugin new name : fax
- Gofon plugin new name : asterisk
- Obsolete plugins removed : netatalk, opengroupware,openxchange,pptp, phpschedule-it, webdav, connectivity, scalix
- New plugins : alias, autofs, cyrus, debconf, DSA, freeradius, game, opsi, puppet

* Fri Nov 23 2012 Olivier BONHOMME <obonhomme@nerim.net> - 1.0.4-1
- Upgrade to 1.0.4 Version
- Remove Obsoletes directives
- Remove devel package
- Update default apache configuration. Memory size set to 128M.
- Dependency list update
- New package : database-management
- Update scripts integration.

* Sat Jul 14 2012 Olivier BONHOMME <obonhomme@nerim.net> - 1.0.3-2
- Move Lost Password Feature files from argonaut plugin to core RPM - Closes #1161

* Sat Jun 23 2012 Olivier BONHOMME <obonhomme@nerim.net> - 1.0.3-1.el6
- Upgrade to 1.0.3 Version
- New plugins : argonaut, openstack-compute, quota, supann
- Merge goto plugin into system plugin
- Remove obsolete plugins : php54-gw
- Remove obsolete patches
- Add missing dependency on perl-ExtUtils-MakeMaker
- SELinux policy update
- Update memory_limite parameter in the Apache Configuration file
- Remove the spool purge cleaning step in %%pre and %%postun steps
- Add devel package

* Sun Oct 23 2011 Olivier BONHOMME <obonhomme@nerim.net> - 1.0.2-1
- Upgrade to 1.0.2 Version
- [rpm] SELinux policy update
- [rpm] Mail Queue Plugin disabled
- [rpm] Patch for get_i18n and get_classs method on fusiondirectory-setup
- [rpm] Patch for removing debug messages
- [feature] Remove online doc
- [feature] Add netgroups plugin
- [feature] Removed old GOsa-si code
- [feature] Added jsonrpc client library
- [feature] Added new daemon class with json rpc methods
- [feature] All deployment are now done through the Argonaut json rpc server
- [feature] New system to get the packages and debconf without a local mirror
- [fix] Cvs import fixes to make it more flexible and usable
- [fix] Corrected css for Firefox 5 and beyond
- [feature] New setup command fusiondirectory-setup that help fixes common setup issues
- [feature] Added tools to easily convert and upload schema in an ldap-tree
- [feature] Completely test and rewrote the help to use php safe mode
- [feature] Put all the application data into /var/cache/fusiondirectory
- [fix] Fixed timezone issues
- [fix] Corrected FSF address
- [feature] Removed the opsi (pending rewrite)
- [feature] Removed log plugin, everything is done with the rsyslog plugin

* Sun Jul 03 2011 Olivier BONHOMME <obonhomme@nerim.net> - 1.0.1-3
- Compliancy to Fedora Policy (fc15)
- Remove gosa-ldap Obsoletes block

* Sat Jun 18 2011 Olivier BONHOMME <obonhomme@nerim.net> - 1.0.1-2
- Fixes #308: Remove the heimdal package
- Fixes #309: Remove the goAgent.pl from plugin-squid package

* Mon May 09 2011 Olivier BONHOMME <obonhomme@nerim.net> - 1.0.1-1
- Update to 1.0.1 version
- Remov advanced options from setup
- Correct online help
- Correct wording on plugins
- Remove the need for magic_quotes_gpc
- Remove the fusiondirectory-desktop package
- Remove program version checking from svn
- Add the apache plugin
- Put final logo
- Full italian language
- Creation of the fusiondirectory SELinux package
- Fixes bugs #104 #118 #154 #163 #187 #188 #189 #191 #192 #193
- Fixes bugs #194 #197 #198 #199 #207 #208 #210 #217 #224 #230
- Fixes bugs #234 #251 #252

* Sun Apr 17 2011 Olivier BONHOMME <obonhomme@nerim.net> - 1.0-1
- First Plugin integration
- Update packager identity

* Fri Apr 15 2011 Benoit Mortier <benoit.mortier@opensides.be>
- First build of FusionDirectory 1.0 as an RPM, should work on SuSE and RedHat
