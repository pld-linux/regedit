Summary:	A GUI to edit Elektra (a.k.a Linux Registry) keys
Summary(pl):	GUI oparte o QT do edycji kluczy Elektry (a.k.a Rejestr Linuksa)
Name:		regedit
Version:	0.3
Release:	0.1
License:	GPL
Group:		Base
Source0:	http://download.berlios.de/tlr-regedit/%{name}-%{version}.tar.gz
# Source0-md5:	b4d7cb62aa4fb6733754c716069d3a90
Source1:	%{name}-exit.png
Patch0:		%{name}-registry2elektra_tmp_hack.patch
Patch1:		%{name}-CFLAGS.patch
Patch2:		%{name}-SIGSEGV_hack.patch
Patch3:		%{name}-quit.patch
URL:		http://www.livejournal.com/users/gregorburger/
BuildRequires:	elektra-devel
BuildRequires:	qmake
BuildRequires:	qt-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A GUI to edit Elektra (a.k.a Linux Registry) keys, based on QT.

%description -l pl
GUI oparte o QT do edycji kluczy Elektry (znanej równie¿ jako Rejestr
Linuksa).

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
qmake regedit.pro
%{__make} \
	QTDIR=%{_prefix} \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	CFLAGS="%{rpmcflags}" \
	CXXFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_bindir}
install src/regedit $RPM_BUILD_ROOT%{_bindir}

install -d $RPM_BUILD_ROOT%{_datadir}/regedit
install icons/*.png $RPM_BUILD_ROOT%{_datadir}/regedit

install -d $RPM_BUILD_ROOT%{_desktopdir}
install regedit.desktop $RPM_BUILD_ROOT%{_desktopdir}

install %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/%{name}/exit.png

%clean
rm -rf $RPM_BUILD_ROOT

%post
# Set the icons directory for myself
kdb set -t string system/sw/regedit/gui/iconDir "%{_datadir}/regedit"

%postun
# Destroy the icons directory for myself
kdb rm system/sw/regedit/gui/iconDir || :
kdb rm system/sw/regedit/gui || :
kdb rm system/sw/regedit || :

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%{_datadir}/regedit
%{_desktopdir}/*.desktop
