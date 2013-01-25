Name:           jdepend
Version:        2.9.1
Release:        2
Epoch:          0
Summary:        Java Design Quality Metrics
License:        BSD-style
Url:            http://clarkware.com/software/JDepend.html
Group:          Development/Java
Source0:        http://www.clarkware.com/software/jdepend-%{version}.zip
BuildRequires:  java-rpmbuild java-1.6.0-openjdk-devel
BuildRequires:  ant
BuildArch:      noarch

%description
JDepend traverses a set of Java class and source file directories and
generates design quality metrics for each Java package. JDepend allows
you to automatically measure the quality of a design in terms of its
extensibility, reusability, and maintainability to effectively manage
and control package dependencies.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
Javadoc for %{name}.

%package demo
Summary:        Demos for %{name}
Group:          Development/Java
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description demo
Demonstrations and samples for %{name}.

%prep
%setup -q
# remove all binary libs
find . -name "*.jar" -exec rm -f {} \;
# fix strange permissions
find . -type d -exec chmod 755 {} \;

%build
export JAVA_HOME=%_prefix/lib/jvm/java-1.6.0
ant jar javadoc

%install
%{__rm} -rf %{buildroot}

# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -m 644 dist/%{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} ${jar/-%{version}/}; done)
# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -a build/docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
%{__ln_s} %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}
# demo
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -pr sample $RPM_BUILD_ROOT%{_datadir}/%{name}

# fix end-of-line
%{__perl} -pi -e 's/\r\n/\n/g' README LICENSE

for i in `find docs -type f`; do
    %{__perl} -pi -e 's/\r\n/\n/g' $i
done

for i in `find $RPM_BUILD_ROOT%{_datadir}/%{name} -type f -name "*.java" -o -name "*.properties"`; do
    %{__perl} -pi -e 's/\r\n/\n/g' $i
done

for i in `find $RPM_BUILD_ROOT%{_javadocdir} -type f -name "*.htm*" -o -name "*.css"`; do
    %{__perl} -pi -e 's/\r\n/\n/g' $i
done

%files
%defattr(0644,root,root,0755)
%doc README LICENSE docs
%{_javadir}/*

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}
%dir %{_javadocdir}/%{name}

%files demo
%defattr(0644,root,root,0755)
%{_datadir}/%{name}


%changelog
* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 0:2.9.1-1.0.8mdv2011.0
+ Revision: 665822
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 0:2.9.1-1.0.7mdv2011.0
+ Revision: 606078
- rebuild

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 0:2.9.1-1.0.6mdv2010.1
+ Revision: 523070
- rebuilt for 2010.1

* Wed Sep 02 2009 Christophe Fergeau <cfergeau@mandriva.com> 0:2.9.1-1.0.5mdv2010.0
+ Revision: 425456
- rebuild

* Sat Mar 07 2009 Antoine Ginies <aginies@mandriva.com> 0:2.9.1-1.0.4mdv2009.1
+ Revision: 351301
- rebuild

* Fri Dec 21 2007 Olivier Blin <oblin@mandriva.com> 0:2.9.1-1.0.3mdv2009.0
+ Revision: 136503
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Dec 16 2007 Anssi Hannula <anssi@mandriva.org> 0:2.9.1-1.0.3mdv2008.1
+ Revision: 120812
- buildrequires java-rpmbuild

* Sat Sep 15 2007 Anssi Hannula <anssi@mandriva.org> 0:2.9.1-1.0.2mdv2008.0
+ Revision: 87429
- rebuild to filter out autorequires of GCJ AOT objects
- remove unnecessary Requires(post) on java-gcj-compat

* Sun Aug 05 2007 David Walluck <walluck@mandriva.org> 0:2.9.1-1.0.1mdv2008.0
+ Revision: 59159
- 2.9.1


* Thu Mar 15 2007 Christiaan Welvaart <spturtle@mandriva.org> 2.9-2mdv2007.1
+ Revision: 144234
- rebuild for 2007.1
- Import jdepend

* Sun Jun 04 2006 David Walluck <walluck@mandriva.org> 0:2.9-1mdv2007.0
- 2.9
- rebuild for libgcj.so.7
- aot-compile

* Sat Jan 14 2006 David Walluck <walluck@mandriva.org> 0:2.7-1mdk
- 2.7

* Sun May 08 2005 David Walluck <walluck@mandriva.org> 0:2.6-3.1mdk
- release

* Tue Aug 24 2004 Randy Watler <rwatler at finali.com> - 0:2.6-3jpp
- Rebuild with ant-1.6.2

