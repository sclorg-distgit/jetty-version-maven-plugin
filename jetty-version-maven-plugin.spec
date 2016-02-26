%global pkg_name jetty-version-maven-plugin
%{?scl:%scl_package %{pkg_name}}
%{?maven_find_provides_and_requires}

Name:           %{?scl_prefix}%{pkg_name}
Version:        1.0.7
Release:        9.12%{?dist}
Summary:        Jetty version management Maven plugin

License:        ASL 2.0 or EPL
URL:            http://www.eclipse.org/jetty/
Source0:        http://git.eclipse.org/c/jetty/org.eclipse.jetty.toolchain.git/snapshot/%{pkg_name}-%{version}.tar.bz2
BuildArch:      noarch

BuildRequires:  %{?scl_prefix}maven-local
BuildRequires:  %{?scl_prefix}mvn(org.apache.commons:commons-lang3)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven:maven-plugin-api)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven:maven-project)
BuildRequires:  %{?scl_prefix}mvn(org.eclipse.jetty.toolchain:jetty-toolchain:pom:)


%description
Jetty version management Maven plugin

%package        javadoc
Summary:        API documentation for %{pkg_name}

%description    javadoc
%{summary}.


%prep
%setup -q -n %{pkg_name}-%{version}
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
# copy license files
cp -p jetty-distribution-remote-resources/src/main/resources/* .

# we have java.util stuff in JVM directly now
# https://bugs.eclipse.org/bugs/show_bug.cgi?id=401163
sed -i 's|edu.emory.mathcs.backport.||' \
    jetty-version-maven-plugin/src/main/java/org/eclipse/jetty/toolchain/version/Release.java
%{?scl:EOF}

%build
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
pushd %{pkg_name}
# skip tests because we don't have jetty-test-helper (yet)
%mvn_build -f
%{?scl:EOF}

%install
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
pushd %{pkg_name}
%mvn_install
%{?scl:EOF}


%files -f %{pkg_name}/.mfiles
%dir %{_mavenpomdir}/%{pkg_name}
%dir %{_javadir}/%{pkg_name}
%doc LICENSE-APACHE-2.0.txt LICENSE-ECLIPSE-1.0.html notice.html

%files javadoc -f %{pkg_name}/.mfiles-javadoc
%doc LICENSE-APACHE-2.0.txt LICENSE-ECLIPSE-1.0.html notice.html

%changelog
* Mon Feb 08 2016 Michal Srb <msrb@redhat.com> - 1.0.7-9.12
- Fix BR on maven-local & co.

* Mon Jan 11 2016 Michal Srb <msrb@redhat.com> - 1.0.7-9.11
- maven33 rebuild #2

* Sat Jan 09 2016 Michal Srb <msrb@redhat.com> - 1.0.7-9.10
- maven33 rebuild

* Thu Jan 15 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0.7-9.9
- Add directory ownership on %%{_mavenpomdir} subdir

* Wed Jan 14 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0.7-9.8
- Fix BR on jetty-toolchain POM

* Tue Jan 13 2015 Michael Simacek <msimacek@redhat.com> - 1.0.7-9.8
- Mass rebuild 2015-01-13

* Tue Jan 06 2015 Michael Simacek <msimacek@redhat.com> - 1.0.7-9.7
- Mass rebuild 2015-01-06

* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0.7-9.6
- Mass rebuild 2014-05-26

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0.7-9.5
- Mass rebuild 2014-02-19

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0.7-9.4
- Mass rebuild 2014-02-18

* Mon Feb 17 2014 Michal Srb <msrb@redhat.com> - 1.0.7-9.3
- SCL-ize BR

* Thu Feb 13 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0.7-9.2
- Rebuild to regenerate auto-requires

* Tue Feb 11 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0.7-9.1
- First maven30 software collection build

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.0.7-9
- Mass rebuild 2013-12-27

* Thu Jul 11 2013 Michal Srb <msrb@redhat.com> - 1.0.7-8
- Build with XMvn
- Fix BR

* Tue Feb 19 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.0.7-7
- Fix backport-util-concurrent dependency
- Use file lists

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.0.7-6
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Sep 20 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0.7-5
- Install license files

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov  4 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.0.7-2
- Add minimal maven version for BR

* Thu Nov  3 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.0.7-1
- Initial version of the package
