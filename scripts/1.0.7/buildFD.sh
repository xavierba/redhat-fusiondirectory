#!/bin/bash
# Script to use for the build action in Jenkins
# $1 is the mock_conf
# $2 is the branch of FusionDirectory
# $3 is the version of FusionDirectory

# Variables
HOME="$(pwd ~)"
MOCK_CONF="$1"
BRANCH_FD="$2"
VERSION_FD="$3"
JENKINSBUILD="$4"
SOURCES_URL="http://download.fusiondirectory.org/sources"


if [ $# -ne 4 ];
then
  echo "Usage: $(basename $0) <mock_conf> <fd_branch> <version_fd>"
  exit 1
fi

# Create temporary working directory
TMPDIR="$(mktemp -d)"
cd ${TMPDIR}

# Downoad Checksum and check signature gpg
wget ${SOURCES_URL}/${BRANCH_FD}/fusiondirectory/CHECKSUM.MD5

if [ $? -ne 0 ] ; then
  echo "Unable to download the checksum"
  exit 1
fi

# Download signature
wget ${SOURCES_URL}/${BRANCH_FD}/fusiondirectory/CHECKSUM.MD5.asc
if [ $? -ne 0 ] ; then
  echo "Unable to download GPG signature for the checksum"
  exit 2
fi

# Verifying signature for the checksum
gpg --verify CHECKSUM.MD5.asc

if [ $? -ne 0 ] ; then 
  echo "Bad Signature for core component"
  exit 3
fi


# Downloading and check signature for the core component
wget ${SOURCES_URL}/${BRANCH_FD}/fusiondirectory/fusiondirectory-${VERSION_FD}.tar.gz

if [ $? -ne 0 ] ; then
  echo "Unable to download core archive"
  exit 1
fi

# Download signature
wget ${SOURCES_URL}/${BRANCH_FD}/fusiondirectory/fusiondirectory-${VERSION_FD}.tar.gz.asc
if [ $? -ne 0 ] ; then
  echo "Unable to download GPG signature for core archive"
  exit 2
fi

# Verifying signature for the core component
gpg --verify fusiondirectory-${VERSION_FD}.tar.gz.asc

if [ $? -ne 0 ] ; then 
  echo "Bad Signature for core component"
  exit 3
fi


# Downloading and check signature for the plugin component
wget ${SOURCES_URL}/${BRANCH_FD}/fusiondirectory/fusiondirectory-plugins-${VERSION_FD}.tar.gz

if [ $? -ne 0 ] ; then
  echo "Unable to download plugins archive"
  exit 1
fi

# Download signature
wget ${SOURCES_URL}/${BRANCH_FD}/fusiondirectory/fusiondirectory-plugins-${VERSION_FD}.tar.gz.asc
if [ $? -ne 0 ] ; then 
  echo "Unable to download GPG signature for plugins archive"
  exit 2
fi

# Verify the MD5 for the tar.gz
cat CHECKSUM.MD5 | grep "${VERSION_FD}" | md5sum -c -
if [ $? -ne 0 ] ; then
  echo "Error in the verification of the MD5 in the tar.gz"
  exit 4
fi

# Create fusiondirectory.spec
cp ${TMPDIR}/fusiondirectory-${VERSION_FD}.tar.gz ${TMPDIR}/fusiondirectory-plugins-${VERSION_FD}.tar.gz ~/packaging-rpm/scripts/
# Generate plugins spec file
cd ~/packaging-rpm/scripts/
./generate_plugin_package.sh ${VERSION_FD}
./generate_plugin_files.sh ${VERSION_FD}
./generate_post_plugins.sh ${VERSION_FD}
./generate_postun_plugins.sh ${VERSION_FD}
# All in one spec file
cd ./specs/
cat header.spec package_core.spec package_plugins.spec package_plugins.spec_schema \
    prep.spec install.spec post_core.spec post_plugins.spec postun_plugins.spec \
    files_core.spec files_plugins.spec files_plugins.spec_schema files_exclude.spec \
    changelog-core.spec > fusiondirectory.spec

sed -i "s#JENKINSBUILD#jenkinsbuild${JENKINSBUILD}#g" fusiondirectory.spec

# Create an SRPMS
cd ${TMPDIR}/
mkdir -p ${HOME}/rpmbuild/SOURCES/
mv fusiondirectory-${VERSION_FD}.tar.gz fusiondirectory-plugins-${VERSION_FD}.tar.gz  ${HOME}/rpmbuild/SOURCES/
rpmbuild -bs ${HOME}/packaging-rpm/scripts/specs/fusiondirectory.spec

# Compile and test the SRPMS
/usr/bin/mock -r ${MOCK_CONF} clean
/usr/bin/mock -r ${MOCK_CONF} ${HOME}/rpmbuild/SRPMS/fusiondirectory-${VERSION_FD}-jenkinsbuild${JENKINSBUILD}.src.rpm

rm ${HOME}/rpmbuild/SRPMS/fusiondirectory-${VERSION_FD}-2.el6.src.rpm

# Copy the SRPMS and RPMS to build_result
cp -a /var/lib/mock/${MOCK_CONF}/root/builddir/build/SRPMS/* ${HOME}/build_result/SRPMS/
cp -a /var/lib/mock/${MOCK_CONF}/root/builddir/build/RPMS/* ${HOME}/build_result/RPMS/

# Remove TMPDIR
rm -Rf ${TMPDIR}/

