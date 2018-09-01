Name:       fusiondirectory-webservice-shell
Version:    _VERSION_
Release:    _RELEASE_ 
Summary:    Shell for the FusionDirectory

Group:      Applications/System
License:    GPLv2
URL:        http://www.fusiondirectory.org

Buildarch:  noarch
Source0:    fusiondirectory-plugins-%{version}.tar.gz

Requires:   perl-Term-ReadLine-Gnu, perl-LWP-Protocol-https

%description 
This is the conmand line shell for the FusionDirectory with a webservice
FusionDirectory is a combination of system-administrator and end-user web
interface, designed to handle LDAP based setups.

%prep

%setup -c -q -n fusiondirectory-webservice-shell-%{version}
%setup -T -D -b 0 -n fusiondirectory-plugins-%{version}

%install
rm -Rf %{buildroot}

mkdir -p %{buildroot}/usr/bin/
cp ./webservice/contrib/bin/* %{buildroot}/usr/bin/
chmod +x %{buildroot}/usr/bin/*

mkdir -p %{buildroot}/usr/share/doc/fusiondirectory-webservice-shell/
cp ./webservice/contrib/docs/* %{buildroot}/usr/share/doc/fusiondirectory-webservice-shell/

mkdir -p %{buildroot}/usr/share/man/man1/
gzip ./webservice/contrib/man/*
cp ./webservice/contrib/man/* %{buildroot}/usr/share/man/man1/

%clean
rm -Rf %{buildroot}

%files
%defattr(0644,root,root)
%attr(0755,root,root) /usr/bin/fusiondirectory-shell
%doc %attr(-,root,root) %{_datadir}/doc/fusiondirectory-webservice-shell/jsonrpc.php.doc
%attr(-,root,root) %{_datadir}/man/man1/fusiondirectory-shell.1.gz

%changelog
* Sat Sep 01 2018 Jonathan SWAELENS <jonathan@opensides.be> - 1.2.2-1
- New upstream release

* Mon Jun 11 2018 Jonathan SWAELENS <jonathan@opensides.be> - 1.2.1-1
- New upstream release

* Fri Jun 16 2017 Jonathan SWAELENS <jonathan@opensides.be> - 1.2-1
- Fixes #5621 Correct specfile with rpmlint help

* Tue Jun 06 2017 Jonathan SWAELENS <jonathan@opensides.be> - 1.1.1-1
- New upstream release

* Wed May 17 2017 Jonathan SWAELENS <jonathan@opensides.be> - 1.1-2
- Add php54-php-Smarty3-gettext as dependance

* Fri Apr 28 2017 Jonathan SWAELENS <jonathan@opnesides.be> - 1.1-1
- New upstream release
