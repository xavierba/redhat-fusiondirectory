Name:           perl-Net-LDAP-Server
Version:        0.43
Release:        _SUB-VERSION_
Summary:        Net::LDAP::Server Perl module
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Net-LDAP-Server/
Source0:        http://www.cpan.org/authors/id/A/AA/AAR/Net-LDAP-Server-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  perl(Convert::ASN1)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Net::LDAP)
Requires:       perl(Convert::ASN1)
Requires:       perl(Net::LDAP)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Net::LDAP::Server provides the protocol handling for an LDAP server. You
can subclass it and implement the methods you need. Then you just
instantiate your subclass and call its C<handle> method to establish a
connection with the client.

%prep
%setup -q -n Net-LDAP-Server-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check
#Problems with check
#make test

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc Changelog README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Thu Jul 03 2014 SWAELENS Jonathan <swaelens.jonathan@openmailbox.org>
- Specfile autogenerated by cpanspec 1.78.