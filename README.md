Zypper random generator
===

# Inhoudsopgave
- [Introductie](#introductie)
    - [Toelichting Birthday Spacing test](#toelichting-birthday-spacing-test)
    - [Uitvoering](#uitvoering)
    - [Interpretatie van resultaten](#interpretatie-van-resultaten)
- [Quickstart (linux / MacOS)](#quickstart--linux--macos-)


## Introductie 

Bij [Zypper](https://www.zypper.app) gebruiken we de [`numpy`](https://numpy.org/doc/stable/reference/random/generator.html) random generator om de start euro te bepalen. De random generator algoritme die wordt gebruikt is [`PCG-64`](https://numpy.org/doc/stable/reference/random/bit_generators/pcg64.html#numpy.random.PCG64) en is een modern en statistisch bewezen algoritme voor het genereren van random getallen.

In deze repository bewijzen we door middel van de [`Birthday Spacing Test`](https://en.wikipedia.org/wiki/Diehard_tests) de randomness van de `numpy` random generator die wordt gebruikt binnen Zypper.

<img src="dist.png" alt="dist image" width="800"/>
<br><br>

###  Toelichting Birthday Spacing test
Het doel van dit script is om de willekeurigheid van de random number generator van `numpy` te valideren. We doen dit 
met een **Birthday Spacing Test**. In deze test onderzoeken we de afstanden tussen willekeurig gegenereerde getallen en 
bepalen we of deze afstanden een exponentiële verdeling volgen, zoals verwacht van een willekeurig proces.


- **Inputs**:
  - `n_numbers`: Aantal te genereren willekeurige getallen
  - `range_interval`: Bereik waarbinnen de willekeurige getallen worden gegenereerd

- **output**:
  - Genereert willekeurige getallen uniform verdeeld binnen het gegeven bereik.
  - Berekent de afstanden tussen deze getallen door ze te sorteren en de verschillen te berekenen.
  - Fit de waargenomen afstanden aan een exponentiële verdeling om de distributieparameters te verkrijgen.
  - Vergelijkt de waargenomen afstanden met een theoretische exponentiële verdeling met behulp van de Kolmogorov-Smirnov (KS) test.
  - Geeft de KS-statistiek en p-waarde weer en neemt een beslissing op basis van de p-waarde.

### Uitvoering

Bij uitvoering toont het script het volgende:

1. Een plot die de empirische verdeling van afstanden vergelijkt met de theoretische exponentiële verdeling.
2. Toont de Kolmogorov-Smirnov statistiek en p-waarde.
3. Maakt een beslissing over of de willekeurige getallen gegenereerd door `numpy` als echt willekeurig kunnen worden beschouwd op basis van de p-waarde.

### Interpretatie van resultaten

- **Als de p-waarde groter is dan 0,05**: Dit suggereert dat de afstanden tussen willekeurige getallen gegenereerd door `numpy` uniform zijn verdeeld, wat impliceert dat de random generator in `numpy` werkt zoals verwacht.
  
- **Als de p-waarde kleiner is dan of gelijk aan 0,05**: De afstanden lijken niet uniform verdeeld te zijn, wat suggereert dat de random generator mogelijk niet echt willekeurig is.

---

# Quickstart (linux / MacOS)

1. Maak een virtual env aan:

```
python -m venv venv && source venv/bin/activate
```

2. Installeer de nodige packages

```
pip install -r requirements.txt
```

3. Run de test

```python
python main.py
```
