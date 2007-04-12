%define name		jdepend
%define version		2.9
%define release		2
%define section		free
%define gcj_support	1

Name:		%{name}
Version:	%{version}
Release:	%mkrel %{release}
Epoch:		0
Summary:        Java Design Quality Metrics
License:        BSD-style
Url:            http://www.clarkware.com/
Group:          Development/Java
#Vendor:         JPackage Project
#Distribution:	JPackage
Source0:        http://www.clarkware.com/software/%{name}-%{version}-MDVCLEAN.tar.bz2
BuildRequires:  ant
%if %{gcj_support}
Requires(post): java-gcj-compat
Requires(postun): java-gcj-compat
BuildRequires:  java-gcj-compat-devel
%else
BuildArch:      noarch
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-buildroot

%description
JDepend traverses a set of Java class and source file directories and
generates design quality metrics for each Java package. JDepend allows
you to automatically measure the quality of a design in terms of its
extensibility, reusability, and maintainability to effectively manage
and control package dependencies.

%package javadoc
Summary:	Javadoc for %{name}
Group:		Development/Java

%description javadoc
Javadoc for %{name}.

%package demo
Summary:	Demos for %{name}
Group:		Development/Java
Requires:	%{name} = %{version}-%{release}

%description demo
Demonstrations and samples for %{name}.

%prep
%setup -q
# remove all binary libs
find . -name "*.jar" -exec rm -f {} \;
# fix strange permissions
find . -type d -exec chmod 755 {} \;

%build
%ant jar javadoc

%install
# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -m 644 dist/%{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} ${jar/-%{version}/}; done)
# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr build/docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
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

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(-,root,root)
%doc README LICENSE docs
%{_javadir}/*
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif

%files javadoc
%defattr(-,root,root)
%{_javadocdir}/%{name}-%{version}

%files demo
%defattr(-,root,root)
%{_datadir}/%{name}


