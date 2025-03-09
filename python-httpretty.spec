#
# Conditional build:
%bcond_without	tests	# unit/functional tests
%bcond_with	doc	# build Sphinx documentation (already built docs included in dist as of 0.9.7)
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define 	module	httpretty
Summary:	HTTP client mock for Python
Summary(pl.UTF-8):	Atrapa klienta HTTP dla Pythona
Name:		python-%{module}
# note: keep 0.9.x here for python2 support
Version:	0.9.7
Release:	5
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/httpretty/
Source0:	https://files.pythonhosted.org/packages/source/h/httpretty/httpretty-%{version}.tar.gz
# Source0-md5:	2fc3d0dc986200be95ce8ad3ef56bc04
Patch0:		%{name}-mock.patch
URL:		https://httpretty.readthedocs.io/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-coverage
BuildRequires:	python-httplib2
BuildRequires:	python-mock
BuildRequires:	python-nose
BuildRequires:	python-nose_randomly
BuildRequires:	python-rednose
BuildRequires:	python-requests
BuildRequires:	python-six >= 1.11.0
BuildRequires:	python-sure >= 1.2.24
BuildRequires:	python-tornado
BuildRequires:	python3-urllib3
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.6
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-coverage
BuildRequires:	python3-httplib2
BuildRequires:	python3-nose
BuildRequires:	python3-nose_randomly
BuildRequires:	python3-rednose
BuildRequires:	python3-requests
BuildRequires:	python3-six >= 1.11.0
BuildRequires:	python3-sure >= 1.2.24
BuildRequires:	python3-tornado
BuildRequires:	python3-urllib3
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-sphinx_rtd_theme
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
HTTP client mock for Python.

%description -l pl.UTF-8
Atrapa klienta HTTP dla Pythona.

%package -n python3-%{module}
Summary:	HTTP client mock for Python
Summary(pl.UTF-8):	Atrapa klienta HTTP dla Pythona
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.6

%description -n python3-%{module}
HTTP client mock for Python.

%description -n python3-%{module} -l pl.UTF-8
Atrapa klienta HTTP dla Pythona.

%package apidocs
Summary:	API documentation for Python httpretty module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona httpretty
Group:		Documentation

%description apidocs
API documentation for Python httpretty module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona httpretty.

%prep
%setup -q -n %{module}-%{version}
%patch -P 0 -p1

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%if %{with doc}
sphinx-build-3 -b html -d docs/build/doctrees docs/source docs/build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc COPYING README.rst
%{py_sitescriptdir}/httpretty
%{py_sitescriptdir}/httpretty-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc COPYING README.rst
%{py3_sitescriptdir}/httpretty
%{py3_sitescriptdir}/httpretty-%{version}-py*.egg-info
%endif

%files apidocs
%defattr(644,root,root,755)
%doc docs/build/html/{_modules,_static,*.html,*.js}
