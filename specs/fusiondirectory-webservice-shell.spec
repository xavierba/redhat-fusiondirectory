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
* Mon Feb 01 2016 Jonathan SWAELENS <jonathan@opensides.be> - 1.0.9.3-1
- New upstream release

* Mon Oct 26 2015 Jonathan SWAELENS <jonathan@opensides.be> - 1.0.9.2-1
- Fixes #4262 Add perl-LWP-Protocol-https dependance

* Sat Sep 07 2015 Jonathan SWAELENS <jonathan@opensides.be> - 1.0.9-1
- Fixes #4089 Add fusiondirectory-shell in rpm
