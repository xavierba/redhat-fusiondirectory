# Config file for mock
MOCK_CONF="$1"

# FD Branch
BRANCH_FD="$2"

# FD Version
VERSION_FD="$3"

# Jenkins build
JENKINSBUILD="$4"


# Create temporary working directory
TMPDIR="$(mktemp -d)"
cd ${TMPDIR}


# Download src and tar.gz
wget --no-check-certificate https://github.com/fusiondirectory/fusiondirectory/archive/${BRANCH_FD}.zip
unzip ${BRANCH_FD} && rm ${BRANCH_FD}
mv fusiondirectory-${BRANCH_FD}/ fusiondirectory-${VERSION_FD}/
tar -czf fusiondirectory-${VERSION_FD}.tar.gz fusiondirectory-${VERSION_FD}/
rm -Rf fusiondirectory-${VERSION_FD}/

# Download src plugins and tar.gz
wget --no-check-certificate https://github.com/fusiondirectory/fusiondirectory-plugins/archive/${BRANCH_FD}.zip
unzip ${BRANCH_FD} && rm ${BRANCH_FD}
mv fusiondirectory-plugins-${BRANCH_FD}/ fusiondirectory-plugins-${VERSION_FD}/
tar -czf fusiondirectory-plugins-${VERSION_FD}.tar.gz fusiondirectory-plugins-${VERSION_FD}/
rm -Rf fusiondirectory-plugins-${VERSION_FD}/


# Copy tar.gz in rpmbuild/SOURCES and copy the plugins sources for create the spec files
cp ${TMPDIR}/fusiondirectory-${VERSION_FD}.tar.gz  ~/rpmbuild/SOURCES/
cp ${TMPDIR}/fusiondirectory-plugins-${VERSION_FD}.tar.gz ~/rpmbuild/SOURCES/
cp ${TMPDIR}/fusiondirectory-plugins-${VERSION_FD}.tar.gz ~/packaging-rpm/scripts/


# Generate plugins spec file
cd ~/packaging-rpm/scripts/
./generate_plugin_package_dev.sh ${VERSION_FD}
./generate_plugin_files_dev.sh ${VERSION_FD}
./generate_post_plugins_dev.sh ${VERSION_FD}
./generate_postun_plugins_dev.sh ${VERSION_FD}

# Create fusiondirectory.spec
# All in one spec file
cd ./specs/
cat /home/jswaelens/dev/template/FD_PLUGINS_SPEC package_plugins.spec package_plugins.spec_schema \
    post_plugins.spec postun_plugins.spec \
    files_plugins.spec files_plugins.spec_schema \
    changelog-core.spec > fusiondirectoryPLUGINS.spec


# Replace version and dist in FD spec file
sed -i "s#VERSION_FD#${VERSION_FD}#g" fusiondirectoryPLUGINS.spec
sed -i "s#JENKINSBUILD#jenkinsbuild${JENKINSBUILD}#g" fusiondirectoryPLUGINS.spec
sed -i "s#%{name}#fusiondirectory#g" fusiondirectoryPLUGINS.spec


# Create an SRPMS
rpmbuild -bs ${HOME}/packaging-rpm/scripts/specs/fusiondirectoryPLUGINS.spec

# Compile and test the SRPMS
/usr/bin/mock -r ${MOCK_CONF} clean
/usr/bin/mock -r ${MOCK_CONF} ${HOME}/rpmbuild/SRPMS/fusiondirectory-plugin-${VERSION_FD}-jenkinsbuild${JENKINSBUILD}.src.rpm

rm ${HOME}/rpmbuild/SRPMS/fusiondirectory-${VERSION_FD}-2.el6.src.rpm


# Copy the SRPMS and RPMS to build_result
cp -a /var/lib/mock/${MOCK_CONF}/root/builddir/build/SRPMS/* ${HOME}/build_result/SRPMS/
cp -a /var/lib/mock/${MOCK_CONF}/root/builddir/build/RPMS/* ${HOME}/build_result/RPMS/

# Remove TMPDIR
rm -Rf ${TMPDIR}/


