# TODO: see comments.
Summary:	A GUI to edit Elektra keys
Name:		regedit
Version:	0.3
Release:	0.1
Source0:	http://members.aon.at/gregorburger/%{name}-%{version}.tar.gz
# Source0-md5:	b4d7cb62aa4fb6733754c716069d3a90	
# Patch0 was made without looking into sources (via perl -pi -e "s/...
# regedit builds, but segfaults during key's values manipulation.
Patch0:		%{name}-registry2elektra_tmp_hack.patch
Patch1:		%{name}-CFLAGS.patch
Patch2:		%{name}-SIGSEGV_hack.patch
Group:		System
License:	GPL
URL:		http://www.livejournal.com/users/gregorburger/
BuildRequires:	elektra-devel
BuildRequires:	qmake
BuildRequires:	qt-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A GUI to edit Linux Registry keys, based on QT

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
qmake regedit.pro
%{__make} QTDIR=%{_prefix} CC="%{__cc}" CXX="%{__cxx}" CFLAGS="%{rpmcflags}" CXXFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_bindir}
install src/regedit $RPM_BUILD_ROOT%{_bindir}

install -d $RPM_BUILD_ROOT%{_datadir}/regedit
install icons/*.png $RPM_BUILD_ROOT%{_datadir}/regedit

install -d $RPM_BUILD_ROOT%{_datadir}/applications
install regedit.desktop $RPM_BUILD_ROOT%{_datadir}/applications/

%clean
rm -rf $RPM_BUILD_ROOT

%post
# Set the icons directory for myself
kdb set -t string system/sw/regedit/gui/iconDir "/usr/share/regedit"

%postun
# Destroy the icons directory for myself
kdb rm system/sw/regedit/gui/iconDir || :
kdb rm system/sw/regedit/gui || :
kdb rm system/sw/regedit || :

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%{_datadir}/regedit
%{_datadir}/applications/*
