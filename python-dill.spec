#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

Summary:	Serialize all of Python
Summary(pl.UTF-8):	Serializacja całości Pythona
Name:		python-dill
# keep 0.3.5.x here for python2 support
Version:	0.3.5.1
Release:	4
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/dill/
Source0:	https://files.pythonhosted.org/packages/source/d/dill/dill-%{version}.tar.gz
# Source0-md5:	3f8757f3aaa394efa67764624ab87cfd
URL:		https://pypi.org/project/dill/
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	sphinx-pdg
%endif
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
dill extends Python's pickle module for serializing and de-serializing
Python objects to the majority of the built-in Python types.
Serialization is the process of converting an object to a byte stream,
and the inverse of which is converting a byte stream back to a Python
object hierarchy.

%description -l pl.UTF-8
dill rozszerza moduł Pythona pickle do serializacji i deserializacji
obiektów pythonowych na większość wbudowanych typów Pythona.
Serializacja to proces przekształcania obiektu na strumień bajtów, a
deserializacja - odwrotność, czyli konwersja strumienia bajtów z
powrotem do hierarchii obiektów Pythona.

%package apidocs
Summary:	API documentation for Python dill module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona dill
Group:		Documentation

%description apidocs
API documentation for Python dill module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona dill.

%prep
%setup -q -n dill-%{version}

sed -i -e "s#python =.*#python = '%{__python}'#g" tests/__main__.py

%build
%py_build

%if %{with tests}
PYTHONPATH=$(pwd) \
%{__python} tests/__main__.py
%endif

%if %{with doc}
PYTHONPATH=$(pwd) \
%{__make} -C docs html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py_install

for bin in get_objgraph undill ; do
	%{__mv} $RPM_BUILD_ROOT%{_bindir}/${bin} $RPM_BUILD_ROOT%{_bindir}/${bin}-2
done

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE README.md
%attr(755,root,root) %{_bindir}/get_objgraph-2
%attr(755,root,root) %{_bindir}/undill-2
%{py_sitescriptdir}/dill
%{py_sitescriptdir}/dill-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/build/{_static,*.html,*.js}
%endif
