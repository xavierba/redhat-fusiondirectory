Name:           perl-POE-Component-Pool-Thread
Version:        _VERSION_
Release:        1%{dist}
Summary:        A POE Managed Boss/Worker threadpool
License:	Artistic or GPL-1+
Group:          Development/Libraries

URL:            http://search.cpan.org/dist/POE-Component-Pool-Thread/
Source0:        http://search.cpan.org/CPAN/authors/id/T/TA/TAG/POE-Component-Pool-Thread-%{version}.tar.gz
Source1:	copyright-POE-Component-Pool-Thread
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:      noarch
BuildRequires:  perl, perl-ExtUtils-MakeMaker

Requires:	perl, perl-POE >= 0.3

%description
This is an expand-on-demand thread pool managed through a POE session in a
manner that does not interfer with cooperative multitasking. A single pipe is
created, each thread communicates its state to the main process through this
pipe. No serialization occurs (these are threads, not child processes), so
execution is very fast.

This description was automagically extracted from the module by dh-make-perl.

%prep
%setup -T -D -b 0 -n POE-Component-Pool-Thread-%{version}
cp /builddir/build/SOURCES/copyright-POE-Component-Pool-Thread ./copyright

%build
%{__perl} Makefile.PL
make

%check
# Bad test
# make test

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
/usr/share/perl5/POE/Component/Pool/Thread.pm

%doc CHANGES copyright

%changelog
* Thu May 8 2014 Jonathan SWAELENS <swaelens.jonathan@openmailbox.org>
- Initial Release
