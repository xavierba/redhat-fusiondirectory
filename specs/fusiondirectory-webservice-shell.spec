Name:       fusiondirectory-webservice-shell
Version:    _VERSION_
Release:    _RELEASE_ 
Summary:    Shell for the FusionDirectory

Group:      Applications/System
License:    GPLv2
URL:        http://www.fusiondirectory.org

Buildarch:  noarch
Source0:    fusiondirectory-plugins-%{version}.tar.gz

Requires:   perl-Term-ReadLine-Gnu

%description 
This is the conmand line shell for the FusionDirectory with a webservice
FusionDirectory is a combination of system-administrator and end-user web
interface, designed to handle LDAP based setups.

%prep

%setup -c -q -n fusiondirectory-webservice-shell-%{version}
%setup -T -D -b 0 -n fusiondirectory-plugins-%{version}

%install
mkdir -p %{buildroot}/usr/share/bin/
cp ./webservice/contrib/bin/* %{buildroot}/usr/share/bin/
chmod +x %{buildroot}/usr/share/bin/*

mkdir -p %{buildroot}/usr/share/doc/fusiondirectory-webservice-shell/
cp ./webservice/contrib/docs/* %{buildroot}/usr/share/doc/fusiondirectory-webservice-shell/

mkdir -p %{buildroot}/usr/share/man/man1/
gzip ./webservice/contrib/man/*
cp ./webservice/contrib/man/* %{buildroot}/usr/share/man/man1/

%clean
rm -Rf %{buildroot}

%files
%defattr(0644,root,root)
/usr/share/bin/fusiondirectory-shell
/usr/share/doc/fusiondirectory-webservice-shell/jsonrpc.php.doc
/usr/share/man/man1/fusiondirectory-shell.1.gz
