#
# note to self: Linus releases need to be named 5.x.0 not 5.x or various
# things break
#
#

%define xm_customver 1

Name:           linux-xmlts-default
Version:        6.1.57
Release:        107
License:        GPL-2.0
Summary:        The Linux kernel
Url:            http://www.kernel.org/
Group:          kernel
Source0:        https://github.com/xanmod/linux/archive/refs/tags/%{version}-xanmod%{xm_customver}.tar.gz
Source1:        config
Source2:        cmdline

%define ktarget  xmlts-default
%define kversion %{version}-%{release}.%{ktarget}

#BuildRequires:  buildreq-kernel

Requires: systemd-bin
Requires: init-rdahead-extras
Requires: linux-xmlts-default-license = %{version}-%{release}

# don't strip .ko files!
%global __os_install_post %{nil}
%define debug_package %{nil}
%define __strip /bin/true

#cve.start cve patches from 0001 to 050
#cve.end

#mainline: Mainline patches, upstream backport and fixes from 0051 to 0099
#mainline.end

# Clear patches commented out or not patched in Clear's 6.1 spec file.
# 0113-print-fsync-count-for-bootchart.patch
# 0118-add-scheduler-turbo3-patch.patch
# 0132-prezero-20220308.patch
# 0200-mm-lru_cache_disable-use-synchronize_rcu_expedited.patch

# Clear patches omitted, due to inclusion in the XanMod kernel.
# 0103-silence-rapl.patch
# 0109-initialize-ata-before-graphics.patch
# 0112-init-wait-for-partition-and-retry-scan.patch
# 0115-enable-stateless-firmware-loading.patch
# 0119-use-lfence-instead-of-rep-and-nop.patch
# 0120-do-accept-in-LIFO-order-for-cache-efficiency.patch
# 0121-locking-rwsem-spin-faster.patch
# 0401-sched-hybrid1.patch (XanMod applied sched-hybrid variations)
# 0402-sched-hybrid2.patch
# 0403-sched-hybrid3.patch
# 0404-sched-hybrid4.patch

# Clear patches omitted, due to removal in the XanMod kernel.
# 0001-sched-migrate.patch (reverted in 6.1.57)
# 0002-sched-migrate.patch (reverted in 6.1.57, SIS_CURRENT feature)

#Serie.clr 01XX: Clear Linux patches
Patch0101: 0101-i8042-decrease-debug-message-level-to-info.patch
Patch0102: 0102-increase-the-ext4-default-commit-age.patch
Patch0104: 0104-pci-pme-wakeups.patch
Patch0105: 0105-ksm-wakeups.patch
Patch0106: 0106-intel_idle-tweak-cpuidle-cstates.patch
Patch0107: 0107-bootstats-add-printk-s-to-measure-boot-time-in-more-.patch
Patch0108: 0108-smpboot-reuse-timer-calibration.patch
Patch0111: 0111-ipv4-tcp-allow-the-memory-tuning-for-tcp-to-go-a-lit.patch
Patch0114: 0114-add-boot-option-to-allow-unsigned-modules.patch
Patch0116: 0116-migrate-some-systemd-defaults-to-the-kernel-defaults.patch
Patch0117: 0117-xattr-allow-setting-user.-attributes-on-symlinks-by-.patch
Patch0122: 0122-ata-libahci-ignore-staggered-spin-up.patch
Patch0123: 0123-print-CPU-that-faults.patch
Patch0124: 0124-x86-microcode-Add-an-option-to-reload-microcode-even.patch
Patch0125: 0125-nvme-workaround.patch
Patch0126: 0126-don-t-report-an-error-if-PowerClamp-run-on-other-CPU.patch
Patch0127: 0127-lib-raid6-add-patch.patch
Patch0128: 0128-itmt_epb-use-epb-to-scale-itmt.patch
Patch0130: 0130-itmt2-ADL-fixes.patch
Patch0131: 0131-add-a-per-cpu-minimum-high-watermark-an-tune-batch-s.patch
Patch0133: 0133-xm-novector.patch
Patch0134: 0134-md-raid6-algorithms-scale-test-duration-for-speedier.patch
Patch0135: 0135-initcall-only-print-non-zero-initcall-debug-to-speed.patch
Patch0136: scale.patch
Patch0137: libsgrowdown.patch
Patch0138: kdf-boottime.patch
Patch0139: adlrdt.patch
Patch0140: kvm-printk.patch
Patch0141: epp-retune.patch
Patch0142: tcptuning.patch
Patch0143: 0001-powerbump-functionality.patch
Patch0144: 0002-add-networking-support-for-powerbump.patch
Patch0145: 0003-futex-bump.patch
Patch0146: 0001-add-umonitor-umwait-C0.x-C-states.patch
Patch0147: 0001-mm-memcontrol-add-some-branch-hints-based-on-gcov-an.patch
Patch0148: 0002-sched-core-add-some-branch-hints-based-on-gcov-analy.patch
Patch0149: netscale.patch
Patch0162: 0162-xm-extra-optmization-flags.patch
#Serie.end

%description
The Linux kernel.

%package extra
License:        GPL-2.0
Summary:        The Linux kernel extra files
Group:          kernel
Requires:       linux-xmlts-default-license = %{version}-%{release}

%description extra
Linux kernel extra files

%package license
Summary: license components for the linux package.
Group: Default

%description license
license components for the linux package.

%package cpio
License:        GPL-2.0
Summary:        cpio file with kernel modules
Group:          kernel

%description cpio
Creates a cpio file with some modules

%package dev
License:        GPL-2.0
Summary:        The Linux kernel
Group:          kernel
Requires:       linux-xmlts-default = %{version}-%{release}
Requires:       linux-xmlts-default-extra = %{version}-%{release}
Requires:       linux-xmlts-default-license = %{version}-%{release}

%description dev
Linux kernel build files

%prep
%setup -q -n linux-%{version}-xanmod%{xm_customver}

#cve.patch.start cve patches
#cve.patch.end

#mainline.patch.start Mainline patches, upstream backport and fixes
#mainline.patch.end

#Serie.patch.start Clear Linux patches
%patch -P 101 -p1
%patch -P 102 -p1
%patch -P 104 -p1
%patch -P 105 -p1
%patch -P 106 -p1
%patch -P 107 -p1
%patch -P 108 -p1
%patch -P 111 -p1
%patch -P 114 -p1
%patch -P 116 -p1
%patch -P 117 -p1
%patch -P 122 -p1
%patch -P 123 -p1
%patch -P 124 -p1
%patch -P 125 -p1
%patch -P 126 -p1
%patch -P 127 -p1
%patch -P 128 -p1
%patch -P 130 -p1
%patch -P 131 -p1
%patch -P 133 -p1
%patch -P 134 -p1
%patch -P 135 -p1
%patch -P 136 -p1
%patch -P 137 -p1
%patch -P 138 -p1
%patch -P 139 -p1
%patch -P 140 -p1
%patch -P 141 -p1
%patch -P 142 -p1
%patch -P 143 -p1
%patch -P 144 -p1
%patch -P 145 -p1
%patch -P 146 -p1
%patch -P 147 -p1
%patch -P 148 -p1
%patch -P 149 -p1
%patch -P 162 -p1
#Serie.patch.end


cp %{SOURCE1} .config

# Run equally well on all x86-64 CPUs with min support of Haswell.
scripts/config -d MCORE2
scripts/config -e MHASWELL

# Disable debug.
%if 1
scripts/config -d DEBUG_INFO
scripts/config -d DEBUG_INFO_BTF
scripts/config -d DEBUG_INFO_BTF_MODULES
scripts/config -d DEBUG_INFO_DWARF_TOOLCHAIN_DEFAULT
scripts/config -d DEBUG_INFO_DWARF4
scripts/config -d DEBUG_INFO_DWARF5
scripts/config -d PAHOLE_HAS_SPLIT_BTF
scripts/config -d SLUB_DEBUG
scripts/config -d PM_DEBUG
scripts/config -d PM_ADVANCED_DEBUG
scripts/config -d PM_SLEEP_DEBUG
scripts/config -d ACPI_DEBUG
scripts/config -d LATENCYTOP
scripts/config -d DEBUG_PREEMPT
%endif

# Disable tracers, XanMod default.
scripts/config -d DMA_FENCE_TRACE
scripts/config -d DRM_I915_LOW_LEVEL_TRACEPOINTS
scripts/config -d RCU_TRACE
scripts/config -d FTRACE

# Enable FQ-PIE Packet Scheduling.
# https://datatracker.ietf.org/doc/html/rfc8033
scripts/config -e NET_SCH_PIE
scripts/config -e NET_SCH_FQ_PIE
scripts/config -e NET_SCH_DEFAULT
scripts/config -e DEFAULT_FQ_PIE

# Enable NTFS3 file-system driver.
# NTFS3 is a kernel NTFS implementation, which offers much faster performance
# than the NTFS-3G FUSE based implementation. Note: ntfs3 requires the file
# system type to mount. e.g. mount -t ntfs3 /dev/sdxY /mnt
# https://www.paragon-software.com/home/ntfs3-driver-faq/
# https://wiki.archlinux.org/title/NTFS
scripts/config -m NTFS3_FS
scripts/config -e NTFS3_LZX_XPRESS
scripts/config -e NTFS3_FS_POSIX_ACL

# Enable Google's BBRv3 (Bottleneck Bandwidth and RTT) TCP congestion control.
# Enable Futex WAIT_MULTIPLE implementation for Wine / Proton Fsync.
# Clear and XanMod defaults.
scripts/config -e TCP_CONG_BBR
scripts/config -e DEFAULT_BBR
scripts/config -e FUTEX
scripts/config -e FUTEX_PI

# Enable WINESYNC driver for fast kernel-backed Wine.
scripts/config -m WINESYNC

# Offload RCU callback processing from boot-selected CPUs.
# Clear defaults.
scripts/config -e RCU_EXPERT
scripts/config -e RCU_NOCB_CPU
scripts/config -e RCU_NOCB_CPU_DEFAULT_ALL

# Disable RCU expedited work in a real-time kthread.
# CachyOS default.
scripts/config -d RCU_EXP_KTHREAD

# To save power, batch RCU callbacks and then flush them after a timed delay,
# memory pressure, or callback list growing too big (can provide 5-10% power-
# savings for idle or lightly-loaded systems, this is beneficial for laptops).
# https://lore.kernel.org/lkml/20221016162305.2489629-3-joel@joelfernandes.org/
# CachyOS and Ubuntu low-latency default.
scripts/config -e RCU_LAZY

mv .config config

%build
BuildKernel() {

    Target=$1
    Arch=x86_64
    ExtraVer="-%{release}.${Target}"

    rm -f localversion

    perl -p -i -e "s/^EXTRAVERSION.*/EXTRAVERSION = ${ExtraVer}/" Makefile

    make O=${Target} -s mrproper
    cp config ${Target}/.config

    make O=${Target} -s ARCH=${Arch} olddefconfig
    make O=${Target} -s ARCH=${Arch} CONFIG_DEBUG_SECTION_MISMATCH=y %{?_smp_mflags} %{?sparse_mflags}
}

BuildKernel %{ktarget}

%install

InstallKernel() {

    Target=$1
    Kversion=$2
    Arch=x86_64
    KernelDir=%{buildroot}/usr/lib/kernel
    DevDir=%{buildroot}/usr/lib/modules/${Kversion}/build

    mkdir   -p ${KernelDir}
    install -m 644 ${Target}/.config    ${KernelDir}/config-${Kversion}
    install -m 644 ${Target}/System.map ${KernelDir}/System.map-${Kversion}
    install -m 644 ${Target}/vmlinux    ${KernelDir}/vmlinux-${Kversion}
    install -m 644 %{SOURCE2}           ${KernelDir}/cmdline-${Kversion}
    cp  ${Target}/arch/x86/boot/bzImage ${KernelDir}/org.clearlinux.${Target}.%{version}-%{release}
    chmod 755 ${KernelDir}/org.clearlinux.${Target}.%{version}-%{release}

    mkdir -p %{buildroot}/usr/lib/modules
    make O=${Target} -s ARCH=${Arch} INSTALL_MOD_PATH=%{buildroot}/usr modules_install

    rm -f %{buildroot}/usr/lib/modules/${Kversion}/build
    rm -f %{buildroot}/usr/lib/modules/${Kversion}/source

    mkdir -p ${DevDir}
    find . -type f -a '(' -name 'Makefile*' -o -name 'Kbuild*' -o -name 'Kconfig*' ')' -exec cp -t ${DevDir} --parents -pr {} +
    find . -type f -a '(' -name '*.sh' -o -name '*.pl' ')' -exec cp -t ${DevDir} --parents -pr {} +
    cp -t ${DevDir} -pr ${Target}/{Module.symvers,tools}
    ln -s ../../../kernel/config-${Kversion} ${DevDir}/.config
    ln -s ../../../kernel/System.map-${Kversion} ${DevDir}/System.map
    cp -t ${DevDir} --parents -pr arch/x86/include
    cp -t ${DevDir}/arch/x86/include -pr ${Target}/arch/x86/include/*
    cp -t ${DevDir}/include -pr include/*
    cp -t ${DevDir}/include -pr ${Target}/include/*
    cp -t ${DevDir} --parents -pr scripts/*
    cp -t ${DevDir}/scripts -pr ${Target}/scripts/*
    find  ${DevDir}/scripts -type f -name '*.[cho]' -exec rm -v {} +
    find  ${DevDir} -type f -name '*.cmd' -exec rm -v {} +
    # Cleanup any dangling links
    find ${DevDir} -type l -follow -exec rm -v {} +

    # Kernel default target link
    ln -s org.clearlinux.${Target}.%{version}-%{release} %{buildroot}/usr/lib/kernel/default-${Target}
}

# cpio file for keyboard drivers
createCPIO() {

    Target=$1
    Kversion=$2
    KernelDir=%{buildroot}/usr/lib/kernel
    ModDir=/usr/lib/modules/${Kversion}

    mkdir -p cpiofile${ModDir}/kernel/drivers/input/{serio,keyboard}
    mkdir -p cpiofile${ModDir}/kernel/drivers/hid
    cp %{buildroot}${ModDir}/kernel/drivers/input/serio/i8042.ko      cpiofile${ModDir}/kernel/drivers/input/serio
    cp %{buildroot}${ModDir}/kernel/drivers/input/serio/libps2.ko     cpiofile${ModDir}/kernel/drivers/input/serio
    cp %{buildroot}${ModDir}/kernel/drivers/input/keyboard/atkbd.ko   cpiofile${ModDir}/kernel/drivers/input/keyboard
    cp %{buildroot}${ModDir}/kernel/drivers/hid/hid-logitech-dj.ko    cpiofile${ModDir}/kernel/drivers/hid
    cp %{buildroot}${ModDir}/kernel/drivers/hid/hid-logitech-hidpp.ko cpiofile${ModDir}/kernel/drivers/hid
    cp %{buildroot}${ModDir}/kernel/drivers/hid/hid-apple.ko          cpiofile${ModDir}/kernel/drivers/hid
    cp %{buildroot}${ModDir}/modules.order   cpiofile${ModDir}
    cp %{buildroot}${ModDir}/modules.builtin cpiofile${ModDir}

    depmod -b cpiofile/usr ${Kversion}

    (
      cd cpiofile
      find . | cpio --create --format=newc \
        | xz --check=crc32 --lzma2=dict=512KiB > ${KernelDir}/initrd-org.clearlinux.${Target}.%{version}-%{release}
    )
}

InstallKernel %{ktarget} %{kversion}

createCPIO %{ktarget} %{kversion}

rm -rf %{buildroot}/usr/lib/firmware

mkdir -p %{buildroot}/usr/share/package-licenses/linux-xmlts-default
cp COPYING %{buildroot}/usr/share/package-licenses/linux-xmlts-default/COPYING
cp -a LICENSES/* %{buildroot}/usr/share/package-licenses/linux-xmlts-default

%postun
rm -fr /var/lib/dkms/*/kernel-%{kversion}-x86_64
rm -fr /var/lib/dkms/*/*/%{kversion}

%files
%dir /usr/lib/kernel
%dir /usr/lib/modules/%{kversion}
/usr/lib/kernel/config-%{kversion}
/usr/lib/kernel/cmdline-%{kversion}
/usr/lib/kernel/org.clearlinux.%{ktarget}.%{version}-%{release}
/usr/lib/kernel/default-%{ktarget}
/usr/lib/modules/%{kversion}/kernel
/usr/lib/modules/%{kversion}/modules.*

%files extra
%dir /usr/lib/kernel
/usr/lib/kernel/System.map-%{kversion}
/usr/lib/kernel/vmlinux-%{kversion}

%files license
%defattr(0644,root,root,0755)
/usr/share/package-licenses/linux-xmlts-default

%files cpio
/usr/lib/kernel/initrd-org.clearlinux.%{ktarget}.%{version}-%{release}

%files dev
%defattr(-,root,root)
/usr/lib/modules/%{kversion}/build
