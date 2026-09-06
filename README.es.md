# Menores testigos por cintura para `rad(n) | f(n)`

<!-- hallazgo:que -->
## Qué se encontró

Dada una función multiplicativa `f` y un entero `n`, se traza una flecha
`q -> p` entre primos que dividen a `n` cuando `p | f(q^e)`, con `q^e` la
potencia exacta de `q` en `n`. Restringiendo a los `n` en que **todo primo
recibe flecha**, ese dibujo siempre contiene un ciclo dirigido, y el largo del
más corto es un invariante de `n`.

Este repositorio calcula **el menor `n` cuyo ciclo más corto tiene largo `k`**,
para once funciones y `k = 2, ..., 10`: **52 valores, cada uno demostradamente
mínimo**, 38 de ellos calculados acá por primera vez. Demuestra además una
operación local sobre el ciclo que da una cota superior para el valor siguiente,
y un **certificado** derivado de ella que decide `m_f(k+1) < m_f(k)` **sin
calcular** `m_f(k+1)`. El certificado resulta **suficiente y no necesario**.

<!-- hallazgo:enunciado -->
## Definiciones y enunciados

Sea `f` multiplicativa y **local**, es decir que `q` nunca divide a `f(q^e)`.
Se escribe `rad(n)` para el producto de los primos distintos de `n` y

    S(f) = { n >= 1 : rad(n) divide a f(n) }.

Para `n = prod q_j^{e_j}` en `S(f)`, el **digrafo de cubrimiento** `D_f(n)`
tiene por vértices los primos de `n` y una flecha `q_i -> q_j` (`i != j`) cuando
`q_j | f(q_i^{e_i})`. Pertenecer a `S(f)` equivale a que todo vértice tenga
flecha entrante, así que `D_f(n)` siempre contiene un ciclo dirigido. Su
**cintura** `g_f(n)` es el largo del más corto, y

    m_f(k) = min { n en S(f) : g_f(n) = k }.

Las once funciones son `sigma`, `sigma*` (unitaria), `phi*` (totiente unitaria),
`sigma**` (biunitaria) y las familias con parámetro

    sigma_s(q^e)  = (q^{s(e+1)} - 1)/(q^s - 1),    sigma*_s(q^e) = q^{se} + 1,
    phi*_s(q^e)   = q^{se} - 1,                    para s = 3, 4, 5, 6.

> **Teorema 1 (forma de un mínimo).** `m_f(k)` tiene exactamente `k` primos
> distintos, y `D_f(m_f(k))` es un ciclo puro de largo `k`.

> **Teorema 2 (lema de corte).** Sea `n` un testigo de cintura `k` y `P` su mayor
> primo, y sea `a_f(P)` la menor potencia de primo `m` con `P | f(m)`. Entonces
>
>     n  >=  P * a_f(P) * primorial(k-2).
>
> En consecuencia, exhibido un testigo `N` de cintura `k`, el mayor primo de
> `m_f(k)` queda acotado por el mayor `P` para el que la desigualdad todavía
> admite `n < N`. La enumeración por debajo de esa cota es exhaustiva, así que
> una búsqueda que no encuentra nada **demuestra** que no hay nada.

> **Teorema 3 (cirugía).** Sea `n` un testigo de cintura `k` cuyo digrafo es el
> ciclo puro `q_1 -> ... -> q_k -> q_1`, sea `p` un primo fuera de él y sean
> `e', a >= 1` tales que, para algún índice `i`:
>
> 1. `p | f(q_i^{e'})`;
> 2. `q_{i+1} | f(p^a)`;
> 3. `q_j` no divide a `f(q_i^{e'})` para todo `j != i`;
> 4. `q_j` no divide a `f(p^a)` para todo `j != i+1`;
> 5. `p` no divide a `f(q_j^{e_j})` para todo `j != i`.
>
> Entonces `n' = n * q_i^{e'-e_i} * p^a` es un testigo de cintura `k+1`, y por lo
> tanto
>
>     m_f(k+1)  <=  m_f(k) * q_i^{e'-e_i} * p^a.
>
> **Corolario (certificado).** Si además `q_i^{e'} * p^a < q_i^{e_i}`, entonces
> `m_f(k+1) < m_f(k)`. Decidirlo es una búsqueda finita que nunca enumera primos:
> la desigualdad obliga `e' < e_i`, así que `e'` recorre `1..e_i-1`, `p` recorre
> los divisores primos de `f(q_i^{e'})` y `a` los exponentes con
> `p^a < q_i^{e_i-e'}`.

> **Teorema 4 (el certificado no es necesario).** Para todo `k >= 2` y todo
> `C > 0` existe `f` multiplicativa y local con `m_f(k+1) < m_f(k)/C`, con
> `m_f(k)` libre de cuadrados —de modo que ningún certificado puede dispararse—
> y con los ciclos de `m_f(k)` y `m_f(k+1)` **disjuntos**.

<!-- hallazgo:ejemplo -->
## El caso más chico, hecho a mano

Sea `n = 234 = 2 * 3^2 * 13` y `f = sigma`:

    sigma(2)   = 3            ->   2 -> 3
    sigma(3^2) = 13           ->   3 -> 13
    sigma(13)  = 14 = 2 * 7   ->   13 -> 2

Todo primo recibe flecha, así que `234` está en `S(sigma)`, y las flechas forman
el triángulo `2 -> 3 -> 13 -> 2`: cintura 3. El Teorema 2 aplicado con el testigo
`N = 234` acota por 13 el mayor primo de cualquier testigo menor; enumerados esos
casos no queda ninguno. Luego `m_sigma(3) = 234` es un mínimo, no un récord.

Para el certificado, con `f = sigma*`, donde `sigma*(q^e) = q^e + 1`, y

    m_{sigma*}(5) = 540765225 = 3^2 * 5^2 * 7^5 * 11 * 13,

se baja `7^5` a `7^3` y se inserta el primo `43`. Las condiciones 1–5 se cumplen
y `7^3 * 43 < 7^5` porque `43 < 49`. Por lo tanto
`m_{sigma*}(6) < m_{sigma*}(5)`, sabido antes de calcularlo. El testigo que
devuelve la construcción, `474549075 = 3^2 * 5^2 * 7^3 * 11 * 13 * 43`, resulta
ser `m_{sigma*}(6)`.

<!-- hallazgo:prueba -->
## Por qué valen los enunciados

**Teorema 2:** son dos cotas inferiores sobre el mismo producto. El antecesor de
`P` en el ciclo aporta una potencia de primo `q^e` con `P | f(q^e)`, así que
`q^e >= a_f(P)` por definición de `a_f`; los `k-2` primos restantes son distintos
entre sí y distintos de `P` y de `q`, así que su producto es al menos el
primorial. La cota se evalúa en enteros: un flotante en el borde podría descartar
un testigo legítimo.

**Teorema 3:** es una cuenta de flechas. En `n'` los vértices `q_j` con `j != i`
conservan su exponente, así que siguen apuntando sólo a `q_{j+1}`, y la condición
5 dice que tampoco apuntan a `p`; `q_i` apunta a `p` por la condición 1 y a
ningún `q_j` por la 3; `p` apunta a `q_{i+1}` por la 2, a ningún otro `q_j` por
la 4, y no a sí mismo por localidad. El digrafo es entonces exactamente el ciclo
de largo `k+1`. Las condiciones 3–5 no son burocracia: sin ellas, el mismo
movimiento sobre `m_sigma(5)` da `1103602500`, cuya cintura es **2**.

**Teorema 4:** es una construcción. Sean `p_1 < ... < p_{k+1}` los `k+1` primos
más chicos y `P_1 < ... < P_k` cualesquiera `k` primos distintos de ellos. Se
define `f(p_i^e) = p_{i+1}` y `f(P_j^e) = P_{j+1}` cíclicamente, y `f(q^e) = 1`
en los demás. Es multiplicativa por construcción y local, y su conjunto de
flechas es exactamente dos ciclos disjuntos, de largos `k+1` y `k`. Un testigo de
cintura `k` debe entonces contener todos los `P_j`, de donde
`m_f(k) = P_1...P_k`, mientras `m_f(k+1) = p_1...p_{k+1}`; tomando los `P_j`
grandes, la razón no está acotada.

<!-- hallazgo:comprobar -->
## Comprobación

```bash
git clone https://github.com/jorgell23-sys/covering-digraph-girth
cd covering-digraph-girth
python verify.py
```

413 comprobaciones, sin instalar nada, `PASS` o `FAIL` en cada una y código de
salida 1 si alguna falla. Rederivan cada valor publicado desde las definiciones,
redemuestran exhaustivamente los alcanzables, construyen la `f` del Teorema 4 y
localizan sus mínimos por fuerza bruta, y contrastan el conteo de `S(sigma)` por
debajo de `10^9` contra Pollack y Pomerance (2012).

<!-- hallazgo:nodice -->
## Qué no se afirma

El conjunto de base **no es nuevo**: para `sigma` son los *prime-abundant
numbers* de Pollack y Pomerance, catalogados como
[A175200](https://oeis.org/A175200). Lo que se calcula acá es un invariante de
grafo sobre esa familia. La minimalidad se afirma sólo para las cinturas
listadas; las celdas vacías son desconocidas, no cero. Si existe un testigo de
cada cintura queda intacto. El certificado es de una sola dirección, y el Teorema
4 muestra que no puede volverse una caracterización para `f` general.

---

> ¿Recién llegás? [**Explicado desde cero**](https://jorgell23-sys.github.io/covering-digraph-girth/es/),
> con dibujos y sin dar nada por sabido
> ([English](https://jorgell23-sys.github.io/covering-digraph-girth/)).

---

## Los términos

En **negrita**, los calculados en este trabajo; todos demostradamente mínimos.

| `k` | `sigma` | `sigma*` | `phi*` | `sigma**` |
|---:|---:|---:|---:|---:|
| 2 | 6 | 6 | 12 | **6** |
| 3 | 234 | 6615 | 66825 | **15925** |
| 4 | 137214 | 4380453 | 1120454775 | **2321865** |
| 5 | 275900625 | 540765225 | **1663175056640625** | **10762773021** |
| 6 | 180141399900 | 474549075 | | **3321843525** |
| 7 | **7746928876851255** | 4485174218525 | | **345358414826425** |
| 8 | **31674203849435875** | **2386830845734335** | | |
| 9 | | **9928651387877145** | | |
| 10 | | **10858178043907173985005** | | |

| `k` | `sigma*_3` | `sigma*_5` | `sigma*_6` |
|---:|---:|---:|---:|
| 2 | **6** | **6** | **10** |
| 3 | **2565** | **2013** | **207553** |
| 4 | **9933** | **32175** | **237133** |
| 5 | **2175327** | **3910725** | |
| 6 | **1278999267** | | |

| `k` | `phi*_3` | `phi*_4` | `phi*_5` | `phi*_6` |
|---:|---:|---:|---:|---:|
| 2 | **12** | **6** | **12** | **6** |
| 3 | **16891** | **207553** | **27951** | **17501** |
| 4 | **26217125** | **16099333** | **161994931** | **4176227** |
| 5 | **76670443861** | **2534414641** | | |

`data/terms.json` trae cada valor con su factorización, su ciclo y el primo hasta
el que llegó la enumeración. Se regenera por cálculo, no se transcribe.

## Las bajadas

`m_f(k+1) < m_f(k)` ocurre **dos veces** entre los 64 pasos consecutivos con los
dos mínimos conocidos, y las dos en el paso `5 -> 6`:

| f | paso | `m_f(k)` | `m_f(k+1)` | razón |
|---|---|---:|---:|---:|
| `sigma**` | 5 -> 6 | 10762773021 | 3321843525 | **0,309** |
| `sigma*` | 5 -> 6 | 540765225 | 474549075 | **0,878** |

La mediana de las 64 razones es **587**, así que las dos bajadas son excepciones
aisladas y no la cola de una distribución que llega hasta 1. La razón más chica
que no es bajada es la de `sigma*_6` de cintura 3 a 4, 1,143, y queda **fuera**
del paso `5 -> 6`.

El certificado del Teorema 3 dispara exactamente en esos dos pares y devuelve el
mínimo siguiente exacto. Comparando factorizaciones sobre los 49 pares donde la
cirugía puede probarse, acierta precisamente cuando `m_f(k+1)` se obtiene de
`m_f(k)` agregando un primo y cambiando un exponente: 49 coincidencias de 49.
Como `m_f(k+1)` tiene siempre exactamente un primo más que `m_f(k)` por el
Teorema 1, insertar dos vértices no puede dar el mínimo siguiente.

Las condiciones 3–5 hay que cumplirlas contra todos los vértices del ciclo, lo
que sugiere que se vuelven más difíciles al crecer `k`. Medido sobre 6661
inserciones candidatas que cumplen las condiciones 1 y 2, la tasa de
supervivencia cae una sola vez —de 7,59 % en cintura a lo sumo 3 a 1,72 % en
cintura 4 o más, `chi^2 = 138,5` con un grado de libertad— y de ahí en adelante
es **constante**: el `chi^2` de homogeneidad vale 10,2 con seis grados de
libertad. Lo que se agota al crecer `k` no es la admisibilidad sino la
admisibilidad barata.

## Los límites, con número

Dos términos quedan acorralados y no determinados:

| | demostrado mayor que | testigo exhibido en | primos para cerrarlo |
|---|---:|---:|---:|
| `m_sigma(9)` | `1,24e21` | `1,23e24` | `2,20e9` |
| `m_phi*(6)` | `1,3e18` | `4,15e22` | `1,4e10` |

Las dos cotas son teoremas: la inferior porque la búsqueda por debajo fue
exhaustiva, la superior porque el testigo está exhibido y verificado. Cerrar
cualquiera de las dos exige enumerar esa cantidad de primos, que no entra en
memoria acá. Varios términos más quedan fuera de alcance por costo y no por
principio: `sigma*_6` en cintura 5 y `phi*_5` en cintura 5 se estiman en 184 y 18
días sobre seis núcleos, y `sigma*_4` en cintura 4 exigiría `1,5e12` primos.

## Los métodos, y cómo se contrastan

Tres implementaciones que no comparten lógica. Una criba halla testigos por
búsqueda exhaustiva sobre enteros y no sabe nada de ciclos; un constructor los
arma a partir de ciclos sobre primos chicos y nunca mira un entero que no venga
de uno; la búsqueda exacta demuestra minimalidad por el Teorema 2 y no acepta
nada sin recalcular la cintura desde el entero mismo. Coinciden en todos los
términos que más de una alcanza.

Hay además un control externo. La criba cuenta **5327** elementos de `S(sigma)`
por debajo de `10^9` sin contar `n = 1`; Pollack y Pomerance cuentan **5328**
contándolo. La coincidencia contrasta este código contra un resultado con
revisión de pares obtenido de forma independiente.

Las búsquedas de trabajo previo —OEIS y seis bases bibliográficas, cada una con
un control positivo que sí devuelve la literatura relevante— están registradas
con su fecha y sus términos de consulta en [`PRIOR_ART.md`](PRIOR_ART.md). *No
haberlo encontrado no es lo mismo que ser nuevo.*

## Qué hay acá

| | |
|---|---|
| [`RESULT.md`](RESULT.md) | el informe completo: enunciados, demostraciones, tablas, límites |
| [`PRIOR_ART.md`](PRIOR_ART.md) | qué se buscó de trabajo previo, dónde y cuándo |
| `verify.py` | todas las comprobaciones, una orden, sin dependencias |
| `src/arithmetic.py` | las definiciones, en Python liso |
| `src/exact.py` | demuestra minimalidad con el lema de corte |
| `src/construct.py` | arma testigos desde ciclos sobre primos chicos |
| `src/sieve.py` | búsqueda exhaustiva sobre enteros (necesita numpy) |
| `src/surgery.py` | el Teorema 3 y su certificado |
| `src/parallel.py` | la misma búsqueda exacta, repartida entre núcleos |
| `src/make_terms.py` | regenera `data/terms.json` por cálculo |

La versión en inglés de esta página: [`README.md`](README.md).

## Cómo citar

Ver [`CITATION.cff`](CITATION.cff). Licencia: MIT para el código, CC BY 4.0 para
texto y datos.

## Autor

**Jorge Ellena Godoy**.

El diseño del sistema y la dirección de la investigación son del autor. Los
resultados matemáticos fueron producidos por un sistema automatizado (Claude,
Anthropic) bajo esa dirección. Todos los cálculos fueron verificados por
implementaciones independientes y contrastados contra trabajo publicado. El autor
es responsable de la corrección de todo lo publicado acá.
