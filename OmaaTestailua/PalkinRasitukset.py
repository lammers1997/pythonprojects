# yksiaukkoisen palkin, jossa tasainen kuorma,
# leikkausvoima- ja taivutusmomenttikuvaaja


from tkinter import *
from matplotlib import pyplot as plt
import math


class Rasituskuvio:

    def __init__(self):

        self.__window = Tk()
        self.__window.title("Yksiaukkoinen teräspalkki")

        # Palkin kuva
        self.__palkki_kuva = PhotoImage(file="palkki.gif")
        self.__label = Label(image=self.__palkki_kuva)
        self.__label.grid(column=0, row=0)

        # q =
        self.__label_info3 = Label(self.__window, text="Kuormitusyhdistelmä = ")
        self.__label_info3.grid(column=0, row=1, sticky=W)

        # kN/m
        self.__label_info4 = Label(self.__window, text="kN/m")
        self.__label_info4.grid(column=1, row=1, sticky=W)

        # Entry, johon käyttäjä syöttää tiedon palkin kuormasta
        self.__entry_unit1 = Entry(self.__window)
        self.__entry_unit1.grid(column=0, row=1, sticky=E)

        # L =
        self.__label_info = Label(self.__window, text="Palkin jänneväli = ")
        self.__label_info.grid(column=0, row=2, sticky=W)

        # Entry, johon syötetään palkin pituus
        self.__entry_unit = Entry(self.__window)
        self.__entry_unit.grid(column=0, row=2, sticky=E)

        # m
        self.__label_info2 = Label(self.__window, text="m")
        self.__label_info2.grid(column=1, row=2, sticky=W)

        # Leikkausvoima ja taivutusmomentti laskenta:
        self.__laske_rasitukset = Button(self.__window, text="Laske leikkausvoima ja taivutusmomentti",
                                         command=self.palkin_rasitukset)
        self.__laske_rasitukset.grid(column=0, row=3, sticky=W)

        # Leikkaus ja momenttikuvion piirtäminen:
        self.__draw_button = Button(self.__window, text="Piirrä kuvaajat",
                                    command=self.piirra_kuvaajat)
        self.__draw_button.grid(column=0, row=4)

        self.__label_result = Label(self.__window, text="")
        self.__label_result.grid(column=0, row=5)

        # Palkin lujuus (MPa)
        self.__lujuus_label = Label(self.__window, text="Materiaalin ominaislujuus: ")
        self.__lujuus_label.grid(column=0, row=6, sticky=W)
        self.__lujuus_entry = Entry(self.__window)
        self.__lujuus_entry.grid(column=0, row=6, sticky=E)

        # sallittu taipuma
        self.__entry_taipuma = Entry(self.__window)
        self.__entry_taipuma.grid(column=0, row=7, sticky=E)
        self.__label_taipuma = Label(self.__window, text="Palkin sallittu taipuma : L/")
        self.__label_taipuma.grid(column=0, row=7, sticky=W)

        # Minimikokoisen palkin laskenta varmuuskertoimella
        self.__laske_palkki = Button(self.__window, text="Määritä palkki",
                                     command=self.all_together)
        self.__laske_palkki.grid(column=0, row=8, sticky=E + W)

        # tulokset
        self.__label_result2 = Label(self.__window, text="")
        self.__label_result2.grid(column=0, row=9)

        # sopiva palkki
        self.__label_result3 = Label(self.__window, text="")
        self.__label_result3.grid(column=0, row=10)
        # poikkileikkausluokka
        self.__label_result6 = Label(self.__window, text="")
        self.__label_result6.grid(column=0, row=11)

        # Palkin taipuma
        self.__label_result4 = Label(self.__window, text="")
        self.__label_result4.grid(column=0, row=12)

        # palkin massa
        self.__label_result5 = Label(self.__window, text="")
        self.__label_result5.grid(column=0, row=13)

        # Taivutuskapasiteetti
        self.__label_taivutuskapasiteetti = Label(self.__window, text="")
        self.__label_taivutuskapasiteetti.grid(column=0, row=14)

    def all_together(self):
        self.palkin_rasitukset()
        self.pienin_palkki()
        self.poikkileikkausluokka()
        self.palkin_taipuma()
        self.taivutuskapasiteetti()
        self.massa()
        self.poikkileikkausluokka()

    def taivutuskapasiteetti(self):
        self.M_kapasiteetti = float(data[self.ipe].taivutusvastus) * float(self.__lujuus_entry.get()) / 1000000
        self.__label_taivutuskapasiteetti.configure(
            text="Palkin taivutuskapasiteetti = {:.1f} kNm".format(self.M_kapasiteetti))

    def poikkileikkausluokka(self):
        LUJUUS = float(self.__lujuus_entry.get())
        c = float(data[self.ipe].uuman_korkeus)
        t = float(data[self.ipe].paksuus)
        EPSILON = (235 / LUJUUS) ** (1 / 2)
        CT = c / t
        if CT <= 72 * EPSILON:
            self.__label_result6.configure(text="Poikkileikkausluokka 1")
        elif CT <= 83 * EPSILON:
            self.__label_result6.configure(text="Poikkileikkausluokka 2")
        elif CT <= 124 * EPSILON:
            self.__label_result6.configure(text="Poikkileikkausluokka 3")

    def massa(self):
        massa = float(data[self.ipe].massa) * float(self.__entry_unit.get())
        self.__label_result5.configure(text="Palkin massa: {:.1f}kg".format(massa))

    def pienin_palkki(self):
        """
        määrittää pienimmän sallitun taivutusvastuksen
        :return:
        """
        self.__pienin_taivutuslujuus = ((self.__max_taivutusmomentti * 1000000) * 1.15) / float(
            self.__lujuus_entry.get())
        self.__label_result2.configure(text="Pienin sallittu taivutuskestävyys: "
                                            "{:.2f} mm^3".format(self.__pienin_taivutuslujuus))

        for i in data:
            if float(self.__pienin_taivutuslujuus) < float(data[i].taivutusvastus):
                self.__label_result3.configure(text="Palkin valinta taivutuksen perusteella: IPE{:.0f}".format(i))
                self.ipe = i
                break

    def palkin_taipuma(self):
        q = float(self.__entry_unit1.get())
        L = float(self.__entry_unit.get())
        E = 210000
        v_max = (5 * q * (L * 1000) ** 4) / (384 * E * float(data[self.ipe].neliomomentti))
        self.__label_result4.configure(text="Palkin taipuma: {:.2f}mm".format(v_max))
        sallittu_taipuma = L * 1000 / float(self.__entry_taipuma.get())
        if v_max > sallittu_taipuma:
            for i in data:
                taipuma = (5 * q * (L * 1000) ** 4) / (384 * E * float(data[i].neliomomentti))
                if taipuma < sallittu_taipuma:
                    self.ipe = i
                    self.__label_result3.configure(text="Palkin valinta taipuman perusteella: IPE{:.0f}".format(i))
                    self.__label_result4.configure(text="Palkin taipuma: {:.2f}mm".format(taipuma))
                    break

    def palkin_rasitukset(self):
        """
        Laskee, ja piirtää leikkausvoimat ja taivutusmomentit
        :return:
        """
        q = float(self.__entry_unit1.get())
        L = float(self.__entry_unit.get())
        # tukireaktiot:
        A = float(q * L) / 2
        # rasitukset:
        self.__max_taivutusmomentti = (q * L ** 2) / 8
        self.__max_leikkausvoima = (q * L) / 2

        # tulosten esittäminen:
        self.__label_result.configure(
            text="max Q = {:.2f}kN ja max M_t {:.2f}kNm".format(self.__max_leikkausvoima, self.__max_taivutusmomentti))

    def piirra_kuvaajat(self):
        q = float(self.__entry_unit1.get())
        L = float(self.__entry_unit.get())
        A = float(q * L) / 2

        # kuvaajien piirtäminen:
        a = []
        b = []
        c = []
        d = []
        x = 0
        while x < L:
            y = A * x - q * x * x / 2
            Q = A - q * x
            a.append(x)
            b.append(y)
            c.append(0)
            d.append(Q)
            x += 0.01

        # taivutusmomentti:
        fig, (ax1, ax2) = plt.subplots(2, sharex=True, sharey=True)
        ax2.plot(a, b, color="black")
        ax2.plot(a, c, color="black")
        ax2.fill_between(a, b, facecolor="white", hatch="/")
        ax2.set(ylabel="Taivutusmomentti M_t")

        # leikkausvoima:
        ax1.plot(a, d, color="black")
        ax1.plot(a, c, color="black")
        ax1.fill_between(a, d, facecolor="white", hatch="/")
        ax1.set(ylabel="Leikkausvoima Q")
        plt.xlabel("Palkin pituus")

        plt.gca().invert_yaxis()
        plt.show()

    def start(self):
        """
        käynnistää ohjelman
        """
        self.__window.mainloop()

    def quit(self):
        """
        lopettaa ohjelman
        :return:
        """
        self.__window.quit()


class IPE:
    """
    Tallentaa IPE tiedot tekstitiedostosta
    """

    def __init__(self, korkeus, massa, neliomomentti, taivutusvastus, uuman_korkeus, paksuus):
        self.korkeus = korkeus
        self.massa = massa
        self.neliomomentti = neliomomentti
        self.taivutusvastus = taivutusvastus
        self.uuman_korkeus = uuman_korkeus
        self.paksuus = paksuus


data = {}


def read_file():
    try:
        tiedosto = open("IPE.txt", "r")
        rivilista = tiedosto.readlines()
        tiedosto.close()
        for rivi in rivilista:
            rivi = rivi.strip()
            rivi = rivi.split(";")
            data[int(rivi[0])] = IPE(rivi[0], rivi[1], rivi[2], rivi[3], rivi[4], rivi[5])

    except OSError:
        print("Tiedostoa ei voitu lukea")


def main():
    read_file()
    ui = Rasituskuvio()
    ui.start()


main()
