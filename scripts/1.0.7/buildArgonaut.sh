#!/bin/bash
# Script to use for the build of Argonaut in Jenkins
# $1 is the mock_conf
# $2 is the branch of FusionDirectory
# $3 is the version of Argonaut

# Variables
HOME="$(pwd ~)"
MOCK_CONF="$1"
VERSION_ARGONAUT="$2"
BUILDNUMBER="$3"

# Usage help
if [ $# -ne 3 ] ; then
  echo "Usage: $(basename $0) <mock_conf> <fd_branch> <argonaut_version>"
  exit 1
fi

# Create temporary working directory
TMPDIR="$(mktemp -d)"
cd ${TMPDIR}

# Download SRC
wget https://github.com/fusiondirectory/argonaut/archive/argonaut-${VERSION_ARGONAUT}.zip

if [ $? -ne 0 ] ; then
  echo "Unable to download the sources"
  exit 1
fi

unzip argonaut-${VERSION_ARGONAUT}.zip && rm argonaut-${VERSION_ARGONAUT}.zip
mv argonaut-argonaut-${VERSION_ARGONAUT}/ argonaut-${VERSION_ARGONAUT}/
tar cfz argonaut-${VERSION_ARGONAUT}.tar.gz argonaut-${VERSION_ARGONAUT}/ && rm -Rf argonaut-${VERSION_ARGONAUT}/

cp ${HOME}/packaging-rpm/redhat/specs/argonaut.spec ${HOME}/rpmbuild/SPECS/argonaut.spec

sed -i "s#VERSION_ARGONAUT#${VERSION_ARGONAUT}#g" ${HOME}/rpmbuild/SPECS/argonaut.spec
sed -i "s#BUILDNUMBER#jenkinsbuild${BUILDNUMBER}#g" ${HOME}/rpmbuild/SPECS/argonaut.spec

# Create an SRPMS
mkdir -p ${HOME}/rpmbuild/SOURCES/
cp ./argonaut-${VERSION_ARGONAUT}.tar.gz  ${HOME}/rpmbuild/SOURCES/

rpmbuild -bs ${HOME}/rpmbuild/SPECS/argonaut.spec

# Compile and test the SRPMS
/usr/bin/mock -r ${MOCK_CONF} clean
/usr/bin/mock -r ${MOCK_CONF} ${HOME}/rpmbuild/SRPMS/argonaut-${VERSION_ARGONAUT}-jenkinsbuild${BUILDNUMBER}.src.rpm

rm ${HOME}/rpmbuild/SRPMS/argonaut-${VERSION_ARGONAUT}-jenkinsbuild${BUILDNUMBER}.src.rpm

# Copy the SRPMS and RPMS to build_result
cp -a /var/lib/mock/${MOCK_CONF}/root/builddir/build/SRPMS/* ${HOME}/build_result/SRPMS/
cp -a /var/lib/mock/${MOCK_CONF}/root/builddir/build/RPMS/* ${HOME}/build_result/RPMS/

# Remove TMPDIR
rm -Rf ${TMPDIR}/

