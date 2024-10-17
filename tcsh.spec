# Workaround to build with GCC 10
%global optflags %{optflags} -fcommon

Summary:	An enhanced version of csh, the C shell
Name:		tcsh
Version:	6.24.13
Release:	1
License:	BSD
Group:		Shells
URL:		https://www.tcsh.org/
Source0:	ftp://ftp.astron.com/pub/%{name}/%{name}-%{version}.tar.gz

Source1:	alias.csh
# patches from fedora
Patch12:	tcsh-6.20.00-tinfo.patch

# our patches
Patch106:	tcsh-6.10.00-glibc_compat.patch

BuildRequires:	pkgconfig(ncurses)
BuildRequires:	groff-for-man
Requires(post):	rpm-helper >= 0.7
Requires(postun):	rpm-helper >= 0.7
Provides:	csh = %{version}
Provides:	/bin/csh
Provides:	/bin/tcsh

%description
Tcsh is an enhanced but completely compatible version of csh, the C
shell. Tcsh is a command language interpreter which can be used both
as an interactive login shell and as a shell script command processor.
Tcsh includes a command line editor, programmable word completion,
spelling correction, a history mechanism, job control and a C language
like syntax.

%prep
%autosetup -p0

%build
%configure --without-hesiod
%make
nroff -me eight-bit.me > eight-bit.txt

%install
install -D tcsh %{buildroot}%{_bindir}/tcsh
install -D tcsh.man %{buildroot}%{_mandir}/man1/tcsh.1

ln -s tcsh.1 %{buildroot}%{_mandir}/man1/csh.1
ln -sf tcsh %{buildroot}%{_bindir}/csh

install -D %{SOURCE1} %{buildroot}/etc/profile.d/$(basename %{SOURCE1})

%post
%_add_shell_helper %{name} $1 %{_bindir}/csh
%_add_shell_helper %{name} $1 %{_bindir}/tcsh

%postun
%_del_shell_helper %{name} $1 %{_bindir}/csh
%_del_shell_helper %{name} $1 %{_bindir}/tcsh

%files
%defattr(644,root,root,755)
%doc FAQ Fixes eight-bit.txt complete.tcsh
%doc Ported README* WishList Y2K
%config(noreplace) %{_sysconfdir}/profile.d/*
%attr(755,root,root) %{_bindir}/*
%{_mandir}/*/*
