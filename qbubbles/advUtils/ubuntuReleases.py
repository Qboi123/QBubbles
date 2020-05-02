import urllib.request

from qbubbles.advUtils.code import HtmlCode
from qbubbles.advUtils.miscellaneous import remove_duplicates


class UbuntuRelease(object):
    def __init__(self, a, b, c, d):
        self.edition = a
        self.version = b
        self.type = c
        self.arch = d


class UbuntuReleases(object):
    def __init__(self, url: str = "http://releases.ubuntu.com"):
        self.url = url
        self._release_suffix = ""

    def get_releases(self):
        u = urllib.request.urlopen(f"{self.url}")
        html = u.read()
        code = HtmlCode(html)
        releases = code.find_links_by_regex("((\\d)*\\.\\d\\d\\.(\\d)*/)|((\\d)*\\.\\d\\d)/")
        return releases

    def get_isos(self, release):
        u2 = urllib.request.urlopen(f"{self.url}/{release}{self._release_suffix}")
        html2 = u2.read()
        code2 = HtmlCode(html2)
        print(f"All links in {release} are {code2.find_all_links()}")
        print(f"All http[s] links in {release} are {code2.find_all_links(http=True, https=True)}")

        isos_ = code2.find_links_by_regex("\\.iso$")
        isos = remove_duplicates(isos_.copy())

        r_isos = []
        import re
        for iso in isos:
            abc = re.search(
                "((?:(?:.*)(?:-(?:.*)).*)|(?:.*))-((?:(?:\\d)*\\.\\d\\d\\.(?:\\d)*)|(?:(?:\\d)*\\.\\d\\d))-((?:(?:.*)(?:-(?:.*))*)|(?:.*))(?:-(.*))\\.iso",
                iso)
            if abc is None:
                continue
            r_isos.append(UbuntuRelease(*abc.groups()))


class UbuntuMateReleases(UbuntuReleases):
    def __init__(self, url="http://cdimage.ubuntu.com/ubuntu-mate/releases"):
        super(UbuntuMateReleases, self).__init__(url)
        self._release_suffix = "/release"


class UbuntuBudgieReleases(UbuntuReleases):
    def __init__(self, url="http://cdimage.ubuntu.com/ubuntu-budgie/releases"):
        super(UbuntuBudgieReleases, self).__init__(url)
        self._release_suffix = "/release"


class UbuntuGnomeReleases(UbuntuReleases):
    def __init__(self, url="http://cdimage.ubuntu.com/ubuntu-gnome/releases"):
        super(UbuntuGnomeReleases, self).__init__(url)
        self._release_suffix = "/release"


class XubuntuReleases(UbuntuReleases):
    def __init__(self, url="http://cdimage.ubuntu.com/xubuntu/releases"):
        super(XubuntuReleases, self).__init__(url)
        self._release_suffix = "/release"


class KubuntuReleases(UbuntuReleases):
    def __init__(self, url="http://cdimage.ubuntu.com/kubuntu/releases"):
        super(KubuntuReleases, self).__init__(url)
        self._release_suffix = "/release"


class LubuntuReleases(UbuntuReleases):
    def __init__(self, url="http://cdimage.ubuntu.com/lubuntu/releases"):
        super(LubuntuReleases, self).__init__(url)
        self._release_suffix = "/release"


class MythbuntuReleases(UbuntuReleases):
    def __init__(self, url="http://cdimage.ubuntu.com/mythbuntu/releases"):
        super(MythbuntuReleases, self).__init__(url)
        self._release_suffix = "/release"


if __name__ == '__main__':
    ur = UbuntuReleases()
    print(f"Ubuntu:        {ur.get_releases()}")
    lur = LubuntuReleases()
    print(f"Lubuntu:       {lur.get_releases()}")
    kur = KubuntuReleases()
    print(f"Kubuntu:       {kur.get_releases()}")
    mur = MythbuntuReleases()
    print(f"Mythbuntu:     {mur.get_releases()}")
    xur = XubuntuReleases()
    print(f"Xubuntu:       {xur.get_releases()}")
    ubr = UbuntuBudgieReleases()
    print(f"Ubuntu Budgie: {ubr.get_releases()}")
    umr = UbuntuMateReleases()
    print(f"Ubunut MATE:   {umr.get_releases()}")
    ugr = UbuntuGnomeReleases()
    print(f"Ubuntu GNOME:  {ugr.get_releases()}")