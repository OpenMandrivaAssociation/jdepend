Summary:        Java Design Quality Metrics
Name:           jdepend
Version:        2.9.1
Release:        2
License:        BSD-style
Url:            http://clarkware.com/software/JDepend.html
Group:          Development/Java
Source0:        http://www.clarkware.com/software/jdepend-%{version}.zip
BuildRequires:  ant
BuildRequires:  java-rpmbuild
BuildRequires:	java-1.6.0-openjdk-devel
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
Requires:       %{name} = %{EVRD}

%description demo
Demonstrations and samples for %{name}.

%prep
%setup -q
# remove all binary libs
find . -name "*.jar" -exec rm -f {} \;
# fix strange permissions
find . -type d -exec chmod 755 {} \;

%build
export JAVA_HOME=%{_prefix}/lib/jvm/java-1.6.0
ant jar javadoc

%install
# jars
install -d -m 755 %{buildroot}%{_javadir}
install -m 644 dist/%{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} ${jar/-%{version}/}; done)
# javadoc
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -a build/docs/api/* %{buildroot}%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}
# demo
install -d -m 755 %{buildroot}%{_datadir}/%{name}
cp -pr sample %{buildroot}%{_datadir}/%{name}

# fix end-of-line
sed -i -e 's/\r\n/\n/g' README LICENSE

for i in `find docs -type f`; do
	sed -i -e 's/\r\n/\n/g' $i
done

for i in `find %{buildroot}%{_datadir}/%{name} -type f -name "*.java" -o -name "*.properties"`; do
	sed -i -e 's/\r\n/\n/g' $i
done

for i in `find %{buildroot}%{_javadocdir} -type f -name "*.htm*" -o -name "*.css"`; do
	sed -i -e 's/\r\n/\n/g' $i
done

%files
%doc README LICENSE docs
%{_javadir}/*

%files javadoc
%{_javadocdir}/%{name}-%{version}
%dir %{_javadocdir}/%{name}

%files demo
%{_datadir}/%{name}

