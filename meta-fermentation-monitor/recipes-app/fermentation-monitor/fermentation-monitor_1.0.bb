SUMMARY = "Fermentation Monitor Application"
DESCRIPTION = "C++/Python application for monitoring dough fermentation"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

SRC_URI = "file://src"

S = "${WORKDIR}/src"

DEPENDS = "opencv python3 python3-flask python3-opencv"
RDEPENDS:${PN} = "python3 python3-flask python3-opencv python3-numpy"

inherit cmake systemd

SYSTEMD_SERVICE:${PN} = "fermentation-monitor.service"

do_install:append() {
    install -d ${D}${systemd_unitdir}/system
    install -m 0644 ${WORKDIR}/src/systemd/fermentation-monitor.service ${D}${systemd_unitdir}/system/
    
    install -d ${D}/opt/fermentation-monitor
    cp -r ${WORKDIR}/src/web ${D}/opt/fermentation-monitor/
    cp -r ${WORKDIR}/src/python ${D}/opt/fermentation-monitor/
}