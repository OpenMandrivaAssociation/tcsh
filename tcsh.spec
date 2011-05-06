%define rversion %{version}.00

Summary:	An enhanced version of csh, the C shell
Name:		tcsh
Version:	6.17
Release:	%mkrel 3
License:	BSD
Group:		Shells
URL:		http://www.tcsh.org/
Source:		ftp://ftp.astron.com/pub/tcsh/tcsh-%{version}.00.tar.gz
Source1:	alias.csh
# patches from fedora
Patch1:		tcsh-6.15.00-closem.patch
Patch12:	tcsh-6.15.00-tinfo.patch
Patch13:	tcsh-6.14.00-unprintable.patch
Patch14:	tcsh-6.15.00-hist-sub.patch

# our patches
Patch101:	tcsh-6.15.00-termios.patch
Patch106:	tcsh-6.10.00-glibc_compat.patch
# handle new DIR_COLORS codes, fixes #40532, #48284
Patch107:	tcsh-6.17.00-ls-colors-var.patch
# -Wformat -Werror=format-security pseudo fixes
Patch108:	tcsh-6.17.00-str-fmt.patch

BuildRequires:	libtermcap-devel groff-for-man
Requires(post):	rpm-helper >= 0.7
Requires(postun): rpm-helper >= 0.7
Provides:	csh = %{version}
# explicit file provides
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
Tcsh is an enhanced but completely compatible version of csh, the C
shell. Tcsh is a command language interpreter which can be used both
as an interactive login shell and as a shell script command processor.
Tcsh includes a command line editor, programmable word completion,
spelling correction, a history mechanism, job control and a C language
like syntax.

%prep
%setup -q -n %{name}-%{rversion}
%patch1 -p1 -b .closem
%patch12 -p1 -b .tinfo
%patch13 -p1 -b .unprintable
%patch14 -p1 -b .hist-sub

%patch101 -p1 -b .termios
%patch106 -p1 -b .glibc_compat
%patch107 -p0 -b .ls-colors
%patch108 -p0 -b .str-fmt

%build
%configure2_5x --bindir=/bin --without-hesiod
%make
nroff -me eight-bit.me > eight-bit.txt

%install
rm -rf %{buildroot}

install -Ds tcsh %{buildroot}/bin/tcsh
install -D tcsh.man %{buildroot}%{_mandir}/man1/tcsh.1

ln -s tcsh.1 %{buildroot}%{_mandir}/man1/csh.1
ln -sf tcsh %{buildroot}/bin/csh

install -D %{SOURCE1} %{buildroot}/etc/profile.d/$(basename %{SOURCE1})

%clean
rm -rf %{buildroot}

%post
/usr/share/rpm-helper/add-shell %{name} $1 /bin/csh
/usr/share/rpm-helper/add-shell %{name} $1 /bin/tcsh

%postun
/usr/share/rpm-helper/del-shell %{name} $1 /bin/csh
/usr/share/rpm-helper/del-shell %{name} $1 /bin/tcsh

%files
%defattr(644,root,root,755)
%doc NewThings FAQ Fixes eight-bit.txt complete.tcsh
%doc Ported README* WishList Y2K
%config(noreplace) %{_sysconfdir}/profile.d/*
%attr(755,root,root) /bin/*
%{_mandir}/*/*
