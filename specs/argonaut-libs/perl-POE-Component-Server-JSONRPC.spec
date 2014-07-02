Name:           perl-POE-Component-Server-JSONRPC
Version:        _VERSION_ 
Release:        1%{dist}
Summary:        POE tcp and http based JSON-RPC 1.0 server
License:	Artistic or GPL-1+
Group:          Development/Libraries

URL:            http://search.cpan.org/dist/POE-Component-Server-JSONRPC/
Source0:        http://search.cpan.org/CPAN/authors/id/M/MC/MCMIC/POE-Component-Server-JSONRPC-%{version}.tar.gz
Source1:	copyright-POE-Component-Server-JSONRPC
Patch0:		remove_test.patch
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:      noarch
BuildRequires:  perl, perl-ExtUtils-MakeMaker

Requires:	perl, perl-POE, perl-Class-Accessor, perl-JSON-Any

%description
This perl POE component allows you easily create a
HTTP json rpc server inside POE

%prep
%setup -T -D -b 0 -n POE-Component-Server-JSONRPC-%{version}
%patch0 -p1
cp /builddir/build/SOURCES/copyright-POE-Component-Server-JSONRPC ./copyright


%build
perl Makefile.PL
make

%check
make test

%install
# Grab perl version for the directory
PERLDIR=$(basename $(cat ./Makefile | grep 'SITELIBEXP' | tr -d ' ' | cut -d '=' -f2))

# Go into the directory
cd ./blib/

# Remove all the .exists
find . -name '.exists' -exec rm "{}" \;

# Create directories in buildroot
mkdir -p %{buildroot}/usr/share/man/
mkdir -p %{buildroot}/usr/share/${PERLDIR}/

# Copy files in buildroot
cp -a ./man3/ %{buildroot}/usr/share/man/
cp -a ./lib/POE/ %{buildroot}/usr/share/${PERLDIR}/

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_mandir}/man3/*
/usr/share/perl5/POE/Component/Server/*

%doc Changes README LICENSE copyright

%changelog
* Fri May 9 2014 Jonathan SWAELENS <swaelens.jonathan@openmailbox.org>
- Initial Release
