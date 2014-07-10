Name:           perl-DNS-ZoneParse
Version:        1.10
Release:        _SUB-VERSION_
Summary:        Perl extension for parsing and manipulating DNS Zone Files 
License:	Artistic or GPL-1+
Group:          Development/Libraries

URL:            http://search.cpan.org/dist/DNS-ZoneParse/
Source0:        http://search.cpan.org/CPAN/authors/id/M/MS/MSCHILLI/DNS-ZoneParse-%{version}.tar.gz
Source1:	copyright-DNS-ZoneParse
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:      noarch
BuildRequires:  perl, perl-ExtUtils-MakeMaker

Requires:	perl
Requires:	perl(Test::More)

%description
DNS::ZoneParse will parse a Zone File and put all the Resource Records (RRs)
into an anonymous hash structure. At the moment, the following types of RRs
are supported: SOA, NS, MX, A, CNAME, TXT, PTR. It could be useful for
maintaining DNS zones, or for transferring DNS zones to other servers. If you
want to generate an XML-friendly version of your zone files, it is easy to
use XML::Simple with this module once you have parsed the zonefile.
.
DNS::ZoneParse scans the DNS zonefile - removes comments and seperates
the file into its constituent records. It then parses each record and
stores the records internally.

%prep
%setup -T -D -b 0 -n DNS-ZoneParse-%{version}
cp /builddir/build/SOURCES/copyright-DNS-ZoneParse ./copyright


%build
perl Makefile.PL
make

%check
# Test not work in chroot???
#make test

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
cp -a ./lib/DNS/ %{buildroot}/usr/share/${PERLDIR}/

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_mandir}/man3/*
/usr/share/perl5/DNS/*

%doc Changes README copyright

%changelog
* Fri May 9 2014 Jonathan SWAELENS <swaelens.jonathan@openmailbox.org>
- Initial Release
