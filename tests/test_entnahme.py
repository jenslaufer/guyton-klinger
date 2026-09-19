"""Die Leitplanken greifen in drei Richtungen — jede bekommt ihren Fall."""

import unittest

from entnahme import naechste_entnahme

# Jens' Ausgangslage: 36.000 EUR auf 1.000.000 EUR = 3,60 % Startrate,
# Leitplanken +/- 20 % => Kuerzung ueber 4,32 %, Erhoehung unter 2,88 %.
STARTRATE = 36000.0 / 1000000.0
OBEN = STARTRATE * 1.20
UNTEN = STARTRATE * 0.80
SCHRITT = 0.10


class LeitplankenTest(unittest.TestCase):
    def test_zwischen_den_leitplanken_nur_inflation(self):
        # Depot steigt auf 1.020.000, Inflation 2 %: 36.720 / 1.020.000 = 3,60 %.
        entnahme, regel = naechste_entnahme(36000.0, 1020000.0, 0.02, OBEN, UNTEN, SCHRITT)

        self.assertEqual(regel, "standard")
        self.assertAlmostEqual(entnahme, 36720.0, places=2)

    def test_obere_leitplanke_kuerzt(self):
        # Depot faellt auf 800.000: 36.720 / 800.000 = 4,59 % > 4,32 %.
        entnahme, regel = naechste_entnahme(36000.0, 800000.0, 0.02, OBEN, UNTEN, SCHRITT)

        self.assertEqual(regel, "oben")
        self.assertAlmostEqual(entnahme, 33048.0, places=2)

    def test_untere_leitplanke_erhoeht(self):
        # Depot steigt auf 1.400.000: 36.720 / 1.400.000 = 2,62 % < 2,88 %.
        entnahme, regel = naechste_entnahme(36000.0, 1400000.0, 0.02, OBEN, UNTEN, SCHRITT)

        self.assertEqual(regel, "unten")
        self.assertAlmostEqual(entnahme, 40392.0, places=2)

    def test_genau_auf_der_oberen_leitplanke_wird_nicht_gekuerzt(self):
        # Die Schwelle selbst gehoert noch zum Normalfall (strikt groesser).
        # Depotwert so gewaehlt, dass die Rate exakt die Schwelle trifft.
        depot = (36000.0 * 1.02) / OBEN

        entnahme, regel = naechste_entnahme(36000.0, depot, 0.02, OBEN, UNTEN, SCHRITT)

        self.assertEqual(regel, "standard")
        self.assertAlmostEqual(entnahme, 36720.0, places=2)

    def test_kuerzung_wirkt_auf_die_inflationsangepasste_zahl(self):
        # Reihenfolge ist die halbe Strategie: erst Inflation, dann Abschlag.
        # Andersherum waeren es 36.000 * 0,9 * 1,02 = 33.048 -- zufaellig gleich,
        # darum hier mit einem Schritt, der die Reihenfolge sichtbar macht.
        entnahme, _ = naechste_entnahme(36000.0, 800000.0, 0.05, OBEN, UNTEN, 0.20)

        self.assertAlmostEqual(entnahme, 36000.0 * 1.05 * 0.80, places=2)

    def test_null_inflation_laesst_die_entnahme_stehen(self):
        entnahme, regel = naechste_entnahme(36000.0, 1000000.0, 0.0, OBEN, UNTEN, SCHRITT)

        self.assertEqual(regel, "standard")
        self.assertAlmostEqual(entnahme, 36000.0, places=2)


if __name__ == "__main__":
    unittest.main()
