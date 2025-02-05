%{?_javapackages_macros:%_javapackages_macros}
# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

Name:           jdepend
Version:        2.9.1
Release:        12.3
Group:		Development/Java
Epoch:          0
Summary:        Java Design Quality Metrics
License:        BSD
URL:            https://www.clarkware.com/

#Downloaded from http://github.com/clarkware/jdepend/tarball/2.9.1
Source0:        clarkware-jdepend-5798059.tar.gz
Source1:        %{name}-%{version}.pom
BuildArch:      noarch

Requires:      java
Requires:      jpackage-utils

BuildRequires: ant
BuildRequires: java-devel
BuildRequires: jpackage-utils

%description
JDepend traverses a set of Java class and source file directories and
generates design quality metrics for each Java package. JDepend allows
you to automatically measure the quality of a design in terms of its
extensibility, reusability, and maintainability to effectively manage
and control package dependencies.

%package javadoc
Summary:    Javadoc for %{name}

Requires:   %{name} = %{version}-%{release}

%description javadoc
Javadoc for %{name}.

%package demo
Summary:    Demos for %{name}

Requires:   %{name} = %{version}-%{release}

%description demo
Demonstrations and samples for %{name}.

%prep
%setup -q -n clarkware-jdepend-5798059
# remove all binary libs
find . -name "*.jar" -exec rm -f {} \;
# fix strange permissions
find . -type d -exec chmod 755 {} \;

%build
ant jar javadoc

%install
# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -m 644 dist/%{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar
# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr build/docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} 
rm -rf build/docs/api
# demo
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -pr sample $RPM_BUILD_ROOT%{_datadir}/%{name}
# pom
install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -pm 644 %{SOURCE1} $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}.pom
# depmap
%add_maven_depmap JPP-%{name}.pom %{name}.jar

%files -f .mfiles
%doc README LICENSE docs

%files javadoc
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}

%files demo
%{_datadir}/%{name}

%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.9.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.9.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.9.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 19 2012 Jaromir Capik <jcapik@redhat.com> 0:2.9.1-6
- Fixing #832140 - jdepend post error
- Minor spec file changes according to the latest guidelines

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.9.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 03 2011 Marek Goldmann <mgoldman@redhat.com> 0:2.9.1-4
- Added Maven POM

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 9 2010 Alexander Kurtakov <akurtako@redhat.com> 0:2.9.1-2
- Install unversioned javadoc.

* Sat Jan 9 2010 Alexander Kurtakov <akurtako@redhat.com> 0:2.9.1-1
- Update to upstream 2.9.1.
- Fix merge review comments rhbz #225942.

* Tue Aug 11 2009 Alexander Kurtakov <akurtako@redhat.com> 0:2.9-1
- Update to upstream 2.9.
- Drop gcj support.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.6-9.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.6-8.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:2.6-7.4
- drop repotag
- fix license tag

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0:2.6-7jpp.3
- Autorebuild for GCC 4.3

* Thu Apr 26 2007 Matt Wringe <mwringe@redhat.com> - 0:2.6-6jpp.3
- rebuild

* Thu Oct 26 2006 Fernando Nasser <fnasser at redhat.com> - 0:2.6-6jpp.2
- Really add missing javadoc requires this time

* Thu Aug 10 2006 Matt Wringe <mwringe at redhat.com> - 0:2.6-6jpp.1
- Merge with upstream version
 - Add missing javadoc post and postun
 - Add missing javadoc requires

* Sat Jul 22 2006 Jakub Jelinek <jakub@redhat.com> - 0:2.6-5jpp_2fc
- Rebuilt

* Thu Jul 20 2006 Matt Wringe <mwringe at redhat.com> - 0:2.6-5jpp_1fc
- Merge with upstream version
- Natively compile packages

* Thu Jul 20 2006 Matt Wringe <mwringe at redhat.com> - 0:2.6-5jpp
- Add conditional native compiling

* Wed May 17 2006 Fernando Nasser <fnasser@redhat.com> - 0:2.6-4jpp
- First JPP 1.7 build

* Sun Aug 23 2004 Randy Watler <rwatler at finali.com> - 0:2.6-3jpp
- Rebuild with ant-1.6.2

* Fri Apr 11 2003 David Walluck <david@anti-microsoft.org> 0:2.6-2jpp
- fix strange permissions

* Fri Apr 11 2003 David Walluck <david@anti-microsoft.org> 0:2.6-1jpp
- 2.6

* Tue Jul 09 2002 Henri Gomez <hgomez@users.sourceforge.net> 2.2-1jpp
- Initial JPackage release
