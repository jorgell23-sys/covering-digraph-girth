# El menor testigo de cada cintura para rad(n) | f(n)

*(English version: [README.md](README.md))*

Diecinueve números enteros, cada uno **demostradamente** el más chico de su
clase — cinco de ellos nunca calculados antes — y los teoremas chicos que hacen
posible demostrarlo **sin conocer ninguna respuesta de antemano**.

**Todo esto se comprueba en dos segundos:**

> **¿Es tu primera vez con esto? Empezá acá:** [**Explicación desde cero**](https://jorgell23-sys.github.io/covering-digraph-girth/es/) —
> todo contado con peras y manzanas, con dibujos y sin conocimientos previos.

```bash
git clone https://github.com/jorgell23-sys/covering-digraph-girth
cd covering-digraph-girth
python verify.py
```

Sin instalar nada. Corre 227 comprobaciones e imprime PASS o FAIL para cada una.

---

## De qué se trata, desde cero

Tomemos un número, digamos **234 = 2 × 3² × 13**, y dos funciones clásicas:

- **rad(n)** — el producto de sus primos distintos. `rad(234) = 2 × 3 × 13 = 78`.
- **sigma(n)** — la suma de todos sus divisores. `sigma(234) = 546`.

Y ahora dibujemos un grafo. Los **vértices** son los primos que dividen a `n`.
Hay una **flecha q → p** cuando `p` divide a `sigma(q^e)`, donde `q^e` es la
potencia exacta de `q` en `n`:

```
sigma(2)   = 3            →   flecha 2 → 3
sigma(3²)  = 13           →   flecha 3 → 13
sigma(13)  = 14 = 2 × 7   →   flecha 13 → 2
```

El grafo es un triángulo: `2 → 3 → 13 → 2`. Su ciclo más corto mide 3 — decimos
que su **cintura** es 3. Y 234 es el número más chico de su clase con cintura 3.

La pregunta que este trabajo responde: **¿cuál es el número más chico de
cintura k?**

El conjunto donde todo primo queda cubierto así no es nuevo: para `sigma` son
los *prime-abundant numbers* de Pollack y Pomerance (2012), catalogados en OEIS
como [A175200](https://oeis.org/A175200). Lo que se calcula acá es un invariante
de grafos sobre esa familia.

## Los resultados

| cintura | `sigma` | `sigma*` | `phi*` |
|---:|---:|---:|---:|
| 2 | 6 | 6 | 12 |
| 3 | 234 | 6615 | 66825 |
| 4 | 137214 | 4380453 | 1120454775 |
| 5 | 275900625 | 540765225 | **1663175056640625** |
| 6 | 180141399900 | 474549075 | |
| 7 | **7746928876851255** | 4485174218525 | |
| 8 | **31674203849435875** | **2386830845734335** | |
| 9 | | **9928651387877145** | |

Los cinco en negrita no habían sido calculados, y **los diecinueve son mínimos
demostrados**. El último es el caso interesante: no se conocía ningún testigo de
cintura 9 para `sigma*`, así que la versión 2 no podía calcularlo en absoluto.
La versión 3 saca la necesidad de conocer uno.

## La diferencia entre «el más chico que encontramos» y «el más chico»

La versión 1 decía, con honestidad, lo que no podía garantizar:

> *La respuesta es mínima sólo entre los primos examinados. Un primo más grande
> podría, en principio, dar un ciclo más barato.*

O sea que cada valor era una conjetura verificada hasta donde alguien miró.
Cerrar ese hueco cuesta un lema.

Sea `n` un menor testigo de cintura `k` y sea `P` su mayor primo. Su antecesor
en el ciclo aporta una potencia `q^e` con `P | f(q^e)`, así que `P ≤ f(q^e)`, y
las formas cerradas dan `q^e ≥ P/2` para `sigma`, `≥ P−1` para `sigma*` y
`≥ P+1` para `phi*`. Los `k−2` primos restantes son distintos, así que:

```
n  ≥  P · a_f(P) · (producto de los k−2 primos más chicos)
```

Leído al revés, eso es un **corte**: si se conoce cualquier testigo `N`, el menor
es a lo sumo `N`, así que su mayor primo no puede pasar de aproximadamente
`sqrt(N / primorial(k−2))`. Enumerar ciclos sobre los primos por debajo de eso
es exhaustivo, y la respuesta deja de depender de hasta dónde miró alguien.

Para `phi*` con cintura 5 el corte es **7 445 747**. Hubo que descartar todos los
primos por debajo de eso para poder decir que el mayor primo de la respuesta es
**23**.

## Arrancar sin conocer la respuesta

Ese corte está enunciado **en función de un testigo ya conocido**, así que la
versión 2 no podía tocar una cintura de la que nadie hubiera exhibido un
ejemplo. Lo decía de sí misma, y llamaba a hallar el primer testigo *«una
búsqueda heurística»*.

Era falso, y la versión 2 tenía el material para verlo. La búsqueda por debajo
de `N` es **exhaustiva**: no devuelve «el mejor que vi» sino «el menor que hay,
si hay alguno por debajo de `N`». Así que lo único que faltaba era un `N` de
arranque que no le debiera nada a una respuesta conocida. Un testigo de cintura
`k` tiene exactamente `k` primos distintos, así que su mayor primo es al menos
`p_k`, y la cota del corte crece con él:

```
n  ≥  p_k · a_f(p_k) · (producto de los k−2 primos más chicos)
```

Se arranca ahí, se duplica hasta que aparezca algo, y **lo primero que aparece
es el mínimo**: nada más chico está por debajo de este `N`, y nada en absoluto
estaba por debajo de los anteriores, que ya se barrieron. Duplicar es una
técnica vieja; lo que la vuelve una demostración acá es la exhaustividad que
tiene debajo.

```bash
python src/exact.py "sigma*" 9 --no-seed     # sin darle ningún testigo
```

No saber la respuesta cuesta un factor de alrededor de **4** en nodos visitados,
medido sobre los términos donde los dos métodos pueden correr. Se paga una sola
vez por cintura.

## Dónde termina, con un número

Los dos términos siguientes no salieron, y la versión 3 puede decir exactamente
por qué. La búsqueda barrió todo lo que hay por debajo de `1,24·10²¹` para `sigma`
con cintura 9 y por debajo de `1,3·10¹⁸` para `phi*` con cintura 6, y no encontró
nada: eso son teoremas. El constructor exhibe testigos en `8,3·10²⁴` y
`4,2·10²²`: eso está verificado, pero no es mínimo. Así que los dos términos
quedan **acorralados**, y cerrar el cerco exigiría cribar **5700 millones** y
**14 000 millones** de primos. Eso no entra en memoria.

Antes el límite era «hace falta un testigo conocido», que es una condición sobre
lo que otros hayan publicado. Ahora es un número de primos: una condición sobre
la máquina.

## Otra cosa que vale la pena mirar

Con `phi*`, cada mínimo **divide** al siguiente:

```
cintura 3:  3^5  → 11 → 5^2                 66825
cintura 4:  3^11 → 23 → 11 → 5^2            1120454775
cintura 5:  3^11 → 23 → 11 → 5^9 → 19       1663175056640625
```

Cada ciclo es el anterior con **un vértice insertado y un exponente subido**, y
de ahí sale la divisibilidad. El testigo exhibido de cintura 6 continúa la
cadena. **Predicción:** el mínimo verdadero de cintura 6 también será múltiplo de
`1663175056640625`. Lo refuta cualquier testigo más chico que no lo sea.

Y la lectura que parecía obvia —*el salto es chico cuando los dos testigos
comparten mucho*— es **falsa**: el salto más grande de los dieciséis pares
consecutivos es uno donde el término anterior divide al siguiente. `verify.py`
recalcula esa tabla.

La demostración, con sus límites, está en [RESULT.md](RESULT.md) (en inglés).

## Algo que vale la pena mirar

Entre la cintura 7 y la 8 con `sigma`, el menor testigo crece por un factor de
apenas **4,09** — después de haber crecido por un factor de **43 005** en el paso
anterior.

```
sigma, cintura 7:  3² · 5 · 7⁴ · 13 · 19 · 37 · 2801²
sigma, cintura 8:  5³ · 7² · 13² · 19 · 31² · 61 · 83 · 331
```

Con siete primos no se cierra ningún ciclo barato, y el mínimo está **obligado a
usar 2801²** — 7,8 millones sólo por ese factor. Con ocho primos disponibles, el
ciclo cierra sin pasar de 331. **El vértice de más sale casi gratis, y con él se
compra la salida del primo caro.**

Y eso importa más allá de la curiosidad: `ln n / k²` se queda entre 0,72 y 0,78
para `k = 4, 5, 6, 7`, lo que invita a leer `n ≈ exp(0,75 k²)` y predice
`n₈ ≈ 7 × 10²⁰`. El valor real es `3,2 × 10¹⁶`. **Cuatro términos sostenían una
ley y el quinto la rompió.**

## La sucesión que baja

Con `sigma*`, la sucesión de mínimos **baja** una vez:

```
6,  6615,  4380453,  540765225,  474549075,  4485174218525,  2386830845734335
                          ↑ más chico que el anterior
```

Los dos números comparten el esqueleto `3² × 5² × 11 × 13`, y toda la diferencia
está en un factor:

| | factor | valor |
|---|---|---:|
| cintura 6 | `7³ × 43` | **14749** |
| cintura 5 | `7⁵` | 16807 |

Cerrar el ciclo de 5 obliga a `7⁵`. Alargarlo a 6 deja entrar un primo nuevo, el
43, **y eso permite bajar el exponente a `7³`**. Agregar un vértice salió más
barato que subir un exponente.

Pasa una vez en ocho pares consecutivos. Lo que agrega la versión 2 es que el
mismo mecanismo funciona **sin** producir una bajada: en `sigma` de 7 a 8 sólo
aplana el crecimiento.

## Cómo está comprobado

Los tres métodos **no comparten ninguna lógica** — la criba no sabe nada de
ciclos, la construcción nunca mira un entero que no venga de uno, y la búsqueda
exacta no acepta nada sin recalcular la cintura desde el entero mismo — y
coinciden en todos los términos que más de uno alcanza.

Y hay un control externo: la criba cuenta **5327** elementos hasta 10⁹ sin
contar `n = 1`. Pollack y Pomerance publicaron **5328** contándolo. Coinciden
exactamente. Eso prueba este código contra un resultado con referato, calculado
por gente que nunca lo vio.

## Lo que este trabajo NO afirma

- **No afirma ser nuevo.** Se buscó en OEIS y en cuatro bases bibliográficas y
  no apareció — con un control positivo que sí encuentra los trabajos
  relevantes. *No encontrar no es lo mismo que no existir.* Está detallado en
  [PRIOR_ART.md](PRIOR_ART.md).
- **No afirma que las sucesiones sean infinitas.** Si existe testigo de toda
  cintura es otra pregunta, que no se toca acá.
- **No afirma minimalidad más allá de la tabla.** Ya no queda ningún obstáculo
  de principio —la búsqueda sin semilla saca la necesidad de un testigo de
  arranque— pero cada cintura de más cuesta tiempo de máquina, y sólo se afirman
  las cinturas efectivamente calculadas.
- **No afirma que duplicar sea la mejor forma de arrancar.** Es la más simple que
  conserva la demostración; una búsqueda por mejor-primero no repetiría trabajo.
- **No afirma que el crecimiento tenga una ley.** Afirma lo contrario, y el
  término nuevo agrega a la causa: `sigma*` crece por un factor de apenas
  **4,16** de la cintura 8 a la 9.
- **No afirma tener interés matemático.** Eso lo juzga quien lo lea.

## Autor

**Jorge Ellena Godoy**, responsable de la corrección de todo lo que hay acá.

## Cómo se produjo

El diseño del sistema y la dirección de la investigación son del autor. Los
resultados matemáticos los produjo un sistema automático (Claude, de Anthropic)
bajo esa dirección. Todos los cálculos se verificaron con implementaciones
independientes y se cruzaron contra trabajo publicado. El autor responde por la
corrección de todo lo que hay acá.

## Licencia

Código bajo [MIT](LICENSE); texto y datos bajo
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
